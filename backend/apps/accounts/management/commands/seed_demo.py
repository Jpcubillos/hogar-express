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
from apps.sales.models import SaleListing
from apps.repairs.models import RepairOrder, RepairIncident, RepairPriority, RepairSeverity, RepairType


class Command(BaseCommand):
    help = "Carga los 10 inmuebles ficticios específicos para desarrollo"

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

        id_type_cc = IdentificationType.objects.get(code="CC")
        id_type_nit = IdentificationType.objects.get(code="NIT")

        # 1. Propietarios Específicos
        p_maria, _ = Party.objects.get_or_create(
            identification_type=id_type_cc, identification_number="31452778",
            defaults={"party_type": Party.PartyType.NATURAL, "first_name": "María", "last_name": "Elena", "display_name": "María Elena"}
        )
        owner_maria, _ = Owner.objects.get_or_create(party=p_maria, defaults={"internal_code": "PROP-001"})

        p_jorge, _ = Party.objects.get_or_create(
            identification_type=id_type_cc, identification_number="16789452",
            defaults={"party_type": Party.PartyType.NATURAL, "first_name": "Jorge", "last_name": "Iván", "display_name": "Jorge Iván"}
        )
        owner_jorge, _ = Owner.objects.get_or_create(party=p_jorge, defaults={"internal_code": "PROP-002"})

        p_canasgordas, _ = Party.objects.get_or_create(
            identification_type=id_type_nit, identification_number="900876543",
            defaults={"party_type": Party.PartyType.LEGAL, "business_name": "Inversiones Cañasgordas", "display_name": "Inversiones Cañasgordas"}
        )
        owner_canasgordas, _ = Owner.objects.get_or_create(party=p_canasgordas, defaults={"internal_code": "PROP-003"})

        p_luz, _ = Party.objects.get_or_create(
            identification_type=id_type_cc, identification_number="38901234",
            defaults={"party_type": Party.PartyType.NATURAL, "first_name": "Luz", "last_name": "Dary", "display_name": "Luz Dary"}
        )
        owner_luz, _ = Owner.objects.get_or_create(party=p_luz, defaults={"internal_code": "PROP-004"})

        # Proveedores de Mantenimiento
        party_prov1, _ = Party.objects.get_or_create(
            identification_type=id_type_nit, identification_number="900123456",
            defaults={"party_type": Party.PartyType.LEGAL, "business_name": "Servicios Hidráulicos Cali S.A.S", "display_name": "Servicios Hidráulicos Cali S.A.S"}
        )
        prov1, _ = ProviderProfile.objects.get_or_create(party=party_prov1, defaults={"provider_kind": ProviderProfile.ProviderKind.COMPANY})

        # Tipos de Inmuebles
        apt_type = PropertyType.objects.get(code="APARTMENT")
        house_type, _ = PropertyType.objects.get_or_create(code="HOUSE", defaults={"name": "Casa Residencia"})
        office_type, _ = PropertyType.objects.get_or_create(code="OFFICE", defaults={"name": "Oficina Comercial"})
        commercial_type, _ = PropertyType.objects.get_or_create(code="COMMERCIAL", defaults={"name": "Local Comercial"})
        warehouse_type, _ = PropertyType.objects.get_or_create(code="WAREHOUSE", defaults={"name": "Bodega Industrial"})

        country = Country.objects.get(code="CO")
        department = Department.objects.get(code="CO-VAC")
        city = City.objects.get(code="CO-VAC-CALI")

        # Barrios
        n_tequendama = Neighborhood.objects.get(code="TEQUENDAMA")
        n_granada, _ = Neighborhood.objects.get_or_create(code="GRANADA", defaults={"name": "Granada", "city": city})
        n_ciudad_jardin, _ = Neighborhood.objects.get_or_create(code="CIUDAD_JARDIN", defaults={"name": "Ciudad Jardín", "city": city})
        n_el_ingenio, _ = Neighborhood.objects.get_or_create(code="EL_INGENIO", defaults={"name": "El Ingenio", "city": city})
        n_san_fernando, _ = Neighborhood.objects.get_or_create(code="SAN_FERNANDO", defaults={"name": "San Fernando", "city": city})
        n_acopi, _ = Neighborhood.objects.get_or_create(code="ACOPI", defaults={"name": "Acopi", "city": city})
        n_limonar, _ = Neighborhood.objects.get_or_create(code="LIMONAR", defaults={"name": "Limonar", "city": city})
        n_pance, _ = Neighborhood.objects.get_or_create(code="PANCE", defaults={"name": "Pance", "city": city})

        # Lista exacta de los 10 inmuebles solicitados por el usuario
        items = [
            ("INM-001", "Calle 5 #38-21", "Apto 502", apt_type, n_tequendama, 5, owner_maria, RentalListing.Status.LEASED, Decimal("1450000.00"), None),
            ("INM-002", "Av. 6N #23-45", "", commercial_type, n_granada, 6, owner_maria, RentalListing.Status.LEASED, Decimal("2100000.00"), None),
            ("INM-003", "Cra 100 #14-32", "Torre 3 Apto 801", apt_type, n_ciudad_jardin, 6, owner_maria, RentalListing.Status.AVAILABLE, Decimal("2300000.00"), None),
            ("INM-004", "Calle 13 #45-67", "", house_type, n_el_ingenio, 5, owner_jorge, RentalListing.Status.LEASED, Decimal("1850000.00"), None),
            ("INM-005", "Torre Empresarial Sur", "Of. 304", office_type, n_san_fernando, 6, owner_canasgordas, RentalListing.Status.LEASED, Decimal("1980000.00"), None),
            ("INM-006", "Torre Empresarial Sur", "Of. 305", office_type, n_san_fernando, 6, owner_canasgordas, RentalListing.Status.LEASED, Decimal("1980000.00"), None),
            ("INM-007", "Zona Industrial Acopi", "Bodega 12", warehouse_type, n_acopi, 4, owner_canasgordas, RentalListing.Status.LEASED, Decimal("4200000.00"), None),
            ("INM-008", "Cra 70 #5-12", "Apto 201", apt_type, n_limonar, 5, owner_canasgordas, RentalListing.Status.PAUSED, Decimal("1750000.00"), None),
            ("INM-009", "Cra 70 #5-12", "Apto 202", apt_type, n_limonar, 5, owner_canasgordas, RentalListing.Status.LEASED, Decimal("1750000.00"), None),
            ("INM-010", "Calle 25 #88-14", "", house_type, n_pance, 6, owner_luz, None, None, Decimal("360000000.00")),
        ]

        for code, addr, unit, ptype, neigh, strat, owner_obj, rent_status, rent_price, sale_price in items:
            prop, _ = Property.objects.get_or_create(
                internal_code=code,
                defaults={
                    "property_type": ptype,
                    "address_line": addr,
                    "unit_number": unit,
                    "country": country,
                    "department": department,
                    "city": city,
                    "neighborhood": neigh,
                    "stratum": strat,
                    "private_area": Decimal("90.00"),
                    "bedrooms": 3 if ptype in [apt_type, house_type] else 0,
                    "bathrooms": 2,
                }
            )
            PropertyOwnership.objects.get_or_create(
                property=prop,
                owner=owner_obj,
                valid_from=date(2026, 1, 1),
                defaults={"ownership_percentage": Decimal("100.0000"), "is_primary": True}
            )

            if rent_status and rent_price:
                RentalListing.objects.get_or_create(
                    property=prop,
                    defaults={"status": rent_status, "asking_rent": rent_price, "available_from": date(2026, 1, 1)}
                )

            if sale_price:
                SaleListing.objects.get_or_create(
                    property=prop,
                    defaults={
                        "status": SaleListing.Status.AVAILABLE,
                        "minimum_price": sale_price,
                        "maximum_price": sale_price
                    }
                )

        # Crear Reparaciones de Ejemplo asociadas
        category_plumb, _ = RepairCategory.objects.get_or_create(code="PLUMBING", defaults={"name": "Plomería"})
        p_arreglo = Property.objects.get(internal_code="INM-008")

        inc, _ = RepairIncident.objects.get_or_create(
            title="Mantenimiento y arreglo integral de baños",
            defaults={"property": p_arreglo, "description": "Fuga de agua y cambio de grifería en Apto 201", "category": category_plumb, "priority": RepairPriority.HIGH, "severity": RepairSeverity.MEDIUM, "repair_type": RepairType.CORRECTIVE}
        )
        RepairOrder.objects.get_or_create(
            order_number="OT-2026-0088",
            defaults={"incident": inc, "property": p_arreglo, "title": "Mantenimiento y arreglo integral de baños", "description": "En reparación activa por humedades.", "category": category_plumb, "priority": RepairPriority.HIGH, "severity": RepairSeverity.MEDIUM, "repair_type": RepairType.CORRECTIVE, "status": "IN_PROGRESS", "current_provider": prov1}
        )

        self.stdout.write(self.style.SUCCESS("Los 10 inmuebles específicos fueron cargados correctamente."))
