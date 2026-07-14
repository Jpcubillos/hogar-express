from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.repairs.views import RepairsViewSet

router = DefaultRouter()
router.register(r'', RepairsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
