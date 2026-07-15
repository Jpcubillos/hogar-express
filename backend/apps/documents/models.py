import hashlib
import os
import uuid

from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

from apps.catalogs.models import DocumentType, PhotoTag, PropertyType
from apps.core.models import ArchivableModel, DomainModel


def stored_file_upload_path(instance, filename):
    extension = os.path.splitext(filename)[1].lower()
    now = timezone.now()
    return f"documents/{now:%Y/%m}/{uuid.uuid4()}{extension}"


class StoredFile(DomainModel):
    class UploadStatus(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        AVAILABLE = "AVAILABLE", "Disponible"
        FAILED = "FAILED", "Fallido"

    class ScanStatus(models.TextChoices):
        NOT_SCANNED = "NOT_SCANNED", "No analizado"
        CLEAN = "CLEAN", "Limpio"
        REJECTED = "REJECTED", "Rechazado"

    file = models.FileField(upload_to=stored_file_upload_path)
    original_name = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=150)
    extension = models.CharField(max_length=20)
    size = models.PositiveBigIntegerField()
    sha256_checksum = models.CharField(max_length=64, db_index=True)
    upload_status = models.CharField(max_length=12, choices=UploadStatus.choices, default=UploadStatus.AVAILABLE)
    security_scan_status = models.CharField(
        max_length=12, choices=ScanStatus.choices, default=ScanStatus.NOT_SCANNED
    )
    uploaded_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, related_name="stored_files")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def calculate_checksum(self):
        sha256 = hashlib.sha256()
        self.file.seek(0)
        for chunk in self.file.chunks():
            sha256.update(chunk)
        self.file.seek(0)
        return sha256.hexdigest()


class Document(ArchivableModel):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Activo"
        EXPIRED = "EXPIRED", "Vencido"
        REPLACED = "REPLACED", "Reemplazado"
        ARCHIVED = "ARCHIVED", "Archivado"

    class Confidentiality(models.TextChoices):
        INTERNAL = "INTERNAL", "Interno"
        RESTRICTED = "RESTRICTED", "Restringido"
        FINANCIAL = "FINANCIAL", "Financiero"

    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT, related_name="documents")
    visible_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    document_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True, db_index=True)
    confidentiality = models.CharField(
        max_length=12, choices=Confidentiality.choices, default=Confidentiality.INTERNAL
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE, db_index=True)
    is_required = models.BooleanField(default=False)
    current_version = models.ForeignKey(
        "DocumentVersion", on_delete=models.SET_NULL, null=True, blank=True, related_name="current_for_documents"
    )

    class Meta:
        ordering = ["-created_at"]

    @property
    def name(self):
        return self.visible_name

    def __str__(self):
        return self.visible_name


class DocumentVersion(DomainModel):
    document = models.ForeignKey(Document, on_delete=models.PROTECT, related_name="versions")
    version_number = models.PositiveIntegerField()
    stored_file = models.ForeignKey(StoredFile, on_delete=models.PROTECT, related_name="document_versions")
    change_reason = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["document", "version_number"], name="uq_document_version_number")
        ]
        ordering = ["document", "-version_number"]


class DocumentLink(DomainModel):
    ALLOWED_MODELS = {
        "people.party",
        "owners.owner",
        "owners.powerofattorney",
        "properties.property",
        "properties.propertyinventory",
        "properties.inventoryitem",
        "properties.utilityevent",
        "rentals.rental",
        "rentals.rentalcontract",
        "rentals.rentaltermination",
        "payments.chargeadjustment",
        "payments.payment",
        "payments.receipt",
        "payments.ownersettlement",
        "payments.ownerdisbursement",
        "guarantors.guaranteecase",
        "repairs.propertyissue",
        "repairs.repairorder",
        "repairs.repairquote",
        "repairs.repaircost",
        "repairs.repairapproval",
        "sales.salelisting",
        "sales.saletransaction",
    }
    document = models.ForeignKey(Document, on_delete=models.PROTECT, related_name="links")
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.UUIDField(db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")
    relation_type = models.CharField(max_length=50, default="ATTACHMENT")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["document", "content_type", "object_id", "relation_type"], name="uq_document_entity_link"
            )
        ]
        indexes = [models.Index(fields=["content_type", "object_id"])]

    def clean(self):
        natural_key = f"{self.content_type.app_label}.{self.content_type.model}"
        if natural_key not in self.ALLOWED_MODELS:
            raise ValidationError({"content_type": "Este tipo de entidad no admite documentos."})
        if self.content_object is None:
            raise ValidationError({"object_id": "La entidad asociada no existe."})


class PhotoMetadata(DomainModel):
    class EvidencePhase(models.TextChoices):
        BEFORE = "BEFORE", "Antes"
        DURING = "DURING", "Durante"
        AFTER = "AFTER", "Después"
        GENERAL = "GENERAL", "General"

    document = models.OneToOneField(Document, on_delete=models.PROTECT, related_name="photo_metadata")
    photo_tag = models.ForeignKey(PhotoTag, on_delete=models.PROTECT, related_name="photos")
    caption = models.CharField(max_length=255, blank=True)
    taken_at = models.DateTimeField(null=True, blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    is_cover = models.BooleanField(default=False)
    evidence_phase = models.CharField(max_length=10, choices=EvidencePhase.choices, default=EvidencePhase.GENERAL)


class DocumentRequirement(ArchivableModel):
    class Scope(models.TextChoices):
        PARTY = "PARTY", "Persona"
        OWNER = "OWNER", "Propietario"
        PROPERTY = "PROPERTY", "Inmueble"
        RENTAL = "RENTAL", "Alquiler"
        SALE = "SALE", "Venta"
        REPAIR = "REPAIR", "Reparación"

    scope = models.CharField(max_length=10, choices=Scope.choices)
    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT, related_name="requirements")
    property_type = models.ForeignKey(PropertyType, on_delete=models.PROTECT, null=True, blank=True)
    required_stage = models.CharField(max_length=50, blank=True)
    valid_from = models.DateField()
    valid_to = models.DateField(null=True, blank=True)
    is_required = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["scope", "document_type", "property_type", "required_stage", "valid_from"],
                name="uq_document_requirement_version",
            )
        ]
