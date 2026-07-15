from apps.core.api import domain_viewset_for
from apps.rentals.models import Rental, RentalContract, RentalNote, RentalParty, RentalTermination

RentalViewSet = domain_viewset_for(Rental, ("property", "status", "is_active"), ("current_contract",))
RentalContractViewSet = domain_viewset_for(RentalContract, ("rental", "status", "contract_type", "is_active"))
RentalPartyViewSet = domain_viewset_for(RentalParty, ("rental", "party", "role"))
RentalNoteViewSet = domain_viewset_for(RentalNote, ("rental", "note_type", "is_pinned"))
RentalTerminationViewSet = domain_viewset_for(RentalTermination, ("rental", "status", "non_renewal"))
