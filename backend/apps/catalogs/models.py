from django.db import models

from apps.core.models import ArchivableModel


class CatalogModel(ArchivableModel):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        abstract = True
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Country(CatalogModel):
    iso_code = models.CharField(max_length=3, unique=True)

    class Meta(CatalogModel.Meta):
        verbose_name = "País"
        verbose_name_plural = "Países"


class Department(CatalogModel):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="departments")

    class Meta(CatalogModel.Meta):
        constraints = [models.UniqueConstraint(fields=["country", "name"], name="uq_department_country_name")]
        verbose_name = "Departamento"


class City(CatalogModel):
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="cities")

    class Meta(CatalogModel.Meta):
        constraints = [models.UniqueConstraint(fields=["department", "name"], name="uq_city_department_name")]
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"

    @property
    def country(self):
        return self.department.country


class Neighborhood(CatalogModel):
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="neighborhoods")

    class Meta(CatalogModel.Meta):
        constraints = [models.UniqueConstraint(fields=["city", "name"], name="uq_neighborhood_city_name")]
        verbose_name = "Barrio"


class Bank(CatalogModel):
    class Meta(CatalogModel.Meta):
        verbose_name = "Banco"


class IdentificationType(CatalogModel):
    applies_to_natural = models.BooleanField(default=True)
    applies_to_legal = models.BooleanField(default=False)

    class Meta(CatalogModel.Meta):
        verbose_name = "Tipo de identificación"


class PropertyType(CatalogModel):
    class Meta(CatalogModel.Meta):
        verbose_name = "Tipo de inmueble"


class DocumentType(CatalogModel):
    allowed_mime_types = models.JSONField(default=list, blank=True)

    class Meta(CatalogModel.Meta):
        verbose_name = "Tipo de documento"


class PhotoTag(CatalogModel):
    class Meta(CatalogModel.Meta):
        verbose_name = "Etiqueta de fotografía"


class InventoryCategory(CatalogModel):
    class Meta(CatalogModel.Meta):
        verbose_name = "Categoría de inventario"


class InventoryConcept(CatalogModel):
    category = models.ForeignKey(InventoryCategory, on_delete=models.PROTECT, related_name="concepts")

    class Meta(CatalogModel.Meta):
        verbose_name = "Concepto de inventario"


class MeasureUnit(CatalogModel):
    symbol = models.CharField(max_length=20, blank=True)

    class Meta(CatalogModel.Meta):
        verbose_name = "Unidad de medida"


class RepairCategory(CatalogModel):
    class Meta(CatalogModel.Meta):
        verbose_name = "Categoría de reparación"


class ProviderSpecialty(CatalogModel):
    class Meta(CatalogModel.Meta):
        verbose_name = "Especialidad de proveedor"


class PaymentMethod(CatalogModel):
    requires_reference = models.BooleanField(default=False)
    is_cash = models.BooleanField(default=False)

    class Meta(CatalogModel.Meta):
        verbose_name = "Método de pago"


class FinancialConcept(CatalogModel):
    class ConceptKind(models.TextChoices):
        INCOME = "INCOME", "Ingreso"
        CHARGE = "CHARGE", "Cargo"
        DEDUCTION = "DEDUCTION", "Deducción"
        ADJUSTMENT = "ADJUSTMENT", "Ajuste"

    kind = models.CharField(max_length=12, choices=ConceptKind.choices)
    owner_visible_by_default = models.BooleanField(default=True)

    class Meta(CatalogModel.Meta):
        verbose_name = "Concepto financiero"


class GuarantorCompany(CatalogModel):
    identification_number = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    class Meta(CatalogModel.Meta):
        verbose_name = "Afianzadora"


class GuaranteeType(CatalogModel):
    class Meta(CatalogModel.Meta):
        verbose_name = "Tipo de fianza"


class UtilityType(CatalogModel):
    class Meta(CatalogModel.Meta):
        verbose_name = "Tipo de servicio público"


class UtilityProvider(CatalogModel):
    utility_types = models.ManyToManyField(UtilityType, blank=True, related_name="providers")

    class Meta(CatalogModel.Meta):
        verbose_name = "Proveedor de servicio público"


# Compatibility with the name used by the foundation API.
GuarantyType = GuaranteeType
