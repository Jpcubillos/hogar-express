from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.catalogs.models import MeasureUnit, PaymentMethod, RepairCategory
from apps.core.models import ArchivableModel, DomainModel
from apps.documents.models import Document
from apps.payments.models import Charge, OwnerSettlementLine, Receipt
from apps.people.models import Party, ProviderProfile
from apps.properties.models import Property
from apps.rentals.models import Rental


class PropertyIssue(ArchivableModel):
    class Priority(models.TextChoices):
        LOW = "LOW", "Baja"
        MEDIUM = "MEDIUM", "Media"
        HIGH = "HIGH", "Alta"
        URGENT = "URGENT", "Urgente"

    class Status(models.TextChoices):
        REPORTED = "REPORTED", "Reportada"
        IN_REVIEW = "IN_REVIEW", "En revisión"
        DISMISSED = "DISMISSED", "No procede"
        CONVERTED = "CONVERTED", "Convertida en orden"
        CLOSED = "CLOSED", "Cerrada"

    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name="issues")
    rental = models.ForeignKey(Rental, on_delete=models.PROTECT, null=True, blank=True, related_name="property_issues")
    title = models.CharField(max_length=180)
    description = models.TextField()
    category = models.ForeignKey(RepairCategory, on_delete=models.PROTECT, related_name="issues")
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM, db_index=True)
    reported_at = models.DateTimeField(db_index=True)
    reported_by_user = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="reported_property_issues"
    )
    reported_by_party = models.ForeignKey(
        Party, on_delete=models.SET_NULL, null=True, blank=True, related_name="reported_property_issues"
    )
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.REPORTED, db_index=True)
    review_notes = models.TextField(blank=True)
    closed_reason = models.TextField(blank=True)

    class Meta:
        ordering = ["-reported_at"]
        indexes = [models.Index(fields=["property", "status"])]


class RepairOrder(ArchivableModel):
    class Status(models.TextChoices):
        REPORTED = "REPORTED", "Reportada"
        IN_REVIEW = "IN_REVIEW", "En revisión"
        PENDING_QUOTE = "PENDING_QUOTE", "Pendiente de cotización"
        PENDING_APPROVAL = "PENDING_APPROVAL", "Pendiente de aprobación"
        APPROVED = "APPROVED", "Aprobada"
        SCHEDULED = "SCHEDULED", "Programada"
        IN_PROGRESS = "IN_PROGRESS", "En progreso"
        COMPLETED = "COMPLETED", "Terminada"
        CLOSED = "CLOSED", "Cerrada"
        CANCELLED = "CANCELLED", "Cancelada"

    issue = models.ForeignKey(PropertyIssue, on_delete=models.PROTECT, null=True, blank=True, related_name="repair_orders")
    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name="repairs")
    rental = models.ForeignKey(Rental, on_delete=models.PROTECT, null=True, blank=True, related_name="repairs")
    order_number = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=180)
    description = models.TextField()
    category = models.ForeignKey(RepairCategory, on_delete=models.PROTECT, related_name="repair_orders")
    priority = models.CharField(max_length=10, choices=PropertyIssue.Priority.choices, default=PropertyIssue.Priority.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REPORTED, db_index=True)
    internal_responsible = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="responsible_repairs"
    )
    scheduled_start = models.DateTimeField(null=True, blank=True, db_index=True)
    scheduled_end = models.DateTimeField(null=True, blank=True)
    actual_start = models.DateTimeField(null=True, blank=True)
    actual_end = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    verification_notes = models.TextField(blank=True)
    verified_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="verified_repairs"
    )
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["property", "status"]),
            models.Index(fields=["internal_responsible", "status"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(scheduled_end__isnull=True)
                | models.Q(scheduled_start__isnull=True)
                | models.Q(scheduled_end__gte=models.F("scheduled_start")),
                name="ck_repair_schedule_dates",
            )
        ]

    def __str__(self):
        return f"{self.order_number} - {self.title}"


class RepairStatusHistory(DomainModel):
    repair = models.ForeignKey(RepairOrder, on_delete=models.PROTECT, related_name="status_history")
    previous_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20)
    reason = models.TextField(blank=True)
    changed_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, related_name="repair_status_changes"
    )
    changed_at = models.DateTimeField(auto_now_add=True, db_index=True)


class RepairAssignment(ArchivableModel):
    class Status(models.TextChoices):
        ASSIGNED = "ASSIGNED", "Asignado"
        ACCEPTED = "ACCEPTED", "Aceptado"
        DECLINED = "DECLINED", "Rechazado"
        COMPLETED = "COMPLETED", "Completado"
        CANCELLED = "CANCELLED", "Cancelado"

    repair = models.ForeignKey(RepairOrder, on_delete=models.PROTECT, related_name="assignments")
    provider = models.ForeignKey(ProviderProfile, on_delete=models.PROTECT, related_name="repair_assignments")
    assigned_at = models.DateTimeField()
    accepted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ASSIGNED)
    scope = models.TextField()


class RepairQuote(ArchivableModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Borrador"
        SUBMITTED = "SUBMITTED", "Presentada"
        SELECTED = "SELECTED", "Seleccionada"
        REJECTED = "REJECTED", "Rechazada"
        DISABLED = "DISABLED", "Deshabilitada"

    repair = models.ForeignKey(RepairOrder, on_delete=models.PROTECT, related_name="quotes")
    provider = models.ForeignKey(ProviderProfile, on_delete=models.PROTECT, related_name="repair_quotes")
    quote_number = models.CharField(max_length=100, blank=True)
    quoted_at = models.DateTimeField()
    valid_until = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    subtotal = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    disabled_reason = models.TextField(blank=True)
    selected_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="selected_repair_quotes"
    )
    selected_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["repair"], condition=models.Q(status="SELECTED", is_active=True), name="uq_repair_selected_quote"
            )
        ]


class RepairQuoteLine(DomainModel):
    class CostType(models.TextChoices):
        MATERIAL = "MATERIAL", "Material"
        LABOR = "LABOR", "Mano de obra"
        TRANSPORT = "TRANSPORT", "Transporte"
        OTHER = "OTHER", "Otro"

    quote = models.ForeignKey(RepairQuote, on_delete=models.PROTECT, related_name="lines")
    cost_type = models.CharField(max_length=10, choices=CostType.choices)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    unit = models.ForeignKey(MeasureUnit, on_delete=models.PROTECT, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    is_extra = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=True)
    disabled_reason = models.TextField(blank=True)


class RepairApproval(ArchivableModel):
    class Decision(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        APPROVED = "APPROVED", "Aprobada"
        REJECTED = "REJECTED", "Rechazada"

    repair = models.ForeignKey(RepairOrder, on_delete=models.PROTECT, related_name="approvals")
    approval_type = models.CharField(max_length=50)
    requested_from = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True, blank=True)
    requested_at = models.DateTimeField()
    decision = models.CharField(max_length=10, choices=Decision.choices, default=Decision.PENDING)
    decided_by_user = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="repair_decisions"
    )
    decided_by_party = models.ForeignKey(
        Party, on_delete=models.SET_NULL, null=True, blank=True, related_name="repair_decisions"
    )
    decided_at = models.DateTimeField(null=True, blank=True)
    evidence_document = models.ForeignKey(Document, on_delete=models.PROTECT, null=True, blank=True)
    notes = models.TextField(blank=True)


class RepairChangeOrder(ArchivableModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        APPROVED = "APPROVED", "Aprobado"
        REJECTED = "REJECTED", "Rechazado"
        CANCELLED = "CANCELLED", "Cancelado"

    repair = models.ForeignKey(RepairOrder, on_delete=models.PROTECT, related_name="change_orders")
    description = models.TextField()
    requested_amount = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    requested_at = models.DateTimeField()
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_repair_changes"
    )


class RepairCost(ArchivableModel):
    repair = models.ForeignKey(RepairOrder, on_delete=models.PROTECT, related_name="costs")
    quote_line = models.ForeignKey(RepairQuoteLine, on_delete=models.PROTECT, null=True, blank=True, related_name="actual_costs")
    cost_type = models.CharField(max_length=10, choices=RepairQuoteLine.CostType.choices)
    provider = models.ForeignKey(ProviderProfile, on_delete=models.PROTECT, null=True, blank=True, related_name="repair_costs")
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    unit = models.ForeignKey(MeasureUnit, on_delete=models.PROTECT, null=True, blank=True)
    unit_cost = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    incurred_on = models.DateField()
    invoice_number = models.CharField(max_length=100, blank=True)


class RepairCostAllocation(ArchivableModel):
    class ResponsibleType(models.TextChoices):
        OWNER = "OWNER", "Propietario"
        TENANT = "TENANT", "Arrendatario"
        AGENCY = "AGENCY", "Inmobiliaria"
        OTHER = "OTHER", "Otro"

    class ApplicationMethod(models.TextChoices):
        TENANT_CHARGE = "TENANT_CHARGE", "Cargo al arrendatario"
        OWNER_SETTLEMENT = "OWNER_SETTLEMENT", "Descuento al propietario"
        OWNER_FUND = "OWNER_FUND", "Fondo del propietario"
        DIRECT = "DIRECT", "Pago directo"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        SCHEDULED = "SCHEDULED", "Programada"
        APPLIED = "APPLIED", "Aplicada"
        VOIDED = "VOIDED", "Anulada"

    repair_cost = models.ForeignKey(RepairCost, on_delete=models.PROTECT, related_name="allocations")
    responsible_type = models.CharField(max_length=10, choices=ResponsibleType.choices)
    responsible_party = models.ForeignKey(Party, on_delete=models.PROTECT, null=True, blank=True)
    amount = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    percentage = models.DecimalField(
        max_digits=7, decimal_places=4, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    application_method = models.CharField(max_length=20, choices=ApplicationMethod.choices)
    installment_count = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1)])
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)


class RepairAllocationInstallment(DomainModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        APPLIED = "APPLIED", "Aplicada"
        PAID = "PAID", "Pagada"
        VOIDED = "VOIDED", "Anulada"

    allocation = models.ForeignKey(RepairCostAllocation, on_delete=models.PROTECT, related_name="installments")
    installment_number = models.PositiveSmallIntegerField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    charge = models.ForeignKey(Charge, on_delete=models.PROTECT, null=True, blank=True, related_name="repair_installments")
    settlement_line = models.ForeignKey(
        OwnerSettlementLine, on_delete=models.PROTECT, null=True, blank=True, related_name="repair_installments"
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["allocation", "installment_number"], name="uq_repair_installment_number")
        ]


class ProviderPayment(ArchivableModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        PAID = "PAID", "Pagado"
        REVERSED = "REVERSED", "Reversado"

    repair = models.ForeignKey(RepairOrder, on_delete=models.PROTECT, related_name="provider_payments")
    provider = models.ForeignKey(ProviderProfile, on_delete=models.PROTECT, related_name="payments_received")
    amount = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    paid_at = models.DateTimeField(null=True, blank=True)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    reference = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    receipt = models.ForeignKey(Receipt, on_delete=models.PROTECT, null=True, blank=True, related_name="provider_payments")


class RepairWarranty(ArchivableModel):
    repair = models.ForeignKey(RepairOrder, on_delete=models.PROTECT, related_name="warranties")
    provider = models.ForeignKey(ProviderProfile, on_delete=models.PROTECT, related_name="warranties")
    starts_on = models.DateField()
    duration_value = models.PositiveIntegerField()
    duration_unit = models.CharField(max_length=10, choices=[("DAY", "Día"), ("MONTH", "Mes"), ("YEAR", "Año")])
    expires_on = models.DateField(db_index=True)
    terms = models.TextField(blank=True)


class RepairComment(DomainModel):
    repair = models.ForeignKey(RepairOrder, on_delete=models.PROTECT, related_name="comments")
    text = models.TextField()
    is_internal = models.BooleanField(default=True)


# Compatibility for the existing API and imports.
Repair = RepairOrder
