from rest_framework import serializers
from django.contrib.auth import authenticate
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

    def get_groups(self, obj):
        return [group.name for group in obj.groups.all()]

    def get_permissions(self, obj):
        # Return list of codenames of permissions the user actually has
        if obj.is_superuser:
            # Superusers have all permissions
            from django.contrib.auth.models import Permission
            return list(Permission.objects.values_list('codename', flat=True))
        return list(obj.get_all_permissions())


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
