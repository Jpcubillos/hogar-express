from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from apps.accounts.models import User
from apps.catalogs.models import DocumentType, PropertyType, City, Neighborhood
from apps.owners.models import Owner
from apps.properties.models import Property
from apps.repairs.models import Repair
import decimal

class Command(BaseCommand):
    help = 'Idempotently seeds development demo data for Hogar Express'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando carga de datos demo ficticios...")

        # 1. Seed Cities and Neighborhoods
        cali, _ = City.objects.get_or_create(
            code="CALI",
            defaults={'name': "Cali", 'department': "Valle del Cauca", 'country': "Colombia"}
        )
        
        neighborhoods = ["Tequendama", "Granada", "Ciudad Jardín", "El Ingenio", "San Fernando", "Acopi", "Limonar", "Pance"]
        for nb in neighborhoods:
            Neighborhood.objects.get_or_create(
                code=nb.upper().replace(" ", "_"),
                defaults={'name': nb, 'city': cali}
            )

        # 2. Seed Document Types
        doc_types = ["Cédula", "Certificado Bancario", "Certificado de Tradición", "Escritura", "Contrato PDF"]
        for dt in doc_types:
            DocumentType.objects.get_or_create(
                code=dt.upper().replace(" ", "_"),
                defaults={'name': dt}
            )

        # 3. Create Demo Users for each role
        roles_users = {
            'admin': ('admin@example.test', 'Administrador'),
            'intern': ('intern@example.test', 'Asesor Interno'),
            'extern': ('extern@example.test', 'Asesor Externo'),
            'visitor': ('visitor@example.test', 'Consulta'),
        }

        for username, (email, group_name) in roles_users.items():
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'is_staff': True if group_name == 'Administrador' else False,
                    'is_active': True,
                    'display_name': f"Demo {group_name}"
                }
            )
            if created or not user.check_password('change_me'):
                user.set_password('change_me')
                user.save()
                
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
            self.stdout.write(self.style.SUCCESS(f"User '{username}' linked to group '{group_name}'"))

        # 4. Create Demo Owners
        owner1, _ = Owner.objects.get_or_create(
            identification="CC 31.452.778",
            defaults={
                'name': "María Elena Castaño Ruiz",
                'phone': "315 442 9087",
                'email': "melena.castano@gmail.com",
                'bank_account': "Bancolombia Ahorros - **** 4521"
            }
        )

        owner2, _ = Owner.objects.get_or_create(
            identification="CC 16.789.432",
            defaults={
                'name': "Jorge Iván Salazar Mosquera",
                'phone': "300 781 2244",
                'email': "jisalazar@hotmail.com",
                'bank_account': "Davivienda Corriente - **** 8810"
            }
        )

        # 5. Create Demo Properties
        prop1, _ = Property.objects.get_or_create(
            address="Calle 5 #38-21, Apto 502",
            defaults={
                'owner': owner1,
                'property_type': "Apartamento",
                'neighborhood': "Tequendama",
                'stratum': 5,
                'area': 78.0,
                'rent_value': decimal.Decimal('1450000.00'),
                'admin_percentage': decimal.Decimal('10.00'),
                'status': "Arrendado"
            }
        )

        prop2, _ = Property.objects.get_or_create(
            address="Cra 100 #14-32, Torre 3 Apto 801",
            defaults={
                'owner': owner1,
                'property_type': "Apartamento",
                'neighborhood': "Ciudad Jardín",
                'stratum': 6,
                'area': 95.0,
                'rent_value': decimal.Decimal('2300000.00'),
                'admin_percentage': decimal.Decimal('10.00'),
                'status': "Disponible"
            }
        )

        # 6. Create Demo Repair order
        Repair.objects.get_or_create(
            property=prop2,
            description="Mantenimiento preventivo antes de nueva entrega",
            defaults={
                'status': "TERMINADO",
                'cost': decimal.Decimal('320000.00'),
                'charge_to': "Propietario"
            }
        )

        self.stdout.write(self.style.SUCCESS("¡Carga de datos demo completada con éxito!"))
