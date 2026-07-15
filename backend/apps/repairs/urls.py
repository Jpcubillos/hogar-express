from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PropertyIssueViewSet, RepairCostViewSet, RepairQuoteViewSet, RepairsViewSet

router = DefaultRouter()
router.register("issues", PropertyIssueViewSet, basename="property-issue")
router.register("orders", RepairsViewSet, basename="repair-order")
router.register("quotes", RepairQuoteViewSet, basename="repair-quote")
router.register("costs", RepairCostViewSet, basename="repair-cost")
urlpatterns = [path("", include(router.urls))]
