from rest_framework import viewsets, permissions
from apps.audit.models import AuditEvent
from rest_framework.serializers import ModelSerializer

class AuditEventSerializer(ModelSerializer):
    class Meta:
        model = AuditEvent
        fields = '__all__'

class AuditEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditEvent.objects.all()
    serializer_class = AuditEventSerializer
    permission_classes = [permissions.IsAdminUser] # Admin only
    filterset_fields = ['action', 'result', 'entity_type']
    search_fields = ['user__username', 'record_id', 'ip']
