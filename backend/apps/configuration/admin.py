from django.contrib import admin

from .models import (
    AdministrationFeePlan,
    DocumentRetentionPolicy,
    GuaranteeEscalationPolicy,
    LateFeePolicy,
    NumberSequence,
    Office,
    Organization,
    ProrationPolicy,
)


admin.site.register(
    [
        Organization,
        Office,
        NumberSequence,
        AdministrationFeePlan,
        LateFeePolicy,
        ProrationPolicy,
        GuaranteeEscalationPolicy,
        DocumentRetentionPolicy,
    ]
)
