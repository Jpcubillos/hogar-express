from apps.core.api import domain_viewset_for
from apps.properties.models import Property, PropertyInventory, RentalListing

PropertiesViewSet = domain_viewset_for(
    Property, ("property_type", "city", "neighborhood", "operational_status", "is_active")
)
RentalListingViewSet = domain_viewset_for(RentalListing, ("property", "status", "is_active"))
PropertyInventoryViewSet = domain_viewset_for(PropertyInventory, ("property", "rental", "status"))
