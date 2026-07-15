from django.db import models

from apps.catalogs.models import GuaranteeType, GuarantorCompany
from apps.configuration.models import GuaranteeEscalationPolicy
from apps.core.models import ArchivableModel, DomainModel
from apps.rentals.models import Rental


class RentalGuarantee(ArchivableModel):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Activa"
        EXPIRED = "EXPIRED", "Vencida"
        CANCELLED = "CANCELLED", "Cancelada"

    rental = models.ForeignKey(Rental, on_delete=models.PROTECT, related_name="guarantees")
    guarantor_company = models.ForeignKey(GuarantorCompany, on_delete=models.PROTECT, related_name="rental_guarantees")
    guarantee_type = models.ForeignKey(GuaranteeType, on_delete=models.PROTECT)
    escalation_policy = models.ForeignKey(
        GuaranteeEscalationPolicy, on_delete=models.PROTECT, null=True, blank=True, related_name="rental_guarantees"
    )
    policy_number = models.CharField(max_length=100)
    coverage_start = models.DateField()
    coverage_end = models.DateField()
    maximum_coverage = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["guarantor_company", "policy_number"], name="uq_guarantee_policy_number"),
            models.CheckConstraint(
                condition=models.Q(coverage_end__gte=models.F("coverage_start")), name="ck_guarantee_dates"
            ),
        ]


class GuaranteeCase(ArchivableModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Borrador"
        REPORTED = "REPORTED", "Reportado"
        IN_REVIEW = "IN_REVIEW", "En revisión"
        AGREEMENT = "AGREEMENT", "Acuerdo"
        RESOLVED = "RESOLVED", "Resuelto"
        CLOSED = "CLOSED", "Cerrado"

    rental_guarantee = models.ForeignKey(RentalGuarantee, on_delete=models.PROTECT, related_name="cases")
    opened_at = models.DateTimeField(db_index=True)
    overdue_days_at_open = models.PositiveIntegerField()
    reported_amount = models.DecimalField(max_digits=16, decimal_places=2)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT, db_index=True)
    resolution = models.TextField(blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)


class GuaranteeCaseEvent(DomainModel):
    guarantee_case = models.ForeignKey(GuaranteeCase, on_delete=models.PROTECT, related_name="events")
    event_type = models.CharField(max_length=50)
    occurred_at = models.DateTimeField(db_index=True)
    amount = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    description = models.TextField()
