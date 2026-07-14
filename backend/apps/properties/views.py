from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from apps.properties.models import Property
from rest_framework.serializers import ModelSerializer

class PropertySerializer(ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'

class PropertiesViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.filter(is_active=True)
    serializer_class = PropertySerializer
    permission_classes = [permissions.IsAuthenticated]
