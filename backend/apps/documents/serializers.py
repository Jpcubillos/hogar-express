from rest_framework import serializers
from django.conf import settings
from apps.documents.models import Document
import os

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'id', 'name', 'original_name', 'file', 'document_type',
            'tag', 'description', 'mime_type', 'extension', 'size',
            'uploaded_by', 'uploaded_at', 'is_archived', 'entity_type',
            'owner', 'property', 'repair'
        ]
        read_only_fields = ['id', 'original_name', 'mime_type', 'extension', 'size', 'checksum', 'uploaded_by', 'uploaded_at']

    def validate_file(self, value):
        # 1. Size check
        max_size_mb = getattr(settings, 'MAX_UPLOAD_SIZE_MB', 10)
        max_size_bytes = max_size_mb * 1024 * 1024
        if value.size > max_size_bytes:
            raise serializers.ValidationError(f"El archivo supera el tamaño máximo permitido de {max_size_mb} MB.")

        # 2. Extension check
        ext = os.path.splitext(value.name)[1].lower()
        allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.webp']
        if ext not in allowed_extensions:
            raise serializers.ValidationError(f"Extensión de archivo no permitida. Permitidas: {', '.join(allowed_extensions)}")

        return value

    def create(self, validated_data):
        file_obj = validated_data['file']
        ext = os.path.splitext(file_obj.name)[1].lower().replace('.', '')
        
        # Determine MIME type
        from mimetypes import guess_type
        mime_type, _ = guess_type(file_obj.name)
        if not mime_type:
            mime_type = 'application/octet-stream'

        validated_data['original_name'] = file_obj.name
        validated_data['extension'] = ext
        validated_data['mime_type'] = mime_type
        validated_data['size'] = file_obj.size
        validated_data['uploaded_by'] = self.context['request'].user

        # Create temporary instance to calculate checksum
        instance = Document(**validated_data)
        instance.checksum = instance.calculate_checksum()
        instance.save()
        
        return instance
