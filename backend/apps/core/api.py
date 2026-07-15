from django.utils import timezone
from rest_framework import permissions, serializers, viewsets


DOMAIN_READ_ONLY_FIELDS = (
    "id",
    "created_at",
    "updated_at",
    "created_by",
    "updated_by",
    "version",
    "archived_at",
    "archived_by",
)


def domain_serializer_for(model, extra_read_only=()):
    meta = type(
        "Meta",
        (),
        {
            "model": model,
            "fields": "__all__",
            "read_only_fields": DOMAIN_READ_ONLY_FIELDS + tuple(extra_read_only),
        },
    )
    return type(f"{model.__name__}Serializer", (serializers.ModelSerializer,), {"Meta": meta})


class AuditedModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.DjangoModelPermissions]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        if hasattr(instance, "is_active"):
            instance.is_active = False
            instance.archived_at = timezone.now()
            instance.archived_by = self.request.user
            instance.save(update_fields=["is_active", "archived_at", "archived_by", "updated_at"])
        else:
            raise serializers.ValidationError("Este registro no admite eliminación desde la API.")


def domain_viewset_for(model, filterset_fields=(), extra_read_only=()):
    queryset = model.objects.all()
    if any(field.name == "is_active" for field in model._meta.fields):
        queryset = queryset.filter(is_active=True)
    attrs = {
        "queryset": queryset,
        "serializer_class": domain_serializer_for(model, extra_read_only),
        "filterset_fields": filterset_fields,
    }
    return type(f"{model.__name__}ViewSet", (AuditedModelViewSet,), attrs)
