from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from .models import RepairAllocationInstallment, RepairCost, RepairCostAllocation


@transaction.atomic
def create_cost_allocations(repair_cost_id, allocations, actor=None):
    """Create the complete financial distribution for one actual repair cost."""
    repair_cost = RepairCost.objects.select_for_update().get(pk=repair_cost_id)
    if repair_cost.allocations.filter(is_active=True).exists():
        raise ValidationError("El costo ya tiene una distribución financiera activa.")
    total = sum(Decimal(str(item["amount"])) for item in allocations)
    if total != repair_cost.total:
        raise ValidationError("La distribución financiera debe sumar exactamente el costo real.")
    created = []
    for item in allocations:
        allocation = RepairCostAllocation.objects.create(
            repair_cost=repair_cost,
            responsible_type=item["responsible_type"],
            responsible_party_id=item.get("responsible_party_id"),
            amount=item["amount"],
            percentage=item.get("percentage"),
            application_method=item["application_method"],
            installment_count=len(item["installments"]),
            created_by=actor,
            updated_by=actor,
        )
        installment_total = sum(Decimal(str(row["amount"])) for row in item["installments"])
        if installment_total != Decimal(str(item["amount"])):
            raise ValidationError("Las cuotas deben sumar el valor asignado al responsable.")
        for index, installment in enumerate(item["installments"], start=1):
            RepairAllocationInstallment.objects.create(
                allocation=allocation,
                installment_number=index,
                due_date=installment["due_date"],
                amount=installment["amount"],
                created_by=actor,
                updated_by=actor,
            )
        created.append(allocation)
    return created
