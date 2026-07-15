from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BuyerInterestViewSet, SaleListingViewSet, SaleOfferViewSet, SaleTransactionViewSet

router = DefaultRouter()
router.register("listings", SaleListingViewSet, basename="sale-listing")
router.register("interests", BuyerInterestViewSet, basename="buyer-interest")
router.register("offers", SaleOfferViewSet, basename="sale-offer")
router.register("transactions", SaleTransactionViewSet, basename="sale-transaction")
urlpatterns = [path("", include(router.urls))]
