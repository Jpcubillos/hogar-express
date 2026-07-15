import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    display_name = models.CharField(max_length=255, blank=True, verbose_name="Nombre visible")
    must_change_password = models.BooleanField(default=False, verbose_name="Debe cambiar contraseña")
    failed_login_attempts = models.PositiveSmallIntegerField(default=0, verbose_name="Intentos fallidos")
    locked_until = models.DateTimeField(null=True, blank=True, verbose_name="Bloqueado hasta")
    last_password_change = models.DateTimeField(null=True, blank=True, verbose_name="Último cambio de contraseña")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = f"{self.first_name} {self.last_name}".strip() or self.username
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} ({self.display_name})"
