from django.contrib.auth import login as django_login, logout as django_logout
from django.contrib.auth.models import Group
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets
from drf_spectacular.utils import extend_schema
from apps.accounts.serializers import (
    CSRFTokenSerializer,
    LoginSerializer,
    MessageSerializer,
    PermissionsSerializer,
    RoleSerializer,
    UserManagementSerializer,
    UserSerializer,
)
from apps.accounts.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.prefetch_related('groups').order_by('username')
    serializer_class = UserManagementSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    filterset_fields = ('is_active', 'is_staff', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'display_name')
    ordering_fields = ('username', 'email', 'date_joined', 'last_login')

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save(update_fields=['is_active', 'updated_at'])


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.prefetch_related('permissions').order_by('name')
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(request=LoginSerializer, responses={200: UserSerializer})
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        django_login(request, user)
        return Response(UserSerializer(user).data)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=None, responses={200: MessageSerializer})
    def post(self, request):
        django_logout(request)
        return Response({'message': 'Sesión cerrada correctamente'})


class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: UserSerializer})
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class CSRFView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(responses={200: CSRFTokenSerializer})
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        # ensure_csrf_cookie decorator forces Django to set the CSRF cookie
        return Response({'csrfToken': get_token(request)})


class UserPermissionsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(responses={200: PermissionsSerializer})
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            'permissions': serializer.data['permissions'],
            'groups': serializer.data['groups']
        })
