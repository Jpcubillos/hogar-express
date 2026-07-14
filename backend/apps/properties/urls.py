from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.properties.views import PropertiesViewSet

router = DefaultRouter()
router.register(r'', PropertiesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
