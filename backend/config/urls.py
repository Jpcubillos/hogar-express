from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from apps.core.views import health_check, ready_check

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # OpenAPI Schema & Docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API endpoints
    path('api/v1/health/', health_check, name='health_check'),
    path('api/v1/ready/', ready_check, name='ready_check'),
    
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/configuration/', include('apps.configuration.urls')),
    path('api/v1/audit/', include('apps.audit.urls')),
    path('api/v1/catalogs/', include('apps.catalogs.urls')),
    path('api/v1/documents/', include('apps.documents.urls')),
    path('api/v1/owners/', include('apps.owners.urls')),
    path('api/v1/properties/', include('apps.properties.urls')),
    path('api/v1/people/', include('apps.people.urls')),
    path('api/v1/rentals/', include('apps.rentals.urls')),
    path('api/v1/payments/', include('apps.payments.urls')),
    path('api/v1/guarantors/', include('apps.guarantors.urls')),
    path('api/v1/sales/', include('apps.sales.urls')),
    path('api/v1/repairs/', include('apps.repairs.urls')),
    path('api/v1/reports/', include('apps.reports.urls')),
]
