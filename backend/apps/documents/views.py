from django.http import FileResponse, Http404, HttpResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.documents.models import Document
from apps.documents.serializers import DocumentSerializer
from apps.audit.models import AuditEvent
import os

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.filter(is_archived=False)
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Allow filtering by associated entity
        queryset = super().get_queryset()
        owner_id = self.request.query_params.get('owner')
        property_id = self.request.query_params.get('property')
        repair_id = self.request.query_params.get('repair')
        
        if owner_id:
            queryset = queryset.filter(owner_id=owner_id)
        if property_id:
            queryset = queryset.filter(property_id=property_id)
        if repair_id:
            queryset = queryset.filter(repair_id=repair_id)
            
        return queryset

    @action(detail=True, methods=['get'], url_path='content')
    def download_content(self, request, pk=None):
        """
        Serves the file content securely.
        Requires 'documents.view_private_document' permission unless user is admin.
        """
        document = self.get_object()
        
        # 1. Permission check
        if not request.user.is_superuser and not request.user.has_perm('accounts.view_private_document'):
            # Allow access if the user uploaded it or is related to a permitted entity
            # (But standard check using Django permissions is safer)
            return Response({'detail': 'No tiene permisos para acceder a este documento.'}, status=status.HTTP_403_FORBIDDEN)

        # 2. Check if file exists physically
        if not document.file or not os.path.exists(document.file.path):
            raise Http404("El archivo físico no fue encontrado en el servidor.")

        # 3. Log Audit download event
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR')
        
        AuditEvent.objects.create(
            user=request.user,
            action='DOWNLOAD',
            ip=ip,
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            entity_type='document',
            record_id=str(document.id),
            path=request.path[:255],
            method=request.method,
            result='SUCCESS'
        )

        # 4. Deliver file
        response = FileResponse(open(document.file.path, 'rb'), content_type=document.mime_type)
        
        # If user wants download vs preview
        disposition = request.query_params.get('disposition', 'inline')
        if disposition == 'attachment':
            response['Content-Disposition'] = f'attachment; filename="{document.original_name}"'
        else:
            response['Content-Disposition'] = f'inline; filename="{document.original_name}"'
            
        # In production Nginx would intercept this with X-Accel-Redirect.
        # We can add the X-Accel-Redirect header setup for production:
        # if not settings.DEBUG:
        #     response['X-Accel-Redirect'] = f'/protected_media/{document.file.name}'
            
        return response
