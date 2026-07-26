from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    RepairIncidentViewSet,
    RepairOrderViewSet,
    RepairTaskViewSet,
    RepairQuoteViewSet,
    RepairQuoteItemViewSet,
    RepairCostViewSet,
    RepairApprovalViewSet,
    RepairWarrantyViewSet,
    RepairCommentViewSet,
    RepairTimelineEventViewSet,
)

router = DefaultRouter()
router.register("incidents", RepairIncidentViewSet, basename="repair-incident")
router.register("orders", RepairOrderViewSet, basename="repair-order")
router.register("tasks", RepairTaskViewSet, basename="repair-task")
router.register("quotes", RepairQuoteViewSet, basename="repair-quote")
router.register("quote-items", RepairQuoteItemViewSet, basename="repair-quote-item")
router.register("costs", RepairCostViewSet, basename="repair-cost")
router.register("approvals", RepairApprovalViewSet, basename="repair-approval")
router.register("warranties", RepairWarrantyViewSet, basename="repair-warranty")
router.register("comments", RepairCommentViewSet, basename="repair-comment")
router.register("timeline", RepairTimelineEventViewSet, basename="repair-timeline")

urlpatterns = [path("", include(router.urls))]
