from decimal import Decimal

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator
from django.db import models

from apps.catalogs.models import FinancialConcept, PaymentMethod
from apps.configuration.models import LateFeePolicy, Office, Organization
from apps.core.models import ArchivableModel, DomainModel
from apps.documents.models import Document
from apps.owners.models import BankAccount, Owner, OwnerPaymentInstruction
from apps.people.models import Party
from apps.properties.models import Property
from apps.rentals.models import Rental


class AccountingPeriod(DomainModel):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Abierto"
        CLOSED = "CLOSED", "Cerrado"

    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="accounting_periods")
    period_start = models.DateField()
    period_end = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    closed_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="closed_accounting_periods"
    )
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["organization", "period_start", "period_end"], name="uq_accounting_period"),
            models.CheckConstraint(condition=models.Q(period_end__gte=models.F("period_start")), name="ck_period_dates"),
        ]


class BillingPeriod(DomainModel):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Abierto"
        PARTIALLY_PAID = "PARTIALLY_PAID", "Pago parcial"
        PAID = "PAID", "Pagado"
        OVERDUE = "OVERDUE", "En mora"
        CLOSED = "CLOSED", "Cerrado"

    rental = models.ForeignKey(Rental, on_delete=models.PROTECT, related_name="billing_periods")
    period_start = models.DateField()
    period_end = models.DateField()
    due_date = models.DateField(db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["rental", "period_start", "period_end"], name="uq_rental_billing_period"),
            models.CheckConstraint(condition=models.Q(period_end__gte=models.F("period_start")), name="ck_billing_dates"),
        ]
        indexes = [models.Index(fields=["status", "due_date"])]


class Charge(ArchivableModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        PARTIAL = "PARTIAL", "Parcial"
        PAID = "PAID", "Pagado"
        CANCELLED = "CANCELLED", "Cancelado"
        WRITTEN_OFF = "WRITTEN_OFF", "Castigado"

    billing_period = models.ForeignKey(BillingPeriod, on_delete=models.PROTECT, related_name="charges")
    party = models.ForeignKey(Party, on_delete=models.PROTECT, related_name="charges")
    financial_concept = models.ForeignKey(FinancialConcept, on_delete=models.PROTECT, related_name="charges")
    description = models.CharField(max_length=255)
    original_amount = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    outstanding_amount = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    due_date = models.DateField(db_index=True)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING, db_index=True)
    visible_to_owner = models.BooleanField(default=True)
    source_content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, null=True, blank=True)
    source_object_id = models.UUIDField(null=True, blank=True, db_index=True)
    source_object = GenericForeignKey("source_content_type", "source_object_id")

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(outstanding_amount__lte=models.F("original_amount")), name="ck_charge_balance"
            )
        ]
        indexes = [models.Index(fields=["party", "status", "due_date"])]


class ChargeAdjustment(ArchivableModel):
    class AdjustmentType(models.TextChoices):
        DEBIT = "DEBIT", "Débito"
        CREDIT = "CREDIT", "Crédito"
        DISCOUNT = "DISCOUNT", "Descuento"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        APPROVED = "APPROVED", "Aprobado"
        REJECTED = "REJECTED", "Rechazado"
        VOIDED = "VOIDED", "Anulado"

    charge = models.ForeignKey(Charge, on_delete=models.PROTECT, related_name="adjustments")
    adjustment_type = models.CharField(max_length=10, choices=AdjustmentType.choices)
    amount = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    reason = models.TextField()
    support_document = models.ForeignKey(Document, on_delete=models.PROTECT, null=True, blank=True)
    visible_to_owner = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    approved_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_charge_adjustments"
    )
    approved_at = models.DateTimeField(null=True, blank=True)


class LateFeeAssessment(ArchivableModel):
    class Status(models.TextChoices):
        CALCULATED = "CALCULATED", "Calculado"
        APPLIED = "APPLIED", "Aplicado"
        VOIDED = "VOIDED", "Anulado"

    charge = models.ForeignKey(Charge, on_delete=models.PROTECT, related_name="late_fee_assessments")
    policy_version = models.ForeignKey(LateFeePolicy, on_delete=models.PROTECT, related_name="assessments")
    calculated_from = models.DateField()
    calculated_through = models.DateField()
    days_late = models.PositiveIntegerField()
    base_amount = models.DecimalField(max_digits=16, decimal_places=2)
    rate = models.DecimalField(max_digits=9, decimal_places=6)
    calculated_amount = models.DecimalField(max_digits=16, decimal_places=2)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.CALCULATED)
    calculation_snapshot = models.JSONField(default=dict)


class Payment(ArchivableModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        CONFIRMED = "CONFIRMED", "Confirmado"
        REVERSED = "REVERSED", "Reversado"

    payer = models.ForeignKey(Party, on_delete=models.PROTECT, related_name="payments")
    rental = models.ForeignKey(Rental, on_delete=models.PROTECT, null=True, blank=True, related_name="payments")
    received_at = models.DateTimeField(db_index=True)
    amount = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    currency = models.CharField(max_length=3, default="COP")
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT, related_name="payments")
    reference = models.CharField(max_length=150, blank=True)
    destination_account = models.ForeignKey(BankAccount, on_delete=models.PROTECT, null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING, db_index=True)
    notes = models.TextField(blank=True)
    registered_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, related_name="registered_payments"
    )
    confirmed_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="confirmed_payments"
    )
    confirmed_at = models.DateTimeField(null=True, blank=True)


class PaymentAllocation(DomainModel):
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name="allocations")
    charge = models.ForeignKey(Charge, on_delete=models.PROTECT, related_name="payment_allocations")
    amount = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])

    class Meta:
        constraints = [models.UniqueConstraint(fields=["payment", "charge"], name="uq_payment_charge_allocation")]


class Receipt(ArchivableModel):
    class ReceiptType(models.TextChoices):
        TENANT = "TENANT", "Arrendatario"
        OWNER_SETTLEMENT = "OWNER_SETTLEMENT", "Recaudo propietario"
        OWNER_CASH = "OWNER_CASH", "Caja propietario"
        PROVIDER = "PROVIDER", "Proveedor"
        OTHER = "OTHER", "Otro"

    class Status(models.TextChoices):
        ISSUED = "ISSUED", "Emitido"
        VOIDED = "VOIDED", "Anulado"
        REPLACED = "REPLACED", "Reemplazado"

    organization = models.ForeignKey(Organization, on_delete=models.PROTECT, related_name="receipts")
    office = models.ForeignKey(Office, on_delete=models.PROTECT, null=True, blank=True, related_name="receipts")
    receipt_type = models.CharField(max_length=20, choices=ReceiptType.choices)
    number = models.CharField(max_length=50)
    party = models.ForeignKey(Party, on_delete=models.PROTECT, related_name="receipts")
    issued_at = models.DateTimeField(db_index=True)
    currency = models.CharField(max_length=3, default="COP")
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ISSUED, db_index=True)
    total = models.DecimalField(max_digits=16, decimal_places=2)
    related_receipt = models.ForeignKey("self", on_delete=models.PROTECT, null=True, blank=True, related_name="related")
    current_version = models.ForeignKey(
        "ReceiptVersion", on_delete=models.SET_NULL, null=True, blank=True, related_name="current_for_receipts"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["organization", "receipt_type", "number"], name="uq_receipt_number")
        ]
        ordering = ["-issued_at"]


class ReceiptPayment(DomainModel):
    receipt = models.ForeignKey(Receipt, on_delete=models.PROTECT, related_name="receipt_payments")
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name="payment_receipts")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["receipt", "payment"], name="uq_receipt_payment")]


class ReceiptVersion(DomainModel):
    receipt = models.ForeignKey(Receipt, on_delete=models.PROTECT, related_name="versions")
    version_number = models.PositiveIntegerField()
    snapshot_data = models.JSONField(default=dict)
    change_reason = models.TextField(blank=True)
    rendered_document = models.ForeignKey(Document, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["receipt", "version_number"], name="uq_receipt_version_number")
        ]


class ReceiptVersionLine(DomainModel):
    receipt_version = models.ForeignKey(ReceiptVersion, on_delete=models.PROTECT, related_name="lines")
    concept = models.ForeignKey(FinancialConcept, on_delete=models.PROTECT, null=True, blank=True)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=1)
    unit_value = models.DecimalField(max_digits=16, decimal_places=2)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    source_content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, null=True, blank=True)
    source_object_id = models.UUIDField(null=True, blank=True)
    source_object = GenericForeignKey("source_content_type", "source_object_id")
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]


class OwnerSettlement(ArchivableModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Borrador"
        PENDING_REVIEW = "PENDING_REVIEW", "Pendiente de revisión"
        APPROVED = "APPROVED", "Aprobado"
        PAID = "PAID", "Pagado"
        VOIDED = "VOIDED", "Anulado"

    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, related_name="settlements")
    period_start = models.DateField()
    period_end = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)
    gross_income = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    administration_fees = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    repair_deductions = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    owner_funds_applied = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    net_payable = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    approved_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_owner_settlements"
    )
    approved_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["owner", "period_start", "period_end"], name="uq_owner_settlement_period"),
            models.CheckConstraint(condition=models.Q(period_end__gte=models.F("period_start")), name="ck_settlement_dates"),
        ]


class OwnerSettlementLine(DomainModel):
    class LineType(models.TextChoices):
        INCOME = "INCOME", "Ingreso"
        DEDUCTION = "DEDUCTION", "Deducción"
        RETENTION = "RETENTION", "Retención"
        ADJUSTMENT = "ADJUSTMENT", "Ajuste"

    settlement = models.ForeignKey(OwnerSettlement, on_delete=models.PROTECT, related_name="lines")
    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name="settlement_lines")
    rental = models.ForeignKey(Rental, on_delete=models.PROTECT, null=True, blank=True, related_name="settlement_lines")
    financial_concept = models.ForeignKey(FinancialConcept, on_delete=models.PROTECT)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    line_type = models.CharField(max_length=12, choices=LineType.choices)
    source_content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, null=True, blank=True)
    source_object_id = models.UUIDField(null=True, blank=True)
    source_object = GenericForeignKey("source_content_type", "source_object_id")


class OwnerDisbursement(ArchivableModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        PAID = "PAID", "Pagado"
        REVERSED = "REVERSED", "Reversado"

    settlement = models.ForeignKey(OwnerSettlement, on_delete=models.PROTECT, related_name="disbursements")
    payment_instruction = models.ForeignKey(OwnerPaymentInstruction, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    paid_at = models.DateTimeField(null=True, blank=True)
    reference = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    support_document = models.ForeignKey(Document, on_delete=models.PROTECT, null=True, blank=True)


class OwnerFundAccount(ArchivableModel):
    owner = models.OneToOneField(Owner, on_delete=models.PROTECT, related_name="fund_account")
    currency = models.CharField(max_length=3, default="COP")


class OwnerFundMovement(DomainModel):
    class MovementType(models.TextChoices):
        CREDIT = "CREDIT", "Ingreso"
        DEBIT = "DEBIT", "Egreso"
        RESERVATION = "RESERVATION", "Reserva"
        RELEASE = "RELEASE", "Liberación"
        REVERSAL = "REVERSAL", "Reversión"

    account = models.ForeignKey(OwnerFundAccount, on_delete=models.PROTECT, related_name="movements")
    movement_type = models.CharField(max_length=12, choices=MovementType.choices)
    amount = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    occurred_at = models.DateTimeField(db_index=True)
    financial_concept = models.ForeignKey(FinancialConcept, on_delete=models.PROTECT)
    receipt = models.ForeignKey(Receipt, on_delete=models.PROTECT, null=True, blank=True, related_name="fund_movements")
    notes = models.TextField(blank=True)
    source_content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT, null=True, blank=True)
    source_object_id = models.UUIDField(null=True, blank=True)
    source_object = GenericForeignKey("source_content_type", "source_object_id")
