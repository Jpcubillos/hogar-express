from django.db import models
from apps.core.models import TimeStampedModel, UserStampedModel, SoftDeleteModel
from apps.owners.models import Owner
import uuid

class Property(TimeStampedModel, UserStampedModel, SoftDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="properties", verbose_name="Propietario")
    property_type = models.CharField(max_length=100, verbose_name="Tipo de inmueble")
    address = models.CharField(max_length=255, verbose_name="Dirección")
    neighborhood = models.CharField(max_length=100, verbose_name="Barrio")
    stratum = models.IntegerField(verbose_name="Estrato")
    area = models.FloatField(verbose_name="Área (m²)")
    rent_value = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor canon")
    admin_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10.0, verbose_name="Porcentaje admin")
    status = models.CharField(max_length=50, default="Disponible", verbose_name="Estado")

    class Meta:
        verbose_name = "Inmueble"
        verbose_name_plural = "Inmuebles"
        
    def __str__(self):
        return f"{self.property_type} - {self.neighborhood} - {self.address}"
