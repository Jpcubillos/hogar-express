import hashlib
import mimetypes
import os

from django.conf import settings
from django.db import transaction
from rest_framework import serializers

from apps.documents.models import Document, DocumentVersion, StoredFile


class DocumentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True, required=False)
    original_name = serializers.CharField(source="current_version.stored_file.original_name", read_only=True)
    mime_type = serializers.CharField(source="current_version.stored_file.mime_type", read_only=True)
    extension = serializers.CharField(source="current_version.stored_file.extension", read_only=True)
    size = serializers.IntegerField(source="current_version.stored_file.size", read_only=True)
    version_number = serializers.IntegerField(source="current_version.version_number", read_only=True)

    class Meta:
        model = Document
        fields = [
            "id",
            "visible_name",
            "document_type",
            "description",
            "document_date",
            "expiration_date",
            "confidentiality",
            "status",
            "is_required",
            "file",
            "original_name",
            "mime_type",
            "extension",
            "size",
            "version_number",
            "created_at",
        ]
        read_only_fields = ["id", "status", "created_at"]

    def validate_file(self, value):
        max_size_mb = getattr(settings, "MAX_UPLOAD_SIZE_MB", 10)
        if value.size <= 0:
            raise serializers.ValidationError("El archivo está vacío.")
        if value.size > max_size_mb * 1024 * 1024:
            raise serializers.ValidationError(f"El archivo supera el máximo permitido de {max_size_mb} MB.")
        extension = os.path.splitext(value.name)[1].lower()
        if extension not in {".pdf", ".jpg", ".jpeg", ".png", ".webp"}:
            raise serializers.ValidationError("Tipo de archivo no permitido.")
        return value

    @staticmethod
    def _checksum(upload):
        digest = hashlib.sha256()
        for chunk in upload.chunks():
            digest.update(chunk)
        upload.seek(0)
        return digest.hexdigest()

    @transaction.atomic
    def create(self, validated_data):
        upload = validated_data.pop("file", None)
        if upload is None:
            raise serializers.ValidationError({"file": "Debe adjuntar un archivo."})
        user = self.context["request"].user
        document = Document.objects.create(created_by=user, updated_by=user, **validated_data)
        extension = os.path.splitext(upload.name)[1].lower().lstrip(".")
        stored_file = StoredFile.objects.create(
            file=upload,
            original_name=upload.name,
            mime_type=mimetypes.guess_type(upload.name)[0] or "application/octet-stream",
            extension=extension,
            size=upload.size,
            sha256_checksum=self._checksum(upload),
            uploaded_by=user,
            created_by=user,
            updated_by=user,
        )
        version = DocumentVersion.objects.create(
            document=document,
            version_number=1,
            stored_file=stored_file,
            created_by=user,
            updated_by=user,
        )
        document.current_version = version
        document.save(update_fields=["current_version", "updated_at"])
        return document

    @transaction.atomic
    def update(self, instance, validated_data):
        upload = validated_data.pop("file", None)
        instance = super().update(instance, validated_data)
        if upload is not None:
            user = self.context["request"].user
            next_version = (instance.versions.order_by("-version_number").values_list("version_number", flat=True).first() or 0) + 1
            extension = os.path.splitext(upload.name)[1].lower().lstrip(".")
            stored_file = StoredFile.objects.create(
                file=upload,
                original_name=upload.name,
                mime_type=mimetypes.guess_type(upload.name)[0] or "application/octet-stream",
                extension=extension,
                size=upload.size,
                sha256_checksum=self._checksum(upload),
                uploaded_by=user,
                created_by=user,
                updated_by=user,
            )
            version = DocumentVersion.objects.create(
                document=instance,
                version_number=next_version,
                stored_file=stored_file,
                change_reason=self.context["request"].data.get("change_reason", "Nueva versión"),
                created_by=user,
                updated_by=user,
            )
            instance.current_version = version
            instance.save(update_fields=["current_version", "updated_at"])
        return instance
