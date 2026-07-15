import os

from django.contrib.contenttypes.models import ContentType
from django.http import FileResponse, Http404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.audit.models import AuditEvent
from apps.documents.models import Document
from apps.documents.serializers import DocumentSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.filter(is_active=True).select_related("current_version__stored_file", "document_type")
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        app_label = self.request.query_params.get("app_label")
        model = self.request.query_params.get("model")
        object_id = self.request.query_params.get("object_id")
        if app_label and model and object_id:
            content_type = ContentType.objects.get_by_natural_key(app_label, model)
            queryset = queryset.filter(links__content_type=content_type, links__object_id=object_id)
        return queryset.distinct()

    @action(detail=True, methods=["get"], url_path="content")
    def download_content(self, request, pk=None):
        document = self.get_object()
        if not request.user.is_superuser and not request.user.has_perm("documents.view_private_document"):
            return Response({"detail": "No tiene permiso para acceder al documento."}, status=status.HTTP_403_FORBIDDEN)
        stored_file = document.current_version.stored_file if document.current_version else None
        if stored_file is None or not stored_file.file or not os.path.exists(stored_file.file.path):
            raise Http404("El archivo físico no fue encontrado.")
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        ip = forwarded.split(",")[0].strip() if forwarded else request.META.get("REMOTE_ADDR")
        AuditEvent.objects.create(
            user=request.user,
            action=AuditEvent.Action.DOWNLOAD,
            ip=ip,
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:500],
            entity_type="documents.Document",
            record_id=str(document.id),
            path=request.path[:255],
            method=request.method,
        )
        response = FileResponse(open(stored_file.file.path, "rb"), content_type=stored_file.mime_type)
        disposition = "attachment" if request.query_params.get("disposition") == "attachment" else "inline"
        response["Content-Disposition"] = f'{disposition}; filename="{stored_file.original_name}"'
        return response
