from apps.core.api import domain_viewset_for
from apps.sales.models import BuyerInterest, SaleListing, SaleOffer, SaleTransaction

SaleListingViewSet = domain_viewset_for(SaleListing, ("property", "status", "is_active"))
BuyerInterestViewSet = domain_viewset_for(BuyerInterest, ("sale_listing", "buyer", "status", "is_active"))
SaleOfferViewSet = domain_viewset_for(SaleOffer, ("buyer_interest", "status", "is_active"))
SaleTransactionViewSet = domain_viewset_for(SaleTransaction, ("sale_listing", "buyer", "status", "is_active"))
