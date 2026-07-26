from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from django.db.models import Q, Count, Avg, Sum, F

from apps.repairs.models import (
    RepairIncident,
    RepairOrder,
    RepairTask,
    RepairQuote,
    RepairQuoteItem,
    RepairCost,
    RepairApproval,
    RepairWarranty,
    RepairComment,
    RepairTimelineEvent,
    RepairPriority,
)
from apps.repairs.serializers import (
    RepairIncidentSerializer,
    RepairOrderSerializer,
    RepairTaskSerializer,
    RepairQuoteSerializer,
    RepairQuoteItemSerializer,
    RepairCostSerializer,
    RepairApprovalSerializer,
    RepairWarrantySerializer,
    RepairCommentSerializer,
    RepairTimelineEventSerializer,
)
from apps.repairs.services import RepairService


class RepairIncidentViewSet(viewsets.ModelViewSet):
    queryset = RepairIncident.objects.filter(is_active=True).select_related("property", "rental", "category", "reported_by_user", "reported_by_party")
    serializer_class = RepairIncidentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["property", "rental", "status", "priority", "severity", "repair_type"]
    search_fields = ["title", "description", "review_notes"]


class RepairOrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet principal para el Aggregate Root (RepairOrder).
    Utiliza select_related y prefetch_related para evitar N+1 queries.
    """
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["property", "rental", "status", "priority", "severity", "repair_type", "internal_responsible", "current_provider"]
    search_fields = ["order_number", "title", "description"]
    serializer_class = RepairOrderSerializer

    def get_queryset(self):
        return (
            RepairOrder.objects.filter(is_active=True)
            .select_related(
                "incident",
                "property",
                "rental",
                "category",
                "internal_responsible",
                "current_provider",
                "verified_by",
            )
            .prefetch_related(
                "tasks__assigned_provider__party",
                "quotes__provider__party",
                "quotes__items",
                "costs__provider__party",
                "approvals__decided_by_user",
                "warranties__provider__party",
                "comments__user",
                "timeline_events__performed_by",
                "status_history__changed_by",
            )
        )

    @action(detail=True, methods=["post"], url_path="change-status")
    def change_status(self, request, pk=None):
        """
        Endpoint que delega la transición de estado a RepairService con verificación de permisos por rol.
        """
        repair_order = self.get_object()
        new_status = request.data.get("status")
        reason = request.data.get("reason", "")

        if not new_status:
            return Response({"error": "El nuevo estado 'status' es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        # Permission checks for critical status transitions
        if new_status == "APPROVED" and not (request.user.is_staff or request.user.has_perm("repairs.approve_repair")):
            return Response({"error": "No tienes permisos suficientes para aprobar esta orden de reparación."}, status=status.HTTP_403_FORBIDDEN)

        if new_status == "CLOSED" and not (request.user.is_staff or request.user.has_perm("repairs.close_repair")):
            return Response({"error": "No tienes permisos suficientes para cerrar esta orden de reparación."}, status=status.HTTP_403_FORBIDDEN)

        try:
            updated_order = RepairService.change_status(repair_order, new_status, user=request.user, reason=reason)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(updated_order)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="update-priority")
    def update_priority(self, request, pk=None):
        """
        Endpoint para actualizar prioridad y recalcular SLA vía RepairService.
        """
        repair_order = self.get_object()
        new_priority = request.data.get("priority")

        if not new_priority or new_priority not in RepairPriority.values:
            return Response({"error": "Prioridad inválida."}, status=status.HTTP_400_BAD_REQUEST)

        updated_order = RepairService.update_priority(repair_order, new_priority, user=request.user)
        serializer = self.get_serializer(updated_order)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="dashboard-summary")
    def dashboard_summary(self, request):
        """
        Endpoint avanzado con métricas operativas y financieras completas.
        """
        now = timezone.now()
        qs = self.get_queryset()

        total_active = qs.exclude(status__in=["CLOSED", "CANCELLED"]).count()
        critical_count = qs.filter(priority=RepairPriority.CRITICAL).exclude(status__in=["CLOSED", "CANCELLED"]).count()
        pending_approval_count = qs.filter(status="PENDING_APPROVAL").count()
        scheduled_count = qs.filter(status="SCHEDULED").count()
        overdue_count = qs.filter(sla_deadline__lt=now).exclude(status__in=["CLOSED", "CANCELLED", "COMPLETED"]).count()

        total_orders = qs.count() or 1
        sla_compliant_orders = qs.filter(Q(sla_deadline__gte=now) | Q(status__in=["CLOSED", "COMPLETED"])).count()
        sla_compliance_rate = round((sla_compliant_orders / total_orders) * 100, 1)

        total_quoted_sum = RepairQuote.objects.filter(status="SELECTED", is_active=True).aggregate(val=Sum("total"))["val"] or 0
        total_actual_sum = RepairCost.objects.filter(category_type="ACTUAL", is_active=True).aggregate(val=Sum("total"))["val"] or 0
        avg_repair_cost = round(float(total_actual_sum / total_orders), 2)

        return Response({
            "active": total_active,
            "critical": critical_count,
            "pending_approval": pending_approval_count,
            "scheduled": scheduled_count,
            "overdue": overdue_count,
            "sla_compliance_rate": sla_compliance_rate,
            "total_quoted_cost": float(total_quoted_sum),
            "total_actual_cost": float(total_actual_sum),
            "avg_repair_cost": avg_repair_cost,
        })

    # =========================================================================
    # ENDPOINTS DE INTEGRACIÓN CON OTROS MÓDULOS (Properties, Owners, Rentals, Sales, Dashboard)
    # =========================================================================

    @action(detail=False, methods=["get"], url_path="by-property")
    def by_property(self, request):
        property_id = request.query_params.get("property_id")
        if not property_id:
            return Response({"error": "Parámetro 'property_id' es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        summary = RepairService.get_property_repairs_summary(property_id)
        return Response(summary)

    @action(detail=False, methods=["get"], url_path="by-owner")
    def by_owner(self, request):
        owner_id = request.query_params.get("owner_id")
        if not owner_id:
            return Response({"error": "Parámetro 'owner_id' es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        summary = RepairService.get_owner_repairs_summary(owner_id)
        return Response(summary)

    @action(detail=False, methods=["get"], url_path="by-rental")
    def by_rental(self, request):
        rental_id = request.query_params.get("rental_id")
        if not rental_id:
            return Response({"error": "Parámetro 'rental_id' es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        summary = RepairService.get_rental_repairs_summary(rental_id)
        return Response(summary)

    @action(detail=False, methods=["get"], url_path="by-sales-property")
    def by_sales_property(self, request):
        property_id = request.query_params.get("property_id")
        if not property_id:
            return Response({"error": "Parámetro 'property_id' es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        summary = RepairService.get_sales_repairs_summary(property_id)
        return Response(summary)

    @action(detail=False, methods=["get"], url_path="dashboard-widgets")
    def dashboard_widgets(self, request):
        data = RepairService.get_dashboard_widgets_data()
        return Response(data)

    @action(detail=False, methods=["get"], url_path="critical")
    def critical_orders(self, request):
        qs = self.get_queryset().filter(priority=RepairPriority.CRITICAL).exclude(status__in=["CLOSED", "CANCELLED"])
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="pending-approval")
    def pending_approval_orders(self, request):
        qs = self.get_queryset().filter(status="PENDING_APPROVAL")
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="overdue")
    def overdue_orders(self, request):
        qs = self.get_queryset().filter(sla_deadline__lt=timezone.now()).exclude(status__in=["CLOSED", "CANCELLED", "COMPLETED"])
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class RepairTaskViewSet(viewsets.ModelViewSet):
    queryset = RepairTask.objects.filter(is_active=True).select_related("repair_order", "assigned_provider__party")
    serializer_class = RepairTaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["repair_order", "assigned_provider", "status"]


class RepairQuoteViewSet(viewsets.ModelViewSet):
    queryset = RepairQuote.objects.filter(is_active=True).select_related("repair", "provider__party", "selected_by").prefetch_related("items")
    serializer_class = RepairQuoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["repair", "provider", "status"]

    @action(detail=True, methods=["post"], url_path="select")
    def select_quote(self, request, pk=None):
        quote = self.get_object()
        selected_quote = RepairService.select_quote(quote, user=request.user)
        serializer = self.get_serializer(selected_quote)
        return Response(serializer.data)


class RepairQuoteItemViewSet(viewsets.ModelViewSet):
    queryset = RepairQuoteItem.objects.all().select_related("quote", "unit")
    serializer_class = RepairQuoteItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class RepairCostViewSet(viewsets.ModelViewSet):
    queryset = RepairCost.objects.filter(is_active=True).select_related("repair", "task", "quote_item", "provider__party", "unit", "document")
    serializer_class = RepairCostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["repair", "provider", "category_type", "cost_type"]


class RepairApprovalViewSet(viewsets.ModelViewSet):
    queryset = RepairApproval.objects.filter(is_active=True).select_related("repair", "requested_from", "decided_by_user", "decided_by_party", "evidence_document")
    serializer_class = RepairApprovalSerializer
    permission_classes = [permissions.IsAuthenticated]


class RepairWarrantyViewSet(viewsets.ModelViewSet):
    queryset = RepairWarranty.objects.filter(is_active=True).select_related("repair", "provider__party")
    serializer_class = RepairWarrantySerializer
    permission_classes = [permissions.IsAuthenticated]


class RepairCommentViewSet(viewsets.ModelViewSet):
    queryset = RepairComment.objects.all().select_related("repair", "user", "document")
    serializer_class = RepairCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        repair_order = serializer.validated_data["repair"]
        text = serializer.validated_data["text"]
        document = serializer.validated_data.get("document")
        is_internal = serializer.validated_data.get("is_internal", True)

        comment = RepairService.add_comment(
            repair_order=repair_order,
            text=text,
            document=document,
            user=self.request.user,
            is_internal=is_internal
        )
        return comment


class RepairTimelineEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RepairTimelineEvent.objects.all().select_related("repair", "performed_by")
    serializer_class = RepairTimelineEventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["repair", "event_type"]
