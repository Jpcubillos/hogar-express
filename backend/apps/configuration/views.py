from apps.configuration.models import (
    AdministrationFeePlan,
    DocumentRetentionPolicy,
    GuaranteeEscalationPolicy,
    LateFeePolicy,
    NumberSequence,
    Office,
    Organization,
    ProrationPolicy,
)
from apps.core.api import domain_viewset_for


OrganizationViewSet = domain_viewset_for(Organization, ('is_active', 'currency', 'timezone'))
OfficeViewSet = domain_viewset_for(Office, ('organization', 'is_active', 'is_main'))
NumberSequenceViewSet = domain_viewset_for(NumberSequence, ('organization', 'office', 'document_kind'))
AdministrationFeePlanViewSet = domain_viewset_for(AdministrationFeePlan, ('organization', 'status', 'is_active'))
LateFeePolicyViewSet = domain_viewset_for(LateFeePolicy, ('organization', 'status', 'is_active'))
ProrationPolicyViewSet = domain_viewset_for(ProrationPolicy, ('organization', 'status', 'is_active'))
GuaranteeEscalationPolicyViewSet = domain_viewset_for(
    GuaranteeEscalationPolicy,
    ('organization', 'status', 'is_active'),
)
DocumentRetentionPolicyViewSet = domain_viewset_for(
    DocumentRetentionPolicy,
    ('organization', 'status', 'scope', 'is_active'),
)
