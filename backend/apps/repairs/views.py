from apps.core.api import domain_viewset_for
from apps.repairs.models import PropertyIssue, RepairCost, RepairOrder, RepairQuote

PropertyIssueViewSet = domain_viewset_for(PropertyIssue, ("property", "rental", "status", "priority", "is_active"))
RepairsViewSet = domain_viewset_for(RepairOrder, ("property", "rental", "status", "priority", "is_active"))
RepairQuoteViewSet = domain_viewset_for(RepairQuote, ("repair", "provider", "status", "is_active"))
RepairCostViewSet = domain_viewset_for(RepairCost, ("repair", "provider", "cost_type", "is_active"))
