from apps.core.api import domain_viewset_for
from apps.guarantors.models import GuaranteeCase, RentalGuarantee

RentalGuaranteeViewSet = domain_viewset_for(RentalGuarantee, ("rental", "guarantor_company", "status", "is_active"))
GuaranteeCaseViewSet = domain_viewset_for(GuaranteeCase, ("rental_guarantee", "status", "is_active"))
