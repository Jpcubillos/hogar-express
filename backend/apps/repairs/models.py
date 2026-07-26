from decimal import Decimal
from datetime import timedelta

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from apps.catalogs.models import MeasureUnit, PaymentMethod, RepairCategory
from apps.core.models import ArchivableModel, DomainModel
from apps.documents.models import Document
from apps.payments.models import Charge, OwnerSettlementLine, Receipt
from apps.people.models import Party, ProviderProfile
from apps.properties.models import Property as PropertyModel
from apps.rentals.models import Rental


class RepairPriority(models.TextChoices):
    LOW = "LOW", "Baja"
    MEDIUM = "MEDIUM", "Media"
    HIGH = "HIGH", "Alta"
    CRITICAL = "CRITICAL", "Crítica"


class RepairSeverity(models.TextChoices):
    LOW = "LOW", "Baja (Cosmética / Leve)"
    MEDIUM = "MEDIUM", "Media (Funcional)"
    HIGH = "HIGH", "Alta (Dañina / Habitabilidad)"
    CRITICAL = "CRITICAL", "Crítica (Riesgo Estructural)"


class RepairType(models.TextChoices):
    CORRECTIVE = "CORRECTIVE", "Reparación Correctiva"
    PREVENTIVE = "PREVENTIVE", "Mantenimiento Preventivo"
    INSPECTION = "INSPECTION", "Inspección Técnica"
    WARRANTY = "WARRANTY", "Atención por Garantía"
    PERIODIC_MAINTENANCE = "PERIODIC_MAINTENANCE", "Mantenimiento Periódico"


class RepairIncident(ArchivableModel):
    """
    Novedad o reporte inicial de un problema en un inmueble.
    """
    class Status(models.TextChoices):
        REPORTED = "REPORTED", "Reportada"
        IN_REVIEW = "IN_REVIEW", "En revisión"
        DISMISSED = "DISMISSED", "No procede"
        CONVERTED = "CONVERTED", "Convertida en orden"
        CLOSED = "CLOSED", "Cerrada"

    property = models.ForeignKey(PropertyModel, on_delete=models.PROTECT, related_name="incidents")
    rental = models.ForeignKey(Rental, on_delete=models.PROTECT, null=True, blank=True, related_name="incidents")
    title = models.CharField(max_length=180)
    description = models.TextField()
    category = models.ForeignKey(RepairCategory, on_delete=models.PROTECT, related_name="incidents")
    priority = models.CharField(max_length=10, choices=RepairPriority.choices, default=RepairPriority.MEDIUM, db_index=True)
    severity = models.CharField(max_length=10, choices=RepairSeverity.choices, default=RepairSeverity.MEDIUM, db_index=True)
    repair_type = models.CharField(max_length=25, choices=RepairType.choices, default=RepairType.CORRECTIVE, db_index=True)
    reported_at = models.DateTimeField(default=timezone.now, db_index=True)
    reported_by_user = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="reported_incidents"
    )
    reported_by_party = models.ForeignKey(
        Party, on_delete=models.SET_NULL, null=True, blank=True, related_name="reported_incidents"
    )
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.REPORTED, db_index=True)
    review_notes = models.TextField(blank=True)
    closed_reason = models.TextField(blank=True)

    class Meta:
        ordering = ["-reported_at"]
        indexes = [models.Index(fields=["property", "status"])]

    def __str__(self):
        return f"Incidente #{self.id} - {self.title}"


class RepairOrder(ArchivableModel):
    """
    Aggregate Root del dominio de Reparaciones.
    Representa la Orden de Trabajo ejecutada.
    """
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

    incident = models.ForeignKey(RepairIncident, on_delete=models.PROTECT, null=True, blank=True, related_name="repair_orders")
    property = models.ForeignKey(PropertyModel, on_delete=models.PROTECT, related_name="repairs")
    rental = models.ForeignKey(Rental, on_delete=models.PROTECT, null=True, blank=True, related_name="repairs")
    order_number = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=180)
    description = models.TextField()
    category = models.ForeignKey(RepairCategory, on_delete=models.PROTECT, related_name="repair_orders")
    priority = models.CharField(max_length=10, choices=RepairPriority.choices, default=RepairPriority.MEDIUM, db_index=True)
    severity = models.CharField(max_length=10, choices=RepairSeverity.choices, default=RepairSeverity.MEDIUM, db_index=True)
    repair_type = models.CharField(max_length=25, choices=RepairType.choices, default=RepairType.CORRECTIVE, db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REPORTED, db_index=True)
    
    internal_responsible = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="responsible_repairs"
    )
    current_provider = models.ForeignKey(
        ProviderProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="primary_repair_orders"
    )
    sla_deadline = models.DateTimeField(null=True, blank=True, db_index=True)
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
            models.Index(fields=["current_provider", "status"]),
            models.Index(fields=["priority", "status"]),
            models.Index(fields=["sla_deadline", "status"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(scheduled_end__isnull=True)
                | models.Q(scheduled_start__isnull=True)
                | models.Q(scheduled_end__gte=models.F("scheduled_start")),
                name="ck_repair_schedule_dates",
            )
        ]

    import builtins

    @builtins.property
    def is_overdue(self) -> bool:
        """
        Calcula si el SLA de la orden está vencido.
        """
        if not self.sla_deadline or self.status in ["CLOSED", "CANCELLED", "COMPLETED"]:
            return False
        return timezone.now() > self.sla_deadline

    def save(self, *args, **kwargs):
        # Auto-calculate SLA deadline if not provided
        if not self.sla_deadline:
            base_time = self.created_at or timezone.now()
            hours_map = {
                RepairPriority.CRITICAL: 24,
                RepairPriority.HIGH: 48,
                RepairPriority.MEDIUM: 120, # 5 days
                RepairPriority.LOW: 240,   # 10 days
            }
            hours = hours_map.get(self.priority, 120)
            self.sla_deadline = base_time + timedelta(hours=hours)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_number} - {self.title}"


class RepairTask(ArchivableModel):
    """
    Sub-actividades o tareas desglosadas dentro de una Orden de Reparación.
    """
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        IN_PROGRESS = "IN_PROGRESS", "En progreso"
        COMPLETED = "COMPLETED", "Completada"
        CANCELLED = "CANCELLED", "Cancelada"

    repair_order = models.ForeignKey(RepairOrder, on_delete=models.CASCADE, related_name="tasks")
    sequence_order = models.PositiveIntegerField(default=1, db_index=True)
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    assigned_provider = models.ForeignKey(
        ProviderProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tasks"
    )
    estimated_cost = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    actual_cost = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING, db_index=True)
    scheduled_date = models.DateField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["sequence_order", "created_at"]

    def __str__(self):
        return f"Tarea #{self.sequence_order}: {self.title} ({self.repair_order.order_number})"


class RepairStatusHistory(DomainModel):
    """
    Historial inmutable de transiciones de estado de una orden.
    """
    repair = models.ForeignKey(RepairOrder, on_delete=models.CASCADE, related_name="status_history")
    previous_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20)
    reason = models.TextField(blank=True)
    changed_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, related_name="repair_status_changes"
    )
    changed_at = models.DateTimeField(auto_now_add=True, db_index=True)


class RepairQuote(ArchivableModel):
    """
    Cotización enviada por un proveedor.
    """
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Borrador"
        SUBMITTED = "SUBMITTED", "Presentada"
        SELECTED = "SELECTED", "Seleccionada"
        REJECTED = "REJECTED", "Rechazada"
        DISABLED = "DISABLED", "Deshabilitada"

    repair = models.ForeignKey(RepairOrder, on_delete=models.PROTECT, related_name="quotes")
    provider = models.ForeignKey(ProviderProfile, on_delete=models.PROTECT, related_name="repair_quotes")
    quote_number = models.CharField(max_length=100, blank=True)
    quoted_at = models.DateTimeField(default=timezone.now)
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

    def __str__(self):
        return f"Cotización #{self.quote_number or self.id} - {self.provider}"


class RepairQuoteItem(DomainModel):
    """
    Ítem desglosado de cotización (antes llamado RepairQuoteLine).
    """
    class CostType(models.TextChoices):
        MATERIAL = "MATERIAL", "Material"
        LABOR = "LABOR", "Mano de obra"
        TRANSPORT = "TRANSPORT", "Transporte"
        OTHER = "OTHER", "Otro"

    quote = models.ForeignKey(RepairQuote, on_delete=models.CASCADE, related_name="items")
    cost_type = models.CharField(max_length=10, choices=CostType.choices)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    unit = models.ForeignKey(MeasureUnit, on_delete=models.PROTECT, null=True, blank=True)
    unit_price = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    is_extra = models.BooleanField(default=False)
    is_enabled = models.BooleanField(default=True)
    disabled_reason = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)


class RepairApproval(ArchivableModel):
    """
    Registro formal y auditable de decisiones/aprobaciones.
    """
    class Decision(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        APPROVED = "APPROVED", "Aprobada"
        REJECTED = "REJECTED", "Rechazada"

    class ApprovalType(models.TextChoices):
        ADMIN = "ADMIN", "Aprobación Administración"
        OWNER = "OWNER", "Aprobación Propietario"
        MANAGER = "MANAGER", "Aprobación Gerencia"
        ACCOUNTING = "ACCOUNTING", "Aprobación Contabilidad"

    repair = models.ForeignKey(RepairOrder, on_delete=models.PROTECT, related_name="approvals")
    approval_type = models.CharField(max_length=50, choices=ApprovalType.choices, default=ApprovalType.ADMIN)
    requested_from = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True, blank=True)
    requested_at = models.DateTimeField(default=timezone.now)
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


class RepairCost(ArchivableModel):
    """
    Costo registrado (Estimado, Cotizado o Ejecutado).
    """
    class CategoryType(models.TextChoices):
        ESTIMATED = "ESTIMATED", "Estimación Rápida Inicial"
        QUOTED = "QUOTED", "Presupuestado / Cotizado"
        ACTUAL = "ACTUAL", "Ejecutado Real"

    repair = models.ForeignKey(RepairOrder, on_delete=models.PROTECT, related_name="costs")
    task = models.ForeignKey(RepairTask, on_delete=models.SET_NULL, null=True, blank=True, related_name="costs")
    quote_item = models.ForeignKey(RepairQuoteItem, on_delete=models.PROTECT, null=True, blank=True, related_name="actual_costs")
    category_type = models.CharField(max_length=10, choices=CategoryType.choices, default=CategoryType.ACTUAL)
    cost_type = models.CharField(max_length=10, choices=RepairQuoteItem.CostType.choices)
    provider = models.ForeignKey(ProviderProfile, on_delete=models.PROTECT, null=True, blank=True, related_name="repair_costs")
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    unit = models.ForeignKey(MeasureUnit, on_delete=models.PROTECT, null=True, blank=True)
    unit_cost = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    incurred_on = models.DateField(default=timezone.now)
    invoice_number = models.CharField(max_length=100, blank=True)
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True, related_name="repair_costs")


class RepairCostAllocation(ArchivableModel):
    """
    Distribución financiera del costo (Propietario / Arrendatario / Inmobiliaria).
    """
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
    """
    Cuotas desglosadas de la distribución de costo.
    """
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        APPLIED = "APPLIED", "Aplicada"
        PAID = "PAID", "Pagada"
        VOIDED = "VOIDED", "Anulada"

    allocation = models.ForeignKey(RepairCostAllocation, on_delete=models.CASCADE, related_name="installments")
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
    """
    Pagos realizados al contratista / proveedor.
    """
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
    """
    Registro de la garantía del trabajo realizado.
    """
    repair = models.ForeignKey(RepairOrder, on_delete=models.PROTECT, related_name="warranties")
    provider = models.ForeignKey(ProviderProfile, on_delete=models.PROTECT, related_name="warranties")
    starts_on = models.DateField()
    duration_value = models.PositiveIntegerField()
    duration_unit = models.CharField(max_length=10, choices=[("DAY", "Día"), ("MONTH", "Mes"), ("YEAR", "Año")])
    expires_on = models.DateField(db_index=True)
    terms = models.TextField(blank=True)


class RepairComment(DomainModel):
    """
    Comentario / Observación con adjunto opcional.
    """
    repair = models.ForeignKey(RepairOrder, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField()
    document = models.ForeignKey(Document, on_delete=models.SET_NULL, null=True, blank=True)
    is_internal = models.BooleanField(default=True)


class RepairTimelineEvent(DomainModel):
    """
    Event Stream cronológico estilo GitHub para auditoría visual.
    """
    class EventType(models.TextChoices):
        CREATED = "CREATED", "Orden Creada"
        STATUS_CHANGE = "STATUS_CHANGE", "Cambio de Estado"
        PRIORITY_CHANGE = "PRIORITY_CHANGE", "Cambio de Prioridad y SLA"
        TASK_ADDED = "TASK_ADDED", "Tarea Agregada"
        TASK_UPDATED = "TASK_UPDATED", "Tarea Actualizada"
        QUOTE_ADDED = "QUOTE_ADDED", "Cotización Recibida"
        QUOTE_SELECTED = "QUOTE_SELECTED", "Cotización Seleccionada"
        APPROVED = "APPROVED", "Aprobación Registrada"
        COST_ADDED = "COST_ADDED", "Costo Registrado"
        DOCUMENT_ATTACHED = "DOCUMENT_ATTACHED", "Soporte Adjuntado"
        COMMENT_ADDED = "COMMENT_ADDED", "Comentario Agregado"
        PAYMENT = "PAYMENT", "Pago a Proveedor"
        CLOSED = "CLOSED", "Orden Cerrada"
        CANCELLED = "CANCELLED", "Orden Cancelada"
        SYSTEM = "SYSTEM", "Evento de Sistema"

    repair = models.ForeignKey(RepairOrder, on_delete=models.CASCADE, related_name="timeline_events")
    event_type = models.CharField(max_length=25, choices=EventType.choices, default=EventType.SYSTEM)
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    performed_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True)
    occurred_at = models.DateTimeField(default=timezone.now, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-occurred_at"]


# Backwards compatibility aliases
PropertyIssue = RepairIncident
Repair = RepairOrder
RepairQuoteLine = RepairQuoteItem
