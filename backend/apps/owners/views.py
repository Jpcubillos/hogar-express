from apps.core.api import domain_viewset_for
from apps.owners.models import Owner

OwnersViewSet = domain_viewset_for(Owner, ("is_active",))
