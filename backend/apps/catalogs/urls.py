from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.catalogs.views import (
    BankViewSet, CityViewSet, NeighborhoodViewSet, PropertyTypeViewSet,
    DocumentTypeViewSet, PhotoTagViewSet, RepairCategoryViewSet,
    PaymentMethodViewSet, GuarantorCompanyViewSet, GuarantyTypeViewSet
)

router = DefaultRouter()
router.register(r'banks', BankViewSet)
router.register(r'cities', CityViewSet)
router.register(r'neighborhoods', NeighborhoodViewSet)
router.register(r'property-types', PropertyTypeViewSet)
router.register(r'document-types', DocumentTypeViewSet)
router.register(r'photo-tags', PhotoTagViewSet)
router.register(r'repair-categories', RepairCategoryViewSet)
router.register(r'payment-methods', PaymentMethodViewSet)
router.register(r'guarantor-companies', GuarantorCompanyViewSet)
router.register(r'guaranty-types', GuarantyTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
