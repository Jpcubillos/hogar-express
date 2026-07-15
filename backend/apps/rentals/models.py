from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.configuration.models import AdministrationFeePlan, LateFeePolicy, ProrationPolicy
from apps.core.models import ArchivableModel, DomainModel
from apps.people.models import Party
from apps.properties.models import Property


class Rental(ArchivableModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Borrador"
        ACTIVE = "ACTIVE", "Activo"
        ENDING = "ENDING", "En terminación"
        ENDED = "ENDED", "Finalizado"
        CANCELLED = "CANCELLED", "Cancelado"

    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name="rentals")
    internal_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT, db_index=True)
    started_on = models.DateField(null=True, blank=True, db_index=True)
    ended_on = models.DateField(null=True, blank=True, db_index=True)
    termination_reason = models.TextField(blank=True)
    current_contract = models.ForeignKey(
        "RentalContract", on_delete=models.SET_NULL, null=True, blank=True, related_name="current_for_rentals"
    )

    class Meta:
        ordering = ["-started_on", "internal_number"]
        indexes = [models.Index(fields=["property", "status"])]

    def __str__(self):
        return f"{self.internal_number} - {self.property}"


class RentalContract(ArchivableModel):
    class ContractType(models.TextChoices):
        INITIAL = "INITIAL", "Inicial"
        RENEWAL = "RENEWAL", "Renovación"

    class DurationUnit(models.TextChoices):
        DAY = "DAY", "Día"
        MONTH = "MONTH", "Mes"
        YEAR = "YEAR", "Año"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Borrador"
        PENDING_SIGNATURE = "PENDING_SIGNATURE", "Pendiente de firma"
        ACTIVE = "ACTIVE", "Activo"
        EXPIRED = "EXPIRED", "Vencido"
        TERMINATED = "TERMINATED", "Terminado"
        VOIDED = "VOIDED", "Anulado"

    rental = models.ForeignKey(Rental, on_delete=models.PROTECT, related_name="contracts")
    contract_number = models.CharField(max_length=50, unique=True)
    contract_type = models.CharField(max_length=10, choices=ContractType.choices)
    contract_version = models.PositiveIntegerField(default=1)
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(db_index=True)
    duration_value = models.PositiveIntegerField()
    duration_unit = models.CharField(max_length=10, choices=DurationUnit.choices)
    billing_day = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(31)])
    rent_amount = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    administration_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    deposit_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    grace_days = models.PositiveSmallIntegerField(default=0)
    administration_fee_plan = models.ForeignKey(
        AdministrationFeePlan, on_delete=models.PROTECT, null=True, blank=True, related_name="contracts"
    )
    late_fee_policy = models.ForeignKey(
        LateFeePolicy, on_delete=models.PROTECT, null=True, blank=True, related_name="contracts"
    )
    proration_policy = models.ForeignKey(
        ProrationPolicy, on_delete=models.PROTECT, null=True, blank=True, related_name="contracts"
    )
    signed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)
    previous_contract = models.ForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True, related_name="renewals"
    )

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(end_date__gte=models.F("start_date")), name="ck_contract_dates"),
            models.UniqueConstraint(fields=["rental", "contract_version"], name="uq_rental_contract_version"),
        ]
        ordering = ["-start_date"]


class RentalParty(DomainModel):
    class Role(models.TextChoices):
        TENANT = "TENANT", "Arrendatario"
        CO_DEBTOR = "CO_DEBTOR", "Codeudor"
        GUARANTOR = "GUARANTOR", "Fiador"
        REPRESENTATIVE = "REPRESENTATIVE", "Representante"

    rental = models.ForeignKey(Rental, on_delete=models.PROTECT, related_name="participants")
    party = models.ForeignKey(Party, on_delete=models.PROTECT, related_name="rental_roles")
    role = models.CharField(max_length=20, choices=Role.choices, db_index=True)
    is_primary = models.BooleanField(default=False)
    liability_percentage = models.DecimalField(
        max_digits=7, decimal_places=4, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    valid_from = models.DateField()
    valid_to = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["rental", "party", "role", "valid_from"], name="uq_rental_party_period"),
            models.UniqueConstraint(
                fields=["rental", "role"],
                condition=models.Q(is_primary=True, valid_to__isnull=True),
                name="uq_rental_primary_role",
            ),
            models.CheckConstraint(
                condition=models.Q(valid_to__isnull=True) | models.Q(valid_to__gte=models.F("valid_from")),
                name="ck_rental_party_dates",
            ),
        ]


class ContractAmendment(DomainModel):
    contract = models.ForeignKey(RentalContract, on_delete=models.PROTECT, related_name="amendments")
    amendment_type = models.CharField(max_length=50)
    effective_date = models.DateField()
    previous_values = models.JSONField(default=dict)
    new_values = models.JSONField(default=dict)
    reason = models.TextField()
    approved_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_contract_amendments"
    )


class RentAdjustment(DomainModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Borrador"
        APPROVED = "APPROVED", "Aprobado"
        APPLIED = "APPLIED", "Aplicado"
        VOIDED = "VOIDED", "Anulado"

    contract = models.ForeignKey(RentalContract, on_delete=models.PROTECT, related_name="rent_adjustments")
    effective_date = models.DateField()
    previous_rent = models.DecimalField(max_digits=16, decimal_places=2)
    new_rent = models.DecimalField(max_digits=16, decimal_places=2)
    percentage = models.DecimalField(max_digits=9, decimal_places=6)
    policy_reference = models.CharField(max_length=100, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)


class RentalStatusHistory(DomainModel):
    rental = models.ForeignKey(Rental, on_delete=models.PROTECT, related_name="status_history")
    previous_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20)
    reason = models.TextField(blank=True)
    changed_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, related_name="rental_status_changes"
    )
    changed_at = models.DateTimeField(auto_now_add=True, db_index=True)


class RentalNote(DomainModel):
    rental = models.ForeignKey(Rental, on_delete=models.PROTECT, related_name="notes")
    note_type = models.CharField(max_length=50, blank=True, db_index=True)
    text = models.TextField()
    is_pinned = models.BooleanField(default=False)
    promised_payment_date = models.DateField(null=True, blank=True, db_index=True)
    visible_until = models.DateField(null=True, blank=True)


class RentalTermination(DomainModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Borrador"
        NOTICE_GIVEN = "NOTICE_GIVEN", "Preaviso registrado"
        APPROVED = "APPROVED", "Aprobada"
        COMPLETED = "COMPLETED", "Completada"
        CANCELLED = "CANCELLED", "Cancelada"

    rental = models.ForeignKey(Rental, on_delete=models.PROTECT, related_name="terminations")
    requested_on = models.DateField()
    effective_on = models.DateField()
    reason = models.TextField()
    non_renewal = models.BooleanField(default=False)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.DRAFT)
    approved_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_terminations"
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(effective_on__gte=models.F("requested_on")), name="ck_termination_dates"
            )
        ]
