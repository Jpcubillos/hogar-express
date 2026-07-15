from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.catalogs import views


router = DefaultRouter()
for prefix, viewset in [
    ("countries", views.CountryViewSet),
    ("departments", views.DepartmentViewSet),
    ("cities", views.CityViewSet),
    ("neighborhoods", views.NeighborhoodViewSet),
    ("banks", views.BankViewSet),
    ("identification-types", views.IdentificationTypeViewSet),
    ("property-types", views.PropertyTypeViewSet),
    ("document-types", views.DocumentTypeViewSet),
    ("photo-tags", views.PhotoTagViewSet),
    ("inventory-categories", views.InventoryCategoryViewSet),
    ("inventory-concepts", views.InventoryConceptViewSet),
    ("measure-units", views.MeasureUnitViewSet),
    ("repair-categories", views.RepairCategoryViewSet),
    ("provider-specialties", views.ProviderSpecialtyViewSet),
    ("payment-methods", views.PaymentMethodViewSet),
    ("financial-concepts", views.FinancialConceptViewSet),
    ("guarantor-companies", views.GuarantorCompanyViewSet),
    ("guarantee-types", views.GuarantyTypeViewSet),
    ("utility-types", views.UtilityTypeViewSet),
    ("utility-providers", views.UtilityProviderViewSet),
]:
    router.register(prefix, viewset, basename=prefix)

urlpatterns = [path("", include(router.urls))]
