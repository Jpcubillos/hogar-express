from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BillingPeriodViewSet, ChargeViewSet, OwnerSettlementViewSet, PaymentViewSet, ReceiptViewSet

router = DefaultRouter()
router.register("billing-periods", BillingPeriodViewSet, basename="billing-period")
router.register("charges", ChargeViewSet, basename="charge")
router.register("receipts", ReceiptViewSet, basename="receipt")
router.register("owner-settlements", OwnerSettlementViewSet, basename="owner-settlement")
router.register("", PaymentViewSet, basename="payment")
urlpatterns = [path("", include(router.urls))]
