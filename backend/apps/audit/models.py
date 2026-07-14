from django.db import models
from django.conf import settings
import uuid

class AuditEvent(models.Model):
    """
    Model that records user actions and API request details for audit logging.
    """
    ACTIONS = [
        ('CREATE', 'CREATE'),
        ('UPDATE', 'UPDATE'),
        ('ARCHIVE', 'ARCHIVE'),
        ('RESTORE', 'RESTORE'),
        ('LOGIN', 'LOGIN'),
        ('LOGOUT', 'LOGOUT'),
        ('DOWNLOAD', 'DOWNLOAD'),
        ('EXPORT', 'EXPORT'),
        ('PERMISSION_CHANGE', 'PERMISSION_CHANGE'),
        ('ROLE_CHANGE', 'ROLE_CHANGE'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_events",
        verbose_name="Usuario"
    )
    action = models.CharField(max_length=50, choices=ACTIONS, verbose_name="Acción")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y hora")
    ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="Dirección IP")
    user_agent = models.TextField(null=True, blank=True, verbose_name="User-Agent")
    entity_type = models.CharField(max_length=100, null=True, blank=True, verbose_name="Tipo de entidad")
    record_id = models.CharField(max_length=255, null=True, blank=True, verbose_name="ID del registro")
    prev_data = models.JSONField(null=True, blank=True, verbose_name="Datos anteriores")
    post_data = models.JSONField(null=True, blank=True, verbose_name="Datos posteriores")
    path = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ruta")
    method = models.CharField(max_length=10, null=True, blank=True, verbose_name="Método HTTP")
    result = models.CharField(max_length=50, default='SUCCESS', verbose_name="Resultado")

    class Meta:
        verbose_name = "Evento de Auditoría"
        verbose_name_plural = "Eventos de Auditoría"
        ordering = ['-timestamp']

    def __str__(self):
        user_str = self.user.username if self.user else "Anónimo"
        return f"{self.timestamp} - {user_str} - {self.action} on {self.entity_type or self.path}"
