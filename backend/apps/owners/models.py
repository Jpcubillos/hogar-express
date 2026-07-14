from django.db import models
from apps.core.models import TimeStampedModel, UserStampedModel, SoftDeleteModel
import uuid

class Owner(TimeStampedModel, UserStampedModel, SoftDeleteModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Nombre completo")
    identification = models.CharField(max_length=50, unique=True, verbose_name="Identificación")
    phone = models.CharField(max_length=50, verbose_name="Teléfono")
    email = models.EmailField(verbose_name="Correo electrónico")
    bank_account = models.CharField(max_length=100, null=True, blank=True, verbose_name="Cuenta bancaria")

    class Meta:
        verbose_name = "Propietario"
        verbose_name_plural = "Propietarios"
        
    def __str__(self):
        return self.name
