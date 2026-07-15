from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GuaranteeCaseViewSet, RentalGuaranteeViewSet

router = DefaultRouter()
router.register("guarantees", RentalGuaranteeViewSet, basename="rental-guarantee")
router.register("cases", GuaranteeCaseViewSet, basename="guarantee-case")
urlpatterns = [path("", include(router.urls))]
