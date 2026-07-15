from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PartyViewSet, ProviderViewSet

router = DefaultRouter()
router.register("parties", PartyViewSet, basename="party")
router.register("providers", ProviderViewSet, basename="provider")
urlpatterns = [path("", include(router.urls))]
