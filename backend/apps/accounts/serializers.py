from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from apps.accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'display_name',
            'groups', 'permissions', 'is_staff', 'is_superuser'
        ]

    def get_groups(self, obj) -> list[str]:
        return [group.name for group in obj.groups.all()]

    def get_permissions(self, obj) -> list[str]:
        # Return list of codenames of permissions the user actually has
        if obj.is_superuser:
            # Superusers have all permissions
            from django.contrib.auth.models import Permission
            return list(Permission.objects.values_list('codename', flat=True))
        return list(obj.get_all_permissions())


class UserManagementSerializer(serializers.ModelSerializer):
    """Serializer seguro para administrar usuarios sin exponer hashes de contraseña."""

    password = serializers.CharField(write_only=True, required=False, min_length=8)
    groups = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        queryset=Group.objects.all(),
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'display_name',
            'groups',
            'is_active',
            'is_staff',
            'must_change_password',
            'locked_until',
            'last_login',
            'date_joined',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'last_login',
            'date_joined',
            'created_at',
            'updated_at',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        if not password:
            raise serializers.ValidationError({'password': 'La contraseña es obligatoria.'})
        user = super().create(validated_data)
        user.set_password(password)
        user.save(update_fields=['password'])
        return user


class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

    def get_permissions(self, obj) -> list[str]:
        return list(
            obj.permissions.order_by('content_type__app_label', 'codename').values_list(
                'codename',
                flat=True,
            )
        )

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save(update_fields=['password'])
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Credenciales inválidas. Por favor verifique e intente de nuevo.")
            if not user.is_active:
                raise serializers.ValidationError("Esta cuenta de usuario ha sido desactivada.")
            data['user'] = user
        else:
            raise serializers.ValidationError("Debe proporcionar usuario y contraseña.")
        return data


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()


class CSRFTokenSerializer(serializers.Serializer):
    csrfToken = serializers.CharField()


class PermissionsSerializer(serializers.Serializer):
    permissions = serializers.ListField(child=serializers.CharField())
    groups = serializers.ListField(child=serializers.CharField())
