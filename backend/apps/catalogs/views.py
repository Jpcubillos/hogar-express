from rest_framework import viewsets, permissions, serializers
from apps.catalogs.models import Bank, City, Neighborhood, PropertyType, DocumentType, PhotoTag, RepairCategory, PaymentMethod, GuarantorCompany, GuarantyType

# Base Serializer
class CatalogBaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'code', 'name', 'description', 'order', 'is_active']


# Specific Serializers
class BankSerializer(CatalogBaseSerializer):
    class Meta(CatalogBaseSerializer.Meta):
        model = Bank

class CitySerializer(CatalogBaseSerializer):
    class Meta(CatalogBaseSerializer.Meta):
        model = City
        fields = CatalogBaseSerializer.Meta.fields + ['department', 'country']

class NeighborhoodSerializer(CatalogBaseSerializer):
    class Meta(CatalogBaseSerializer.Meta):
        model = Neighborhood
        fields = CatalogBaseSerializer.Meta.fields + ['city']

class PropertyTypeSerializer(CatalogBaseSerializer):
    class Meta(CatalogBaseSerializer.Meta):
        model = PropertyType

class DocumentTypeSerializer(CatalogBaseSerializer):
    class Meta(CatalogBaseSerializer.Meta):
        model = DocumentType

class PhotoTagSerializer(CatalogBaseSerializer):
    class Meta(CatalogBaseSerializer.Meta):
        model = PhotoTag

class RepairCategorySerializer(CatalogBaseSerializer):
    class Meta(CatalogBaseSerializer.Meta):
        model = RepairCategory

class PaymentMethodSerializer(CatalogBaseSerializer):
    class Meta(CatalogBaseSerializer.Meta):
        model = PaymentMethod

class GuarantorCompanySerializer(CatalogBaseSerializer):
    class Meta(CatalogBaseSerializer.Meta):
        model = GuarantorCompany

class GuarantyTypeSerializer(CatalogBaseSerializer):
    class Meta(CatalogBaseSerializer.Meta):
        model = GuarantyType


# ViewSets (Read-only by default for standard users, writeable by admin)
class CatalogBaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return super().get_permissions()

class BankViewSet(CatalogBaseViewSet):
    queryset = Bank.objects.filter(is_active=True)
    serializer_class = BankSerializer

class CityViewSet(CatalogBaseViewSet):
    queryset = City.objects.filter(is_active=True)
    serializer_class = CitySerializer

class NeighborhoodViewSet(CatalogBaseViewSet):
    queryset = Neighborhood.objects.filter(is_active=True)
    serializer_class = NeighborhoodSerializer
    filterset_fields = ['city']

class PropertyTypeViewSet(CatalogBaseViewSet):
    queryset = PropertyType.objects.filter(is_active=True)
    serializer_class = PropertyTypeSerializer

class DocumentTypeViewSet(CatalogBaseViewSet):
    queryset = DocumentType.objects.filter(is_active=True)
    serializer_class = DocumentTypeSerializer

class PhotoTagViewSet(CatalogBaseViewSet):
    queryset = PhotoTag.objects.filter(is_active=True)
    serializer_class = PhotoTagSerializer

class RepairCategoryViewSet(CatalogBaseViewSet):
    queryset = RepairCategory.objects.filter(is_active=True)
    serializer_class = RepairCategorySerializer

class PaymentMethodViewSet(CatalogBaseViewSet):
    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer

class GuarantorCompanyViewSet(CatalogBaseViewSet):
    queryset = GuarantorCompany.objects.filter(is_active=True)
    serializer_class = GuarantorCompanySerializer

class GuarantyTypeViewSet(CatalogBaseViewSet):
    queryset = GuarantyType.objects.filter(is_active=True)
    serializer_class = GuarantyTypeSerializer
