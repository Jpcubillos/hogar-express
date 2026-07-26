from django.core.exceptions import ValidationError
from django.utils import timezone

class RepairStateMachine:
    """
    Enforces DDD invariants and strictly allowed state transitions
    for RepairOrder instances.
    """

    ALLOWED_TRANSITIONS = {
        "REPORTED": ["IN_REVIEW", "CANCELLED"],
        "IN_REVIEW": ["PENDING_QUOTE", "PENDING_APPROVAL", "CANCELLED"],
        "PENDING_QUOTE": ["PENDING_APPROVAL", "CANCELLED"],
        "PENDING_APPROVAL": ["APPROVED", "IN_REVIEW", "CANCELLED"],
        "APPROVED": ["SCHEDULED", "CANCELLED"],
        "SCHEDULED": ["IN_PROGRESS", "CANCELLED"],
        "IN_PROGRESS": ["COMPLETED", "CANCELLED"],
        "COMPLETED": ["CLOSED", "CANCELLED"],
        "CLOSED": [],       # Terminal state
        "CANCELLED": [],    # Terminal state
    }

    @classmethod
    def validate_transition(cls, repair_order, new_status: str, user=None, reason: str = ""):
        current_status = repair_order.status

        # 1. Immutable Terminal State Invariant
        if current_status in ["CLOSED", "CANCELLED"]:
            raise ValidationError(
                f"No se puede cambiar el estado de una orden finalizada ({current_status})."
            )

        # 2. Check Allowed Graph Transition
        allowed = cls.ALLOWED_TRANSITIONS.get(current_status, [])
        if new_status not in allowed:
            raise ValidationError(
                f"Transición inválida: No se permite cambiar de '{current_status}' a '{new_status}'."
            )

        # 3. Specific Invariants per Target State
        if new_status == "CANCELLED" and not reason.strip():
            raise ValidationError("Es obligatorio proporcionar un motivo de cancelación.")

        if new_status == "PENDING_APPROVAL":
            # If quote was required, ensure a selected quote exists
            has_selected_quote = repair_order.quotes.filter(status="SELECTED", is_active=True).exists()
            if current_status == "PENDING_QUOTE" and not has_selected_quote:
                raise ValidationError(
                    "No se puede solicitar aprobación sin seleccionar previamente una cotización válida."
                )

        if new_status == "APPROVED":
            # Ensure an approval decision has been registered
            has_approval = repair_order.approvals.filter(decision="APPROVED", is_active=True).exists()
            if not has_approval:
                raise ValidationError(
                    "La orden no puede pasar a Aprobada sin un registro formal de aprobación en el sistema."
                )

        if new_status == "COMPLETED":
            # Check all tasks are completed
            unfinished_tasks = repair_order.tasks.filter(is_active=True).exclude(status__in=["COMPLETED", "CANCELLED"]).count()
            if unfinished_tasks > 0:
                raise ValidationError(
                    f"Existen {unfinished_tasks} tareas pendientes. Todas las tareas deben completarse antes de terminar la orden."
                )

        if new_status == "CLOSED":
            if current_status != "COMPLETED":
                raise ValidationError("Una orden solo puede cerrarse si previamente ha sido marcada como TERMINADA.")
            if not repair_order.verification_notes and not repair_order.verified_by:
                raise ValidationError("El cierre requiere registro de verificación del trabajo realizado.")

        return True
