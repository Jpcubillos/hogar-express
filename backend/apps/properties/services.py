from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum

from apps.owners.models import Owner

from .models import Property, PropertyOwnership


@transaction.atomic
def replace_current_ownerships(property_id, ownerships, valid_from, actor=None):
    """Replace current ownership rows and enforce an exact 100% distribution."""
    property_obj = Property.objects.select_for_update().get(pk=property_id)
    total = sum(Decimal(str(item["percentage"])) for item in ownerships)
    if total != Decimal("100"):
        raise ValidationError("La participación vigente de propietarios debe sumar exactamente 100%.")
    primary_count = sum(bool(item.get("is_primary")) for item in ownerships)
    if primary_count != 1:
        raise ValidationError("Debe existir exactamente un propietario principal.")
    PropertyOwnership.objects.filter(property=property_obj, valid_to__isnull=True).update(
        valid_to=valid_from - timedelta(days=1)
    )
    rows = []
    for item in ownerships:
        rows.append(
            PropertyOwnership(
                property=property_obj,
                owner=Owner.objects.get(pk=item["owner_id"]),
                ownership_percentage=item["percentage"],
                is_primary=item.get("is_primary", False),
                valid_from=valid_from,
                created_by=actor,
                updated_by=actor,
            )
        )
    PropertyOwnership.objects.bulk_create(rows)
    return rows


def validate_current_ownership(property_id):
    total = (
        PropertyOwnership.objects.filter(property_id=property_id, valid_to__isnull=True)
        .aggregate(total=Sum("ownership_percentage"))["total"]
        or Decimal("0")
    )
    if total != Decimal("100"):
        raise ValidationError("La participación vigente de propietarios no suma 100%.")
    return total
