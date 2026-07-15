"""Shared persistence primitives for every Hogar Express domain model."""

import uuid

from django.conf import settings
from django.db import models


class DomainModel(models.Model):
    """UUID, audit stamps, optimistic version and legacy migration metadata."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_updated",
    )
    version = models.PositiveIntegerField(default=1)
    legacy_id = models.CharField(max_length=100, null=True, blank=True, db_index=True)
    legacy_source = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = True


class ArchivableModel(DomainModel):
    """Business records are archived instead of physically deleted."""

    is_active = models.BooleanField(default=True, db_index=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    archived_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_archived",
    )
    archive_reason = models.TextField(blank=True)

    class Meta:
        abstract = True


# Backwards-compatible abstract mixins retained for code written against the
# foundation commit. New models should use DomainModel/ArchivableModel.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserStampedModel(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_legacy_created",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_legacy_updated",
    )

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    is_active = models.BooleanField(default=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    archived_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(app_label)s_%(class)s_legacy_archived",
    )

    class Meta:
        abstract = True


class LegacyMigratableModel(models.Model):
    legacy_id = models.CharField(max_length=100, null=True, blank=True)
    legacy_source = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = True
