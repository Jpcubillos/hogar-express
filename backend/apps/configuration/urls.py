from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.configuration.views import (
    AdministrationFeePlanViewSet,
    DocumentRetentionPolicyViewSet,
    GuaranteeEscalationPolicyViewSet,
    LateFeePolicyViewSet,
    NumberSequenceViewSet,
    OfficeViewSet,
    OrganizationViewSet,
    ProrationPolicyViewSet,
)


router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet, basename='organizations')
router.register(r'offices', OfficeViewSet, basename='offices')
router.register(r'number-sequences', NumberSequenceViewSet, basename='number-sequences')
router.register(r'administration-fee-plans', AdministrationFeePlanViewSet, basename='administration-fee-plans')
router.register(r'late-fee-policies', LateFeePolicyViewSet, basename='late-fee-policies')
router.register(r'proration-policies', ProrationPolicyViewSet, basename='proration-policies')
router.register(
    r'guarantee-escalation-policies',
    GuaranteeEscalationPolicyViewSet,
    basename='guarantee-escalation-policies',
)
router.register(
    r'document-retention-policies',
    DocumentRetentionPolicyViewSet,
    basename='document-retention-policies',
)

urlpatterns = [path('', include(router.urls))]
