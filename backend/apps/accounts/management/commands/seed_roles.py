from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from apps.accounts.models import User

class Command(BaseCommand):
    help = 'Idempotently seeds groups/roles and permissions for Hogar Express'

    def handle(self, *args, **options):
        # We need a ContentType to bind custom permissions to.
        # We'll use the accounts.User ContentType or core ContentType.
        user_ct = ContentType.objects.get_for_model(User)
        
        # 1. Define custom permissions
        custom_permissions = [
            # Repairs
            ('view_repair', 'Can view repairs', user_ct),
            ('add_repair', 'Can add repairs', user_ct),
            ('change_repair', 'Can change repairs', user_ct),
            ('approve_repair', 'Can approve repairs', user_ct),
            ('close_repair', 'Can close repairs', user_ct),
            ('apply_financial_charge', 'Can apply financial charge for repairs', user_ct),
            # Reports
            ('view_operational_reports', 'Can view operational reports', user_ct),
            ('view_financial_reports', 'Can view financial reports', user_ct),
            ('export_reports', 'Can export reports', user_ct),
            # Documents
            ('view_private_document', 'Can view private documents', user_ct),
            ('upload_document', 'Can upload documents', user_ct),
            ('change_document', 'Can edit documents metadata', user_ct),
            ('archive_document', 'Can archive documents', user_ct),
            # Accounts
            ('manage_users', 'Can manage users', user_ct),
            ('manage_roles', 'Can manage roles and permissions', user_ct),
            # Sales
            ('view_sales', 'Can view sales modules', user_ct),
            ('manage_sales', 'Can manage sales transactions', user_ct),
            # Owners
            ('view_owner', 'Can view owners', user_ct),
            ('manage_owner', 'Can manage owners', user_ct),
            # Properties
            ('view_property', 'Can view properties', user_ct),
            ('manage_property', 'Can manage properties', user_ct),
            # People (Arrendatarios, Codeudores, Apoderados)
            ('view_people', 'Can view related people', user_ct),
            ('manage_people', 'Can manage related people', user_ct),
            # Rentals & Contratos
            ('view_rental', 'Can view rentals and contracts', user_ct),
            ('manage_rental', 'Can manage rentals and contracts', user_ct),
            # Payments
            ('view_payment', 'Can view payments', user_ct),
            ('manage_payment', 'Can manage payments', user_ct),
        ]

        # Idempotently create permissions
        permissions_dict = {}
        for codename, name, ct in custom_permissions:
            perm, created = Permission.objects.get_or_create(
                codename=codename,
                content_type=ct,
                defaults={'name': name}
            )
            permissions_dict[codename] = perm
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created permission: {codename}"))

        # 2. Define Groups and their specific permissions
        groups_config = {
            'Administrador': {
                'permissions': list(permissions_dict.keys()), # Full access
            },
            'Asesor Interno': {
                'permissions': [
                    'view_owner', 'manage_owner',
                    'view_property', 'manage_property',
                    'view_people', 'manage_people',
                    'view_rental', 'manage_rental',
                    'view_payment', 'manage_payment',
                    'view_repair', 'add_repair', 'change_repair',
                    'view_private_document', 'upload_document', 'change_document', 'archive_document',
                    'view_operational_reports', 'export_reports'
                ]
            },
            'Asesor Externo': {
                'permissions': [
                    'view_property',  # Can query available properties for sale
                    'view_sales', 'manage_sales',  # Limited to sales
                    'view_operational_reports'
                ]
            },
            'Consulta': {
                'permissions': [
                    'view_owner', 'view_property', 'view_people', 'view_rental',
                    'view_payment', 'view_repair', 'view_private_document',
                    'view_operational_reports'
                ]
            }
        }

        # Idempotently create groups and assign permissions
        for group_name, config in groups_config.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created group: {group_name}"))
            
            # Get permissions for this group
            perms_to_set = [permissions_dict[codename] for codename in config['permissions'] if codename in permissions_dict]
            group.permissions.set(perms_to_set)
            self.stdout.write(self.style.SUCCESS(f"Updated permissions for group: {group_name}"))

        self.stdout.write(self.style.SUCCESS("Roles and permissions seeding completed successfully!"))
