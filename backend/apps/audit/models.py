import uuid

from django.conf import settings
from django.db import models


class AuditEvent(models.Model):
    class Action(models.TextChoices):
        CREATE = "CREATE", "Crear"
        UPDATE = "UPDATE", "Actualizar"
        ARCHIVE = "ARCHIVE", "Archivar"
        RESTORE = "RESTORE", "Restaurar"
        LOGIN = "LOGIN", "Inicio de sesión"
        LOGOUT = "LOGOUT", "Cierre de sesión"
        LOGIN_FAILED = "LOGIN_FAILED", "Inicio fallido"
        DOWNLOAD = "DOWNLOAD", "Descargar"
        EXPORT = "EXPORT", "Exportar"
        PRINT = "PRINT", "Imprimir"
        GENERATE = "GENERATE", "Generar"
        APPROVE = "APPROVE", "Aprobar"
        REJECT = "REJECT", "Rechazar"
        CANCEL = "CANCEL", "Cancelar"
        VOID = "VOID", "Anular"
        REVERSE = "REVERSE", "Reversar"
        STATUS_CHANGE = "STATUS_CHANGE", "Cambiar estado"
        PERMISSION_CHANGE = "PERMISSION_CHANGE", "Cambiar permiso"
        ROLE_CHANGE = "ROLE_CHANGE", "Cambiar rol"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_events"
    )
    action = models.CharField(max_length=50, choices=Action.choices)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    entity_type = models.CharField(max_length=100, blank=True, db_index=True)
    record_id = models.CharField(max_length=255, blank=True, db_index=True)
    prev_data = models.JSONField(null=True, blank=True)
    post_data = models.JSONField(null=True, blank=True)
    path = models.CharField(max_length=255, blank=True)
    method = models.CharField(max_length=10, blank=True)
    result = models.CharField(max_length=50, default="SUCCESS", db_index=True)
    correlation_id = models.UUIDField(null=True, blank=True, db_index=True)
    reason = models.TextField(blank=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Evento de auditoría"
        indexes = [models.Index(fields=["entity_type", "record_id", "-timestamp"])]

    def __str__(self):
        actor = self.user.username if self.user else "Anónimo"
        return f"{self.timestamp} - {actor} - {self.action}"
