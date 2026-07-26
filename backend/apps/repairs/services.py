from datetime import timedelta
from decimal import Decimal

from django.db import transaction
from django.db.models import Avg, Count, F, Q, Sum
from django.utils import timezone

from apps.repairs.models import (
    RepairApproval,
    RepairComment,
    RepairCost,
    RepairCostAllocation,
    RepairOrder,
    RepairPriority,
    RepairQuote,
    RepairStatusHistory,
    RepairTask,
    RepairTimelineEvent,
    RepairWarranty,
)
from apps.repairs.state_machine import RepairStateMachine


class RepairService:
    """
    Capa de servicio del Dominio de Reparaciones.
    Toda mutación se ejecuta dentro de transaction.atomic() y emite
    eventos automáticos en el Timeline. Proporciona además contratos
    de consulta desacoplados para Inmuebles, Propietarios, Alquileres,
    Ventas y el Dashboard General.
    """

    @classmethod
    @transaction.atomic
    def change_status(cls, repair_order: RepairOrder, new_status: str, user=None, reason: str = "") -> RepairOrder:
        """
        Ejecuta una transición de estado validada por RepairStateMachine dentro de una transacción atómica.
        """
        RepairStateMachine.validate_transition(repair_order, new_status, user=user, reason=reason)

        previous_status = repair_order.status
        repair_order.status = new_status

        if new_status == "COMPLETED":
            repair_order.completed_at = timezone.now()
        elif new_status == "CLOSED":
            repair_order.closed_at = timezone.now()
            repair_order.verified_by = user
            repair_order.verified_at = timezone.now()
            repair_order.verification_notes = reason or "Verificación y cierre completados."
        elif new_status == "CANCELLED":
            repair_order.cancelled_at = timezone.now()
            repair_order.cancellation_reason = reason

        repair_order.save()

        # Record Status History
        RepairStatusHistory.objects.create(
            repair=repair_order,
            previous_status=previous_status,
            new_status=new_status,
            reason=reason,
            changed_by=user,
        )

        # Record Automated Timeline Event
        event_type = RepairTimelineEvent.EventType.STATUS_CHANGE
        if new_status == "CLOSED":
            event_type = RepairTimelineEvent.EventType.CLOSED
        elif new_status == "CANCELLED":
            event_type = RepairTimelineEvent.EventType.CANCELLED
        elif new_status == "APPROVED":
            event_type = RepairTimelineEvent.EventType.APPROVED

        RepairTimelineEvent.objects.create(
            repair=repair_order,
            event_type=event_type,
            title=f"Estado cambiado a {repair_order.get_status_display()}",
            description=f"Transición de {previous_status} a {new_status}. {reason}".strip(),
            performed_by=user,
            metadata={"previous_status": previous_status, "new_status": new_status, "reason": reason},
        )

        return repair_order

    @classmethod
    @transaction.atomic
    def update_priority(cls, repair_order: RepairOrder, new_priority: str, user=None) -> RepairOrder:
        """
        Actualiza la prioridad y recalcula el SLA Deadline dentro de una transacción atómica.
        """
        if repair_order.priority == new_priority:
            return repair_order

        previous_priority = repair_order.priority
        previous_sla = repair_order.sla_deadline

        repair_order.priority = new_priority
        
        # Recalculate SLA
        base_time = repair_order.created_at or timezone.now()
        hours_map = {
            RepairPriority.CRITICAL: 24,
            RepairPriority.HIGH: 48,
            RepairPriority.MEDIUM: 120,
            RepairPriority.LOW: 240,
        }
        hours = hours_map.get(new_priority, 120)
        repair_order.sla_deadline = base_time + timedelta(hours=hours)
        repair_order.save()

        # Log timeline event
        RepairTimelineEvent.objects.create(
            repair=repair_order,
            event_type=RepairTimelineEvent.EventType.PRIORITY_CHANGE,
            title=f"Prioridad actualizada a {repair_order.get_priority_display()}",
            description=f"Prioridad cambiada de {previous_priority} a {new_priority}. SLA actualizado.",
            performed_by=user,
            metadata={
                "previous_priority": previous_priority,
                "new_priority": new_priority,
                "previous_sla": previous_sla.isoformat() if previous_sla else None,
                "new_sla": repair_order.sla_deadline.isoformat(),
            },
        )

        return repair_order

    @classmethod
    @transaction.atomic
    def select_quote(cls, quote: RepairQuote, user=None) -> RepairQuote:
        """
        Selecciona una cotización como ganadora y deshabilita las demás para la orden.
        """
        repair_order = quote.repair
        
        # Unselect any previous selected quote
        repair_order.quotes.filter(status="SELECTED").update(status="REJECTED")

        quote.status = "SELECTED"
        quote.selected_by = user
        quote.selected_at = timezone.now()
        quote.save()

        # Update order current provider
        repair_order.current_provider = quote.provider
        repair_order.save()

        # Log timeline event
        RepairTimelineEvent.objects.create(
            repair=repair_order,
            event_type=RepairTimelineEvent.EventType.QUOTE_SELECTED,
            title=f"Cotización #{quote.quote_number or quote.id} seleccionada",
            description=f"Proveedor: {quote.provider.party.display_name}. Valor total: ${quote.total:,.2f}",
            performed_by=user,
            metadata={"quote_id": str(quote.id), "total": str(quote.total)},
        )

        return quote

    @classmethod
    @transaction.atomic
    def add_comment(cls, repair_order: RepairOrder, text: str, document=None, user=None, is_internal=True) -> RepairComment:
        """
        Agrega un comentario al historial y emite evento en el Timeline.
        """
        comment = RepairComment.objects.create(
            repair=repair_order,
            user=user,
            text=text,
            document=document,
            is_internal=is_internal,
        )

        RepairTimelineEvent.objects.create(
            repair=repair_order,
            event_type=RepairTimelineEvent.EventType.COMMENT_ADDED,
            title="Comentario registrado",
            description=text[:150] + ("..." if len(text) > 150 else ""),
            performed_by=user,
            metadata={"comment_id": str(comment.id), "has_document": document is not None},
        )

        return comment

    # =========================================================================
    # CONTRATOS DE INTEGRACIÓN CON OTROS MÓDULOS DEL SISTEMA
    # =========================================================================

    @classmethod
    def get_property_repairs_summary(cls, property_id) -> dict:
        """
        Contrato de Integración con el Módulo de Inmuebles.
        Retorna el resumen completo de reparaciones para una propiedad especifica.
        """
        qs = RepairOrder.objects.filter(property_id=property_id, is_active=True)

        active_orders = qs.exclude(status__in=["CLOSED", "CANCELLED"])
        closed_orders = qs.filter(status="CLOSED")
        last_repair = qs.order_by("-created_at").first()
        next_scheduled = qs.filter(status="SCHEDULED", scheduled_start__gte=timezone.now()).order_by("scheduled_start").first()

        total_cost = RepairCost.objects.filter(repair__property_id=property_id, category_type="ACTUAL", is_active=True).aggregate(val=Sum("total"))["val"] or Decimal(0)
        active_warranties_count = RepairWarranty.objects.filter(repair__property_id=property_id, expires_on__gte=timezone.now().date(), is_active=True).count()

        return {
            "property_id": str(property_id),
            "total_repairs": qs.count(),
            "active_repairs_count": active_orders.count(),
            "pending_repairs_count": qs.filter(status__in=["REPORTED", "IN_REVIEW", "PENDING_QUOTE", "PENDING_APPROVAL"]).count(),
            "closed_repairs_count": closed_orders.count(),
            "last_repair_date": last_repair.created_at.isoformat() if last_repair else None,
            "next_scheduled_visit": next_scheduled.scheduled_start.isoformat() if next_scheduled and next_scheduled.scheduled_start else None,
            "accumulated_cost": float(total_cost),
            "active_warranties_count": active_warranties_count,
        }

    @classmethod
    def get_owner_repairs_summary(cls, owner_id) -> dict:
        """
        Contrato de Integración con el Módulo de Propietarios.
        Retorna el resumen financiero y operativo de reparaciones para un propietario.
        """
        allocations = RepairCostAllocation.objects.filter(
            responsible_type="OWNER",
            responsible_party__owner__id=owner_id,
            is_active=True,
        )

        total_allocated = allocations.aggregate(val=Sum("amount"))["val"] or Decimal(0)
        total_pending = allocations.filter(status="PENDING").aggregate(val=Sum("amount"))["val"] or Decimal(0)
        total_settlement_deducted = allocations.filter(application_method="OWNER_SETTLEMENT", status="APPLIED").aggregate(val=Sum("amount"))["val"] or Decimal(0)

        orders_qs = RepairOrder.objects.filter(property__ownerships__owner_id=owner_id, is_active=True).distinct()
        active_warranties = RepairWarranty.objects.filter(repair__property__ownerships__owner_id=owner_id, expires_on__gte=timezone.now().date(), is_active=True).count()

        return {
            "owner_id": str(owner_id),
            "total_repairs_count": orders_qs.count(),
            "pending_repairs_count": orders_qs.exclude(status__in=["CLOSED", "CANCELLED"]).count(),
            "total_cost_allocated": float(total_allocated),
            "pending_charge_amount": float(total_pending),
            "settlement_deducted_amount": float(total_settlement_deducted),
            "active_warranties_count": active_warranties,
        }

    @classmethod
    def get_rental_repairs_summary(cls, rental_id) -> dict:
        """
        Contrato de Integración con el Módulo de Alquileres.
        Retorna las reparaciones y afectaciones financieras ligadas a un contrato de arrendamiento.
        """
        qs = RepairOrder.objects.filter(rental_id=rental_id, is_active=True)

        tenant_allocations = RepairCostAllocation.objects.filter(
            repair_cost__repair__rental_id=rental_id,
            responsible_type="TENANT",
            is_active=True,
        )

        owner_allocations = RepairCostAllocation.objects.filter(
            repair_cost__repair__rental_id=rental_id,
            responsible_type="OWNER",
            is_active=True,
        )

        return {
            "rental_id": str(rental_id),
            "total_repairs_count": qs.count(),
            "active_repairs_count": qs.exclude(status__in=["CLOSED", "CANCELLED"]).count(),
            "tenant_total_charges": float(tenant_allocations.aggregate(val=Sum("amount"))["val"] or 0),
            "owner_total_deductions": float(owner_allocations.aggregate(val=Sum("amount"))["val"] or 0),
            "has_blocking_repairs": qs.filter(priority=RepairPriority.CRITICAL).exclude(status__in=["CLOSED", "CANCELLED"]).exists(),
        }

    @classmethod
    def get_sales_repairs_summary(cls, property_id) -> dict:
        """
        Contrato de Integración con el Módulo de Ventas.
        Retorna el historial de mejoras e inversión en reparaciones para un inmueble en comercialización.
        """
        qs = RepairOrder.objects.filter(property_id=property_id, is_active=True)

        total_invested = RepairCost.objects.filter(
            repair__property_id=property_id,
            category_type="ACTUAL",
            is_active=True,
        ).aggregate(val=Sum("total"))["val"] or Decimal(0)

        improvements = qs.filter(repair_type__in=["PREVENTIVE", "PERIODIC_MAINTENANCE"], status="CLOSED")

        return {
            "property_id": str(property_id),
            "active_repairs_count": qs.exclude(status__in=["CLOSED", "CANCELLED"]).count(),
            "pending_repairs_count": qs.filter(status__in=["REPORTED", "IN_REVIEW", "PENDING_QUOTE", "PENDING_APPROVAL"]).count(),
            "closed_repairs_count": qs.filter(status="CLOSED").count(),
            "total_invested_amount": float(total_invested),
            "improvements_count": improvements.count(),
        }

    @classmethod
    def get_dashboard_widgets_data(cls) -> dict:
        """
        Contrato de Integración con el Dashboard General.
        Expone métricas agregadas globales por proveedor, categoría y cumplimiento de SLA.
        """
        now = timezone.now()
        qs = RepairOrder.objects.filter(is_active=True)

        by_status = dict(qs.values("status").annotate(count=Count("id")).values_list("status", "count"))
        by_priority = dict(qs.values("priority").annotate(count=Count("id")).values_list("priority", "count"))
        by_category = dict(qs.values("category__name").annotate(count=Count("id")).values_list("category__name", "count"))
        by_provider = dict(
            qs.filter(current_provider__isnull=False)
            .values("current_provider__party__display_name")
            .annotate(count=Count("id"))
            .values_list("current_provider__party__display_name", "count")
        )

        total_orders = qs.count() or 1
        sla_compliant_orders = qs.filter(Q(sla_deadline__gte=now) | Q(status__in=["CLOSED", "COMPLETED"])).count()
        sla_compliance_rate = round((sla_compliant_orders / total_orders) * 100, 1)

        total_quoted_sum = RepairQuote.objects.filter(status="SELECTED", is_active=True).aggregate(val=Sum("total"))["val"] or 0
        total_actual_sum = RepairCost.objects.filter(category_type="ACTUAL", is_active=True).aggregate(val=Sum("total"))["val"] or 0

        return {
            "by_status": by_status,
            "by_priority": by_priority,
            "by_category": by_category,
            "by_provider": by_provider,
            "sla_compliance_rate": sla_compliance_rate,
            "total_quoted_cost": float(total_quoted_sum),
            "total_actual_cost": float(total_actual_sum),
            "avg_repair_cost": round(float(total_actual_sum / total_orders), 2),
        }
