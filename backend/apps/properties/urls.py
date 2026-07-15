from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PropertiesViewSet, PropertyInventoryViewSet, RentalListingViewSet

router = DefaultRouter()
router.register("rental-listings", RentalListingViewSet, basename="rental-listing")
router.register("inventories", PropertyInventoryViewSet, basename="property-inventory")
router.register("", PropertiesViewSet, basename="property")
urlpatterns = [path("", include(router.urls))]
