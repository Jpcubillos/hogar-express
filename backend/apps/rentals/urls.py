from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RentalContractViewSet, RentalNoteViewSet, RentalPartyViewSet, RentalTerminationViewSet, RentalViewSet

router = DefaultRouter()
router.register("contracts", RentalContractViewSet, basename="rental-contract")
router.register("participants", RentalPartyViewSet, basename="rental-party")
router.register("notes", RentalNoteViewSet, basename="rental-note")
router.register("terminations", RentalTerminationViewSet, basename="rental-termination")
router.register("", RentalViewSet, basename="rental")
urlpatterns = [path("", include(router.urls))]
