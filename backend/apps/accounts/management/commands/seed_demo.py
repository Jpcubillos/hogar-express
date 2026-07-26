from datetime import date
from decimal import Decimal

from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.management.base import BaseCommand

from apps.accounts.models import User
from apps.catalogs.models import City, Country, Department, IdentificationType, Neighborhood, PropertyType, RepairCategory
from apps.owners.models import Owner
from apps.people.models import Party, ProviderProfile
from apps.properties.models import Property, PropertyOwnership, RentalListing
from apps.repairs.models import RepairOrder, RepairIncident, RepairPriority, RepairSeverity, RepairType


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
        nit_type = IdentificationType.objects.get(code="NIT")

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

        # Provider 1
        party_prov1, _ = Party.objects.get_or_create(
            identification_type=nit_type,
            identification_number="900123456",
            defaults={
                "party_type": Party.PartyType.LEGAL,
                "business_name": "Servicios Hidráulicos Cali S.A.S",
                "display_name": "Servicios Hidráulicos Cali S.A.S",
            },
        )
        prov1, _ = ProviderProfile.objects.get_or_create(
            party=party_prov1,
            defaults={"provider_kind": ProviderProfile.ProviderKind.COMPANY}
        )

        # Provider 2
        party_prov2, _ = Party.objects.get_or_create(
            identification_type=identification_type,
            identification_number="16789456",
            defaults={
                "party_type": Party.PartyType.NATURAL,
                "first_name": "Pedro",
                "last_name": "Ramírez",
                "display_name": "Pedro Ramírez (Maestro Cerrajería)",
            },
        )
        prov2, _ = ProviderProfile.objects.get_or_create(
            party=party_prov2,
            defaults={"provider_kind": ProviderProfile.ProviderKind.CONTRACTOR}
        )

        # Properties
        property_type = PropertyType.objects.get(code="APARTMENT")
        country = Country.objects.get(code="CO")
        department = Department.objects.get(code="CO-VAC")
        city = City.objects.get(code="CO-VAC-CALI")
        neighborhood = Neighborhood.objects.get(code="TEQUENDAMA")

        property_obj1, _ = Property.objects.get_or_create(
            internal_code="INM-DEMO-001",
            defaults={
                "property_type": property_type,
                "address_line": "Calle 5 #38-21",
                "unit_number": "Apto 502",
                "country": country,
                "department": department,
                "city": city,
                "neighborhood": neighborhood,
                "stratum": 5,
                "private_area": Decimal("78.00"),
                "bedrooms": 2,
                "bathrooms": 2,
            },
        )
        PropertyOwnership.objects.get_or_create(
            property=property_obj1,
            owner=owner,
            valid_from=date(2026, 1, 1),
            defaults={"ownership_percentage": Decimal("100.0000"), "is_primary": True},
        )
        RentalListing.objects.get_or_create(
            property=property_obj1,
            status=RentalListing.Status.AVAILABLE,
            defaults={"asking_rent": Decimal("1450000.00"), "available_from": date(2026, 1, 1)},
        )

        property_obj2, _ = Property.objects.get_or_create(
            internal_code="INM-DEMO-002",
            defaults={
                "property_type": property_type,
                "address_line": "Av. 6N #23-45",
                "unit_number": "Oficina 301",
                "country": country,
                "department": department,
                "city": city,
                "neighborhood": neighborhood,
                "stratum": 6,
                "private_area": Decimal("110.00"),
                "bedrooms": 3,
                "bathrooms": 2,
            },
        )
        PropertyOwnership.objects.get_or_create(
            property=property_obj2,
            owner=owner,
            valid_from=date(2026, 1, 1),
            defaults={"ownership_percentage": Decimal("100.0000"), "is_primary": True},
        )

        # Demo Repair Order
        category, _ = RepairCategory.objects.get_or_create(code="PLUMBING", defaults={"name": "Plomería"})
        
        incident, _ = RepairIncident.objects.get_or_create(
            title="Filtración en tubería del baño principal",
            defaults={
                "property": property_obj1,
                "description": "Humedad en techo proveniente del baño superior",
                "category": category,
                "priority": RepairPriority.CRITICAL,
                "severity": RepairSeverity.HIGH,
                "repair_type": RepairType.CORRECTIVE,
            }
        )

        RepairOrder.objects.get_or_create(
            order_number="OT-2026-0089",
            defaults={
                "incident": incident,
                "property": property_obj1,
                "title": "Filtración en tubería del baño principal",
                "description": "Se evidencia humedad activa en el techo del apartamento 402.",
                "category": category,
                "priority": RepairPriority.CRITICAL,
                "severity": RepairSeverity.HIGH,
                "repair_type": RepairType.CORRECTIVE,
                "status": "PENDING_APPROVAL",
                "current_provider": prov1,
            }
        )

        self.stdout.write(self.style.SUCCESS("Datos de demostración cargados."))
