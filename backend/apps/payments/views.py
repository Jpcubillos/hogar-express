from apps.core.api import domain_viewset_for
from apps.payments.models import BillingPeriod, Charge, OwnerSettlement, Payment, Receipt

BillingPeriodViewSet = domain_viewset_for(BillingPeriod, ("rental", "status", "due_date"))
ChargeViewSet = domain_viewset_for(Charge, ("billing_period", "party", "status", "due_date", "is_active"))
PaymentViewSet = domain_viewset_for(Payment, ("payer", "rental", "status", "payment_method", "is_active"))
ReceiptViewSet = domain_viewset_for(Receipt, ("party", "receipt_type", "status", "is_active"), ("number", "current_version"))
OwnerSettlementViewSet = domain_viewset_for(OwnerSettlement, ("owner", "status", "period_start", "period_end", "is_active"))

# Receipts must only be issued/versioned through transactional services.
ReceiptViewSet.http_method_names = ["get", "head", "options"]
