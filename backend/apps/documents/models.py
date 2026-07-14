import uuid
import os
import hashlib
from django.db import models
from django.conf import settings
from apps.catalogs.models import DocumentType

def document_upload_path(instance, filename):
    """
    Generates a secure path with UUID: documents/{entity_type}/{year}/{month}/{uuid}.{extension}
    """
    ext = filename.split('.')[-1].lower() if '.' in filename else ''
    entity_type = instance.entity_type or 'general'
    # Use timezone-aware date or datetime.date
    from django.utils import timezone
    now = timezone.now()
    year = now.strftime('%Y')
    month = now.strftime('%m')
    unique_id = uuid.uuid4()
    new_filename = f"{unique_id}.{ext}" if ext else f"{unique_id}"
    return os.path.join('documents', entity_type, year, month, new_filename)


class Document(models.Model):
    """
    Metadata representation of uploaded documents. The binary file is saved outside Postgres.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, verbose_name="Nombre visible")
    original_name = models.CharField(max_length=255, verbose_name="Nombre original")
    file = models.FileField(upload_to=document_upload_path, verbose_name="Archivo")
    
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Tipo de documento"
    )
    tag = models.CharField(max_length=100, null=True, blank=True, verbose_name="Etiqueta")
    description = models.TextField(null=True, blank=True, verbose_name="Descripción")
    
    mime_type = models.CharField(max_length=100, verbose_name="MIME Type")
    extension = models.CharField(max_length=20, verbose_name="Extensión")
    size = models.BigIntegerField(verbose_name="Tamaño (bytes)")
    checksum = models.CharField(max_length=64, verbose_name="Checksum SHA-256")
    
    document_date = models.DateField(null=True, blank=True, verbose_name="Fecha del documento")
    expiration_date = models.DateField(null=True, blank=True, verbose_name="Fecha de vencimiento")
    is_required = models.BooleanField(default=False, verbose_name="Obligatorio")
    
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Cargado por"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de carga")
    is_archived = models.BooleanField(default=False, verbose_name="Archivado")
    
    # Generic entity categorization
    entity_type = models.CharField(max_length=100, default='general', verbose_name="Tipo de entidad asociada")
    
    # Optional explicit relations to avoid complexity
    owner = models.ForeignKey('owners.Owner', on_delete=models.CASCADE, null=True, blank=True, related_name='documents')
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, null=True, blank=True, related_name='documents')
    repair = models.ForeignKey('repairs.Repair', on_delete=models.CASCADE, null=True, blank=True, related_name='documents')

    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.name} ({self.extension.upper()})"

    def calculate_checksum(self):
        """
        Calculates SHA-256 checksum of the file.
        """
        sha256 = hashlib.sha256()
        self.file.seek(0)
        for chunk in self.file.chunks():
            sha256.update(chunk)
        return sha256.hexdigest()
