from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Rental, RentalContract, RentalStatusHistory


@transaction.atomic
def activate_contract(contract_id, actor=None, reason="Activación de contrato"):
    contract = RentalContract.objects.select_for_update().select_related("rental__property").get(pk=contract_id)
    rental = Rental.objects.select_for_update().get(pk=contract.rental_id)
    overlaps = RentalContract.objects.filter(
        rental__property=rental.property,
        status=RentalContract.Status.ACTIVE,
        start_date__lte=contract.end_date,
        end_date__gte=contract.start_date,
    ).exclude(pk=contract.pk)
    if overlaps.exists():
        raise ValidationError("El inmueble ya tiene un contrato activo que se cruza con estas fechas.")
    previous_status = rental.status
    RentalContract.objects.filter(rental=rental, status=RentalContract.Status.ACTIVE).exclude(pk=contract.pk).update(
        status=RentalContract.Status.EXPIRED
    )
    contract.status = RentalContract.Status.ACTIVE
    contract.updated_by = actor
    contract.save(update_fields=["status", "updated_by", "updated_at"])
    rental.status = Rental.Status.ACTIVE
    rental.started_on = contract.start_date
    rental.ended_on = contract.end_date
    rental.current_contract = contract
    rental.updated_by = actor
    rental.save(update_fields=["status", "started_on", "ended_on", "current_contract", "updated_by", "updated_at"])
    RentalStatusHistory.objects.create(
        rental=rental,
        previous_status=previous_status,
        new_status=rental.status,
        reason=reason,
        changed_by=actor,
        created_by=actor,
        updated_by=actor,
    )
    return rental
