from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.core.models import ArchivableModel, DomainModel


class Organization(ArchivableModel):
    legal_name = models.CharField(max_length=255)
    trade_name = models.CharField(max_length=255, blank=True)
    identification_type = models.CharField(max_length=30, default="NIT")
    identification_number = models.CharField(max_length=50, unique=True)
    verification_digit = models.CharField(max_length=2, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    logo = models.FileField(upload_to="organization/", null=True, blank=True)
    timezone = models.CharField(max_length=64, default="America/Bogota")
    currency = models.CharField(max_length=3, default="COP")

    class Meta:
        ordering = ["legal_name"]
        verbose_name = "Organización"
        verbose_name_plural = "Organizaciones"

    def __str__(self):
        return self.trade_name or self.legal_name


class Office(ArchivableModel):
    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="offices")
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    is_main = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["organization", "code"], name="uq_office_org_code"),
            models.UniqueConstraint(
                fields=["organization"],
                condition=models.Q(is_main=True, is_active=True),
                name="uq_office_one_active_main",
            ),
        ]
        ordering = ["organization", "name"]

    def __str__(self):
        return f"{self.organization} - {self.name}"


class NumberSequence(DomainModel):
    class ResetFrequency(models.TextChoices):
        NEVER = "NEVER", "Nunca"
        YEARLY = "YEARLY", "Anual"
        MONTHLY = "MONTHLY", "Mensual"

    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="number_sequences")
    office = models.ForeignKey(Office, on_delete=models.PROTECT, null=True, blank=True, related_name="number_sequences")
    document_kind = models.CharField(max_length=50)
    prefix = models.CharField(max_length=20)
    current_number = models.PositiveBigIntegerField(default=0)
    padding = models.PositiveSmallIntegerField(default=6, validators=[MinValueValidator(1), MaxValueValidator(12)])
    reset_frequency = models.CharField(max_length=10, choices=ResetFrequency.choices, default=ResetFrequency.YEARLY)
    current_period = models.CharField(max_length=10, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "office", "document_kind"],
                name="uq_sequence_scope_kind",
            )
        ]


class EffectivePolicy(ArchivableModel):
    class PolicyStatus(models.TextChoices):
        DRAFT = "DRAFT", "Borrador"
        APPROVED = "APPROVED", "Aprobada"
        RETIRED = "RETIRED", "Retirada"

    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="%(class)s_policies")
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=150)
    valid_from = models.DateField()
    valid_to = models.DateField(null=True, blank=True)
    policy_version = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=12, choices=PolicyStatus.choices, default=PolicyStatus.DRAFT)
    approved_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_%(class)s"
    )
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class AdministrationFeePlan(EffectivePolicy):
    percentage = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    fixed_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["organization", "code", "policy_version"], name="uq_admin_plan_version")
        ]


class LateFeePolicy(EffectivePolicy):
    class CalculationMethod(models.TextChoices):
        SIMPLE_DAILY = "SIMPLE_DAILY", "Interés simple diario"
        FIXED = "FIXED", "Valor fijo"
        MANUAL = "MANUAL", "Cálculo manual"

    calculation_method = models.CharField(max_length=20, choices=CalculationMethod.choices)
    daily_rate = models.DecimalField(max_digits=9, decimal_places=6, default=0, validators=[MinValueValidator(0)])
    fixed_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    grace_days = models.PositiveSmallIntegerField(default=0)
    max_days = models.PositiveSmallIntegerField(null=True, blank=True)
    include_non_business_days = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["organization", "code", "policy_version"], name="uq_late_policy_version")
        ]


class ProrationPolicy(EffectivePolicy):
    daily_basis = models.PositiveSmallIntegerField(default=30, validators=[MinValueValidator(1), MaxValueValidator(366)])
    cutoff_day = models.PositiveSmallIntegerField(default=15, validators=[MinValueValidator(1), MaxValueValidator(31)])
    allow_current_partial_period = models.BooleanField(default=True)
    allow_next_full_period = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["organization", "code", "policy_version"], name="uq_proration_policy_version")
        ]


class GuaranteeEscalationPolicy(EffectivePolicy):
    overdue_days_threshold = models.PositiveSmallIntegerField()
    automatic_escalation = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["organization", "code", "policy_version"], name="uq_guarantee_policy_version")
        ]


class DocumentRetentionPolicy(EffectivePolicy):
    scope = models.CharField(max_length=50)
    retention_months = models.PositiveIntegerField()
    preserve_versions = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["organization", "code", "policy_version"], name="uq_retention_policy_version")
        ]
