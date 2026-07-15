from apps.core.api import domain_viewset_for
from apps.people.models import Party, ProviderProfile

PartyViewSet = domain_viewset_for(Party, ("party_type", "identification_type", "is_active"))
ProviderViewSet = domain_viewset_for(ProviderProfile, ("provider_kind", "is_active"))
