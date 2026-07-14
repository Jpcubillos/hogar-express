from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

# Placeholder views for repairs
from apps.repairs.models import Repair
from rest_framework.serializers import ModelSerializer

class RepairSerializer(ModelSerializer):
    class Meta:
        model = Repair
        fields = '__all__'

class RepairsViewSet(viewsets.ModelViewSet):
    queryset = Repair.objects.filter(is_active=True)
    serializer_class = RepairSerializer
    permission_classes = [permissions.IsAuthenticated]
