from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.catalogs import models
from apps.configuration.models import AdministrationFeePlan, NumberSequence, Office, Organization
from apps.documents.models import DocumentRequirement


class Command(BaseCommand):
    help = "Crea o actualiza catálogos, organización y configuración inicial"

    @staticmethod
    def catalog(model, code, name, **defaults):
        return model.objects.update_or_create(code=code, defaults={"name": name, "is_active": True, **defaults})[0]

    def handle(self, *args, **options):
        colombia = self.catalog(models.Country, "CO", "Colombia", iso_code="COL")
        valle = self.catalog(models.Department, "CO-VAC", "Valle del Cauca", country=colombia)
        cali = self.catalog(models.City, "CO-VAC-CALI", "Cali", department=valle)
        for code, name in [
            ("TEQUENDAMA", "Tequendama"),
            ("GRANADA", "Granada"),
            ("CIUDAD_JARDIN", "Ciudad Jardín"),
            ("EL_INGENIO", "El Ingenio"),
            ("SAN_FERNANDO", "San Fernando"),
            ("LIMONAR", "Limonar"),
            ("PANCE", "Pance"),
        ]:
            self.catalog(models.Neighborhood, code, name, city=cali)

        for code, name, natural, legal in [
            ("CC", "Cédula de ciudadanía", True, False),
            ("CE", "Cédula de extranjería", True, False),
            ("PASSPORT", "Pasaporte", True, False),
            ("NIT", "NIT", False, True),
        ]:
            self.catalog(
                models.IdentificationType,
                code,
                name,
                applies_to_natural=natural,
                applies_to_legal=legal,
            )

        for code, name in [
            ("APARTMENT", "Apartamento"),
            ("STUDIO", "Apartaestudio"),
            ("HOUSE", "Casa"),
            ("COMMERCIAL", "Local"),
            ("AIRBNB", "Airbnb"),
            ("LOT", "Lote"),
            ("FARM", "Finca"),
        ]:
            self.catalog(models.PropertyType, code, name)

        document_types = {}
        for code, name in [
            ("ID", "Documento de identidad"),
            ("TRADITION", "Certificado de tradición"),
            ("UTILITY_BILL", "Factura de servicio público"),
            ("MANDATE", "Contrato de mandato"),
            ("MEGAOBRAS", "Paz y salvo de megaobras"),
            ("CONTRACT", "Contrato"),
            ("QUOTE", "Cotización"),
            ("INVOICE", "Factura"),
            ("PAYMENT_SUPPORT", "Soporte de pago"),
            ("PHOTO", "Fotografía"),
        ]:
            document_types[code] = self.catalog(models.DocumentType, code, name)

        for code, name in [
            ("FACADE", "Fachada"), ("LIVING_ROOM", "Sala"), ("KITCHEN", "Cocina"),
            ("BEDROOM", "Habitación"), ("BATHROOM", "Baño"), ("METER", "Contador"),
            ("DAMAGE", "Daño"), ("BEFORE", "Antes"), ("DURING", "Durante"), ("AFTER", "Después"),
        ]:
            self.catalog(models.PhotoTag, code, name)

        general_inventory = self.catalog(models.InventoryCategory, "GENERAL", "Inventario general")
        for code, name in [
            ("OUTLET", "Toma eléctrica"), ("SWITCH", "Interruptor"), ("DOOR", "Puerta"),
            ("WINDOW", "Ventana"), ("KEY", "Llave"), ("LIGHT", "Luminaria"),
        ]:
            self.catalog(models.InventoryConcept, code, name, category=general_inventory)
        self.catalog(models.MeasureUnit, "UNIT", "Unidad", symbol="ud")

        for code, name in [
            ("PLUMBING", "Plomería"), ("ELECTRICAL", "Electricidad"), ("PAINT", "Pintura"),
            ("GAS", "Gas"), ("CARPENTRY", "Carpintería"), ("GENERAL", "General"),
        ]:
            self.catalog(models.RepairCategory, code, name)
            self.catalog(models.ProviderSpecialty, code, name)

        for code, name, is_cash, requires_reference in [
            ("CASH", "Efectivo", True, False),
            ("TRANSFER", "Transferencia", False, True),
            ("DEPOSIT", "Consignación", False, True),
            ("CARD", "Tarjeta", False, True),
        ]:
            self.catalog(
                models.PaymentMethod,
                code,
                name,
                is_cash=is_cash,
                requires_reference=requires_reference,
            )

        for code, name, kind in [
            ("RENT", "Canon de arrendamiento", "INCOME"),
            ("ADMIN_FEE", "Administración inmobiliaria", "DEDUCTION"),
            ("LATE_FEE", "Interés por mora", "CHARGE"),
            ("REPAIR", "Reparación", "CHARGE"),
            ("UTILITY", "Servicio público", "CHARGE"),
            ("DISCOUNT", "Descuento", "ADJUSTMENT"),
            ("OTHER", "Otro concepto", "ADJUSTMENT"),
        ]:
            self.catalog(models.FinancialConcept, code, name, kind=kind)

        for code, name in [("WATER", "Agua"), ("ENERGY", "Energía"), ("GAS", "Gas")]:
            self.catalog(models.UtilityType, code, name)
        for code, name in [("EMCALI", "EMCALI"), ("GASES_OCCIDENTE", "Gases de Occidente")]:
            self.catalog(models.UtilityProvider, code, name)

        for code, name in [("BANCOLOMBIA", "Bancolombia"), ("DAVIVIENDA", "Davivienda"),
                           ("BANCO_BOGOTA", "Banco de Bogotá"), ("BANCO_OCCIDENTE", "Banco de Occidente")]:
            self.catalog(models.Bank, code, name)

        organization, _ = Organization.objects.update_or_create(
            identification_number="DEMO-HE",
            defaults={"legal_name": "Hogar Express", "trade_name": "Hogar Express", "is_active": True},
        )
        office, _ = Office.objects.update_or_create(
            organization=organization,
            code="MAIN",
            defaults={"name": "Oficina principal", "is_main": True, "is_active": True},
        )
        for kind, prefix in [("TENANT", "RA"), ("OWNER_SETTLEMENT", "RP"), ("OWNER_CASH", "RC"),
                             ("PROVIDER", "PR"), ("REPAIR_ORDER", "OT")]:
            NumberSequence.objects.get_or_create(
                organization=organization,
                office=office,
                document_kind=kind,
                defaults={"prefix": prefix},
            )
        AdministrationFeePlan.objects.get_or_create(
            organization=organization,
            code="STANDARD",
            policy_version=1,
            defaults={
                "name": "Administración estándar",
                "valid_from": date(2026, 1, 1),
                "percentage": Decimal("10.000000"),
                "status": "DRAFT",
            },
        )
        DocumentRequirement.objects.get_or_create(
            scope="OWNER", document_type=document_types["ID"], property_type=None,
            required_stage="CREATE", valid_from=date(2026, 1, 1), defaults={"is_required": True}
        )
        for code in ["TRADITION", "UTILITY_BILL"]:
            DocumentRequirement.objects.get_or_create(
                scope="PROPERTY", document_type=document_types[code], property_type=None,
                required_stage="ACTIVE", valid_from=date(2026, 1, 1), defaults={"is_required": True}
            )
        for code in ["MANDATE", "TRADITION", "MEGAOBRAS", "UTILITY_BILL"]:
            DocumentRequirement.objects.get_or_create(
                scope="SALE", document_type=document_types[code], property_type=None,
                required_stage="AVAILABLE", valid_from=date(2026, 1, 1), defaults={"is_required": True}
            )
        self.stdout.write(self.style.SUCCESS("Catálogos y configuración inicial actualizados."))
