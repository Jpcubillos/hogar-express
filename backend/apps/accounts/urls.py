from django.urls import path
from apps.accounts.views import LoginView, LogoutView, MeView, CSRFView, UserPermissionsView

urlpatterns = [
    path('login/', LoginView.as_view(), name='auth_login'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('me/', MeView.as_view(), name='auth_me'),
    path('csrf/', CSRFView.as_view(), name='auth_csrf'),
    path('permissions/', UserPermissionsView.as_view(), name='auth_permissions'),
]
