from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.core.models import ArchivableModel, DomainModel
from apps.documents.models import Document


class ReportDefinition(ArchivableModel):
    code = models.CharField(max_length=80, unique=True)
    name = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    required_permission = models.CharField(max_length=150)
    available_formats = models.JSONField(default=list)
    filter_schema = models.JSONField(default=dict)
    column_schema = models.JSONField(default=list)
    default_order = models.JSONField(default=list)

    class Meta:
        ordering = ["name"]


class ReportRun(DomainModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        RUNNING = "RUNNING", "Generando"
        COMPLETED = "COMPLETED", "Completado"
        FAILED = "FAILED", "Fallido"
        EXPIRED = "EXPIRED", "Expirado"

    report_definition = models.ForeignKey(ReportDefinition, on_delete=models.PROTECT, related_name="runs")
    requested_by = models.ForeignKey("accounts.User", on_delete=models.PROTECT, related_name="report_runs")
    requested_at = models.DateTimeField(auto_now_add=True, db_index=True)
    filters = models.JSONField(default=dict)
    output_format = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING, db_index=True)
    row_count = models.PositiveIntegerField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    generated_document = models.ForeignKey(Document, on_delete=models.PROTECT, null=True, blank=True)
    checksum = models.CharField(max_length=64, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)


class OperationalAlert(DomainModel):
    class Severity(models.TextChoices):
        INFO = "INFO", "Información"
        WARNING = "WARNING", "Advertencia"
        CRITICAL = "CRITICAL", "Crítica"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Abierta"
        ACKNOWLEDGED = "ACKNOWLEDGED", "Reconocida"
        RESOLVED = "RESOLVED", "Resuelta"
        DISMISSED = "DISMISSED", "Descartada"

    alert_type = models.CharField(max_length=80, db_index=True)
    severity = models.CharField(max_length=10, choices=Severity.choices, default=Severity.INFO)
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.UUIDField(db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")
    title = models.CharField(max_length=180)
    message = models.TextField()
    due_at = models.DateTimeField(null=True, blank=True, db_index=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.OPEN, db_index=True)
    acknowledged_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="acknowledged_alerts"
    )
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["alert_type", "content_type", "object_id"],
                condition=models.Q(status__in=["OPEN", "ACKNOWLEDGED"]),
                name="uq_open_alert_entity_type",
            )
        ]
