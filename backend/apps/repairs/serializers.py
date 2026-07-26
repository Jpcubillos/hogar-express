from rest_framework import serializers
from apps.repairs.models import (
    RepairIncident,
    RepairOrder,
    RepairTask,
    RepairStatusHistory,
    RepairQuote,
    RepairQuoteItem,
    RepairApproval,
    RepairCost,
    RepairCostAllocation,
    RepairAllocationInstallment,
    ProviderPayment,
    RepairWarranty,
    RepairComment,
    RepairTimelineEvent,
)


class RepairIncidentSerializer(serializers.ModelSerializer):
    property_address = serializers.ReadOnlyField(source="property.address_line")
    category_name = serializers.ReadOnlyField(source="category.name")

    class Meta:
        model = RepairIncident
        fields = "__all__"


class RepairTaskSerializer(serializers.ModelSerializer):
    provider_name = serializers.ReadOnlyField(source="assigned_provider.party.display_name")

    class Meta:
        model = RepairTask
        fields = "__all__"


class RepairStatusHistorySerializer(serializers.ModelSerializer):
    changed_by_name = serializers.ReadOnlyField(source="changed_by.display_name")

    class Meta:
        model = RepairStatusHistory
        fields = "__all__"


class RepairQuoteItemSerializer(serializers.ModelSerializer):
    unit_name = serializers.ReadOnlyField(source="unit.name")

    class Meta:
        model = RepairQuoteItem
        fields = "__all__"


class RepairQuoteSerializer(serializers.ModelSerializer):
    items = RepairQuoteItemSerializer(many=True, read_only=True)
    provider_name = serializers.ReadOnlyField(source="provider.party.display_name")

    class Meta:
        model = RepairQuote
        fields = "__all__"


class RepairApprovalSerializer(serializers.ModelSerializer):
    decided_by_user_name = serializers.ReadOnlyField(source="decided_by_user.display_name")

    class Meta:
        model = RepairApproval
        fields = "__all__"


class RepairCostSerializer(serializers.ModelSerializer):
    provider_name = serializers.ReadOnlyField(source="provider.party.display_name")

    class Meta:
        model = RepairCost
        fields = "__all__"


class RepairCostAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairCostAllocation
        fields = "__all__"


class ProviderPaymentSerializer(serializers.ModelSerializer):
    provider_name = serializers.ReadOnlyField(source="provider.party.display_name")

    class Meta:
        model = ProviderPayment
        fields = "__all__"


class RepairWarrantySerializer(serializers.ModelSerializer):
    provider_name = serializers.ReadOnlyField(source="provider.party.display_name")

    class Meta:
        model = RepairWarranty
        fields = "__all__"


class RepairCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source="user.display_name")

    class Meta:
        model = RepairComment
        fields = "__all__"


class RepairTimelineEventSerializer(serializers.ModelSerializer):
    performed_by_name = serializers.ReadOnlyField(source="performed_by.display_name")

    class Meta:
        model = RepairTimelineEvent
        fields = "__all__"


class RepairOrderSerializer(serializers.ModelSerializer):
    """
    Serializer para el Aggregate Root (RepairOrder).
    Proporciona información anidada para vistas de detalle y la propiedad calculada is_overdue.
    """
    property_address = serializers.ReadOnlyField(source="property.address_line")
    category_name = serializers.ReadOnlyField(source="category.name")
    internal_responsible_name = serializers.ReadOnlyField(source="internal_responsible.display_name")
    is_overdue = serializers.ReadOnlyField()

    tasks = RepairTaskSerializer(many=True, read_only=True)
    quotes = RepairQuoteSerializer(many=True, read_only=True)
    costs = RepairCostSerializer(many=True, read_only=True)
    approvals = RepairApprovalSerializer(many=True, read_only=True)
    warranties = RepairWarrantySerializer(many=True, read_only=True)
    comments = RepairCommentSerializer(many=True, read_only=True)
    timeline_events = RepairTimelineEventSerializer(many=True, read_only=True)
    status_history = RepairStatusHistorySerializer(many=True, read_only=True)

    class Meta:
        model = RepairOrder
        fields = "__all__"
