from django.db import models
from apps.core.models import TimeStampedModel, UserStampedModel, SoftDeleteModel
from apps.properties.models import Property
import uuid

class Repair(TimeStampedModel, UserStampedModel, SoftDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="repairs", verbose_name="Inmueble")
    description = models.TextField(verbose_name="Descripción del daño")
    status = models.CharField(max_length=50, default="REPORTADO", verbose_name="Estado de reparación")
    cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.0, verbose_name="Costo total")
    charge_to = models.CharField(max_length=50, default="Propietario", verbose_name="Cargo a")

    class Meta:
        verbose_name = "Reparación"
        verbose_name_plural = "Reparaciones"
        
    def __str__(self):
        return f"Reparación - {self.property} - {self.status}"
