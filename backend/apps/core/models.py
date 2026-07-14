from django.db import models
from django.conf import settings

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created_at`` and ``updated_at`` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        abstract = True


class UserStampedModel(models.Model):
    """
    An abstract base class model that tracks user creation/modification.
    """
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created",
        verbose_name="Creado por"
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated",
        verbose_name="Actualizado por"
    )

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    An abstract base class model that provides archiving capabilities.
    """
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    archived_at = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de archivado")
    archived_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_archived",
        verbose_name="Archivado por"
    )

    class Meta:
        abstract = True


class LegacyMigratableModel(models.Model):
    """
    An abstract base class model for legacy entities migrated from MS Access.
    """
    legacy_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="ID Legado (Access)")
    legacy_source = models.CharField(max_length=100, null=True, blank=True, verbose_name="Origen Legado")

    class Meta:
        abstract = True
