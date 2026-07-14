from django.db import models
from apps.core.models import TimeStampedModel, UserStampedModel, SoftDeleteModel
import uuid

class CatalogModel(TimeStampedModel, UserStampedModel, SoftDeleteModel):
    """
    Base abstract class for all system catalog entities.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, unique=True, verbose_name="Código")
    name = models.CharField(max_length=255, verbose_name="Nombre")
    description = models.TextField(null=True, blank=True, verbose_name="Descripción")
    order = models.IntegerField(default=0, verbose_name="Orden de visualización")

    class Meta:
        abstract = True
        ordering = ['order', 'name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Bank(CatalogModel):
    class Meta(CatalogModel.Meta):
        verbose_name = "Banco"
        verbose_name_plural = "Bancos"


class City(CatalogModel):
    department = models.CharField(max_length=100, default="Valle del Cauca", verbose_name="Departamento")
    country = models.CharField(max_length=100, default="Colombia", verbose_name="País")
    
    class Meta(CatalogModel.Meta):
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"


class Neighborhood(CatalogModel):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="neighborhoods", verbose_name="Ciudad")
    
    class Meta(CatalogModel.Meta):
        verbose_name = "Barrio"
        verbose_name_plural = "Barrios"


class PropertyType(CatalogModel):
    class Meta(CatalogModel.Meta):
        verbose_name = "Tipo de Inmueble"
        verbose_name_plural = "Tipos de Inmueble"


class DocumentType(CatalogModel):
    class Meta(CatalogModel.Meta):
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documento"


class PhotoTag(CatalogModel):
    class Meta(CatalogModel.Meta):
        verbose_name = "Etiqueta de Fotografía"
        verbose_name_plural = "Etiquetas de Fotografía"


class RepairCategory(CatalogModel):
    class Meta(CatalogModel.Meta):
        verbose_name = "Categoría de Reparación"
        verbose_name_plural = "Categorías de Reparación"


class PaymentMethod(CatalogModel):
    class Meta(CatalogModel.Meta):
        verbose_name = "Método de Pago"
        verbose_name_plural = "Métodos de Pago"


class GuarantorCompany(CatalogModel):
    class Meta(CatalogModel.Meta):
        verbose_name = "Afianzadora"
        verbose_name_plural = "Afianzadoras"


class GuarantyType(CatalogModel):
    class Meta(CatalogModel.Meta):
        verbose_name = "Tipo de Fianza"
        verbose_name_plural = "Tipos de Fianza"


class UtilityType(CatalogModel):
    class Meta(CatalogModel.Meta):
        verbose_name = "Tipo de Servicio Público"
        verbose_name_plural = "Tipos de Servicio Público"


class UtilityProvider(CatalogModel):
    class Meta(CatalogModel.Meta):
        verbose_name = "Proveedor de Servicio Público"
        verbose_name_plural = "Proveedores de Servicio Público"
