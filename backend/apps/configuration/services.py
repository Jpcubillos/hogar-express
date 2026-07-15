from django.db import transaction
from django.utils import timezone

from .models import NumberSequence


@transaction.atomic
def next_document_number(sequence_id, occurred_at=None):
    """Return the next collision-safe formatted number for a document sequence."""
    sequence = NumberSequence.objects.select_for_update().get(pk=sequence_id)
    occurred_at = occurred_at or timezone.now()
    if sequence.reset_frequency == NumberSequence.ResetFrequency.YEARLY:
        period = occurred_at.strftime("%Y")
    elif sequence.reset_frequency == NumberSequence.ResetFrequency.MONTHLY:
        period = occurred_at.strftime("%Y%m")
    else:
        period = ""
    if period != sequence.current_period:
        sequence.current_period = period
        sequence.current_number = 0
    sequence.current_number += 1
    sequence.save(update_fields=["current_period", "current_number", "updated_at"])
    components = [sequence.prefix]
    if period:
        components.append(period)
    components.append(str(sequence.current_number).zfill(sequence.padding))
    return "-".join(components)
