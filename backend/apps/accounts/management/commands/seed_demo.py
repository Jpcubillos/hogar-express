from datetime import date
from decimal import Decimal

from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.management.base import BaseCommand

from apps.accounts.models import User
from apps.catalogs.models import City, Country, Department, IdentificationType, Neighborhood, PropertyType
from apps.owners.models import Owner
from apps.people.models import Party
from apps.properties.models import Property, PropertyOwnership, RentalListing


class Command(BaseCommand):
    help = "Carga usuarios y datos ficticios mínimos para desarrollo"

    def handle(self, *args, **options):
        call_command("seed_catalogs")
        call_command("seed_roles")
        roles_users = {
            "admin": ("admin@example.test", "Administrador"),
            "intern": ("intern@example.test", "Asesor Interno"),
            "extern": ("extern@example.test", "Asesor Externo"),
            "visitor": ("visitor@example.test", "Consulta"),
        }
        for username, (email, group_name) in roles_users.items():
            user, _ = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": email,
                    "display_name": f"Demo {group_name}",
                    "is_staff": group_name == "Administrador",
                    "is_superuser": group_name == "Administrador",
                },
            )
            user.set_password("change_me")
            user.is_active = True
            user.save()
            user.groups.add(Group.objects.get(name=group_name))

        identification_type = IdentificationType.objects.get(code="CC")
        party, _ = Party.objects.get_or_create(
            identification_type=identification_type,
            identification_number="31452778",
            defaults={
                "party_type": Party.PartyType.NATURAL,
                "first_name": "María Elena",
                "last_name": "Castaño Ruiz",
                "display_name": "María Elena Castaño Ruiz",
            },
        )
        owner, _ = Owner.objects.get_or_create(party=party, defaults={"internal_code": "PROP-DEMO-001"})
        property_obj, _ = Property.objects.get_or_create(
            internal_code="INM-DEMO-001",
            defaults={
                "property_type": PropertyType.objects.get(code="APARTMENT"),
                "address_line": "Calle 5 #38-21",
                "unit_number": "502",
                "country": Country.objects.get(code="CO"),
                "department": Department.objects.get(code="CO-VAC"),
                "city": City.objects.get(code="CO-VAC-CALI"),
                "neighborhood": Neighborhood.objects.get(code="TEQUENDAMA"),
                "stratum": 5,
                "private_area": Decimal("78.00"),
                "bedrooms": 2,
                "bathrooms": 2,
            },
        )
        PropertyOwnership.objects.get_or_create(
            property=property_obj,
            owner=owner,
            valid_from=date(2026, 1, 1),
            defaults={"ownership_percentage": Decimal("100.0000"), "is_primary": True},
        )
        RentalListing.objects.get_or_create(
            property=property_obj,
            status=RentalListing.Status.AVAILABLE,
            defaults={"asking_rent": Decimal("1450000.00"), "available_from": date(2026, 1, 1)},
        )
        self.stdout.write(self.style.SUCCESS("Datos de demostración cargados."))
