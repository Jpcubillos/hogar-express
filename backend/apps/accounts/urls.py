from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.accounts.views import CSRFView, LoginView, LogoutView, MeView, RoleViewSet, UserPermissionsView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'roles', RoleViewSet, basename='roles')

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth_login'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('me/', MeView.as_view(), name='auth_me'),
    path('csrf/', CSRFView.as_view(), name='auth_csrf'),
    path('permissions/', UserPermissionsView.as_view(), name='auth_permissions'),
] + router.urls
