from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import OperationalAlertViewSet, ReportDefinitionViewSet, ReportRunViewSet

router = DefaultRouter()
router.register("definitions", ReportDefinitionViewSet, basename="report-definition")
router.register("runs", ReportRunViewSet, basename="report-run")
router.register("alerts", OperationalAlertViewSet, basename="operational-alert")
urlpatterns = [path("", include(router.urls))]
