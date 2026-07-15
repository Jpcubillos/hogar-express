from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand


PERMISSIONS = [
    ("accounts", "user", "manage_users", "Puede administrar usuarios"),
    ("accounts", "user", "manage_roles", "Puede administrar roles y permisos"),
    ("configuration", "organization", "manage_configuration", "Puede administrar configuración"),
    ("catalogs", "country", "manage_catalogs", "Puede administrar catálogos"),
    ("owners", "owner", "view_owner_business", "Puede consultar propietarios"),
    ("owners", "owner", "manage_owner", "Puede administrar propietarios"),
    ("properties", "property", "view_property_business", "Puede consultar inmuebles"),
    ("properties", "property", "manage_property", "Puede administrar inmuebles"),
    ("people", "party", "view_people", "Puede consultar personas"),
    ("people", "party", "manage_people", "Puede administrar personas"),
    ("rentals", "rental", "view_rental_business", "Puede consultar alquileres"),
    ("rentals", "rental", "manage_rental", "Puede administrar alquileres"),
    ("payments", "payment", "view_payment_business", "Puede consultar pagos"),
    ("payments", "payment", "manage_payment", "Puede registrar y administrar pagos"),
    ("payments", "receipt", "generate_receipt", "Puede generar recibos"),
    ("payments", "receipt", "void_receipt", "Puede anular recibos"),
    ("payments", "ownersettlement", "manage_owner_settlement", "Puede gestionar recaudo propietario"),
    ("documents", "document", "view_private_document", "Puede ver documentos privados"),
    ("documents", "document", "upload_document", "Puede cargar documentos"),
    ("documents", "document", "change_document_metadata", "Puede editar metadatos"),
    ("documents", "document", "archive_document", "Puede archivar documentos"),
    ("repairs", "repairorder", "view_repair_business", "Puede consultar reparaciones"),
    ("repairs", "repairorder", "manage_repair", "Puede administrar reparaciones"),
    ("repairs", "repairorder", "approve_repair", "Puede aprobar reparaciones"),
    ("repairs", "repairorder", "close_repair", "Puede cerrar reparaciones"),
    ("repairs", "repairorder", "apply_financial_charge", "Puede aplicar costos de reparación"),
    ("sales", "salelisting", "view_sales", "Puede consultar ventas"),
    ("sales", "salelisting", "manage_sales", "Puede administrar ventas"),
    ("reports", "reportdefinition", "view_operational_reports", "Puede consultar reportes operativos"),
    ("reports", "reportdefinition", "view_financial_reports", "Puede consultar reportes financieros"),
    ("reports", "reportdefinition", "export_reports", "Puede exportar reportes"),
    ("audit", "auditevent", "view_audit", "Puede consultar auditoría"),
]

DEFAULT_ACCESS = {
    "Asesor Interno": {
        "owners": {"view", "add", "change"},
        "properties": {"view", "add", "change"},
        "people": {"view", "add", "change"},
        "rentals": {"view", "add", "change"},
        "payments": {"view", "add", "change"},
        "documents": {"view", "add", "change"},
        "repairs": {"view", "add", "change"},
        "reports": {"view", "add"},
        "guarantors": {"view", "add", "change"},
    },
    "Asesor Externo": {
        "properties": {"view"},
        "sales": {"view", "add", "change"},
        "documents": {"view", "add"},
        "reports": {"view"},
    },
    "Consulta": {
        "owners": {"view"},
        "properties": {"view"},
        "people": {"view"},
        "rentals": {"view"},
        "payments": {"view"},
        "documents": {"view"},
        "repairs": {"view"},
        "reports": {"view"},
        "guarantors": {"view"},
    },
}


class Command(BaseCommand):
    help = "Crea o actualiza roles y permisos del sistema"

    def handle(self, *args, **options):
        permission_map = {}
        for app_label, model, codename, name in PERMISSIONS:
            content_type = ContentType.objects.get(app_label=app_label, model=model)
            permission, _ = Permission.objects.update_or_create(
                content_type=content_type, codename=codename, defaults={"name": name}
            )
            permission_map[codename] = permission

        groups = {
            "Asesor Interno": {
                "view_owner_business", "manage_owner", "view_property_business", "manage_property",
                "view_people", "manage_people", "view_rental_business", "manage_rental",
                "view_payment_business", "manage_payment", "generate_receipt", "manage_owner_settlement",
                "view_private_document", "upload_document", "change_document_metadata", "archive_document",
                "view_repair_business", "manage_repair", "view_operational_reports", "export_reports",
            },
            "Asesor Externo": {"view_property_business", "view_sales", "manage_sales", "view_operational_reports"},
            "Consulta": {"view_owner_business", "view_property_business", "view_people", "view_rental_business",
                         "view_payment_business", "view_repair_business", "view_operational_reports"},
        }
        administrator, _ = Group.objects.get_or_create(name="Administrador")
        administrator.permissions.set(Permission.objects.all())
        for group_name, codenames in groups.items():
            group, _ = Group.objects.get_or_create(name=group_name)
            granted = {permission_map[codename] for codename in codenames}
            for app_label, actions in DEFAULT_ACCESS[group_name].items():
                for permission in Permission.objects.filter(content_type__app_label=app_label):
                    action = permission.codename.split("_", 1)[0]
                    if action in actions:
                        granted.add(permission)
            group.permissions.set(granted)
        self.stdout.write(self.style.SUCCESS("Roles y permisos actualizados."))
