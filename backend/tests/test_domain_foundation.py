from decimal import Decimal

import pytest
from django.contrib.auth.models import Group
from django.core.management import call_command

from apps.catalogs.models import Country, PropertyType
from apps.accounts.serializers import UserManagementSerializer
from apps.configuration.models import NumberSequence, Organization
from apps.owners.models import Owner
from apps.properties.models import Property, PropertyOwnership


@pytest.mark.django_db(transaction=True)
def test_seed_catalogs_is_idempotent():
    call_command("seed_catalogs")
    initial = (Country.objects.count(), PropertyType.objects.count(), Organization.objects.count())
    call_command("seed_catalogs")
    assert (Country.objects.count(), PropertyType.objects.count(), Organization.objects.count()) == initial
    assert Country.objects.get(code="CO").name == "Colombia"
    assert NumberSequence.objects.filter(document_kind="TENANT").exists()


@pytest.mark.django_db(transaction=True)
def test_seed_roles_is_idempotent():
    call_command("seed_catalogs")
    call_command("seed_roles")
    call_command("seed_roles")
    assert set(Group.objects.values_list("name", flat=True)) >= {
        "Administrador",
        "Asesor Interno",
        "Asesor Externo",
        "Consulta",
    }
    assert Group.objects.get(name="Administrador").permissions.exists()


@pytest.mark.django_db(transaction=True)
def test_seed_demo_creates_normalized_owner_and_property():
    call_command("seed_demo")
    owner = Owner.objects.get(internal_code="PROP-DEMO-001")
    property_obj = Property.objects.get(internal_code="INM-DEMO-001")
    ownership = PropertyOwnership.objects.get(property=property_obj, owner=owner, valid_to__isnull=True)
    assert ownership.ownership_percentage == Decimal("100.0000")
    assert property_obj.rental_listings.filter(status="AVAILABLE").exists()


@pytest.mark.django_db
def test_user_management_serializer_hashes_password():
    serializer = UserManagementSerializer(
        data={
            "username": "api-user",
            "password": "ClaveSegura123!",
            "email": "api-user@example.com",
        }
    )
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    assert user.check_password("ClaveSegura123!")
    assert serializer.data.get("password") is None
