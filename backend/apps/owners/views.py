from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

# Placeholder views for owners
from apps.owners.models import Owner
from rest_framework.serializers import ModelSerializer

class OwnerSerializer(ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'

class OwnersViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.filter(is_active=True)
    serializer_class = OwnerSerializer
    permission_classes = [permissions.IsAuthenticated]
