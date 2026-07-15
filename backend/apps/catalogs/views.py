from rest_framework import permissions, serializers, viewsets

from apps.catalogs import models


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"


def serializer_for(model):
    return type(f"{model.__name__}Serializer", (CatalogSerializer,), {"Meta": type("Meta", (), {"model": model, "fields": "__all__"})})


class CatalogViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [permissions.IsAdminUser()]
        return super().get_permissions()


def viewset_for(model, filterset_fields=()):
    attrs = {
        "queryset": model.objects.filter(is_active=True),
        "serializer_class": serializer_for(model),
        "filterset_fields": filterset_fields,
    }
    return type(f"{model.__name__}ViewSet", (CatalogViewSet,), attrs)


CountryViewSet = viewset_for(models.Country)
DepartmentViewSet = viewset_for(models.Department, ("country",))
CityViewSet = viewset_for(models.City, ("department",))
NeighborhoodViewSet = viewset_for(models.Neighborhood, ("city",))
BankViewSet = viewset_for(models.Bank)
IdentificationTypeViewSet = viewset_for(models.IdentificationType)
PropertyTypeViewSet = viewset_for(models.PropertyType)
DocumentTypeViewSet = viewset_for(models.DocumentType)
PhotoTagViewSet = viewset_for(models.PhotoTag)
InventoryCategoryViewSet = viewset_for(models.InventoryCategory)
InventoryConceptViewSet = viewset_for(models.InventoryConcept, ("category",))
MeasureUnitViewSet = viewset_for(models.MeasureUnit)
RepairCategoryViewSet = viewset_for(models.RepairCategory)
ProviderSpecialtyViewSet = viewset_for(models.ProviderSpecialty)
PaymentMethodViewSet = viewset_for(models.PaymentMethod)
FinancialConceptViewSet = viewset_for(models.FinancialConcept, ("kind",))
GuarantorCompanyViewSet = viewset_for(models.GuarantorCompany)
GuarantyTypeViewSet = viewset_for(models.GuaranteeType)
UtilityTypeViewSet = viewset_for(models.UtilityType)
UtilityProviderViewSet = viewset_for(models.UtilityProvider)
