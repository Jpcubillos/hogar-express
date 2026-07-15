from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.core.models import ArchivableModel, DomainModel
from apps.people.models import Party
from apps.properties.models import Property


class SaleListing(ArchivableModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Borrador"
        AVAILABLE = "AVAILABLE", "Disponible"
        RESERVED = "RESERVED", "Reservado"
        NEGOTIATION = "NEGOTIATION", "En negociación"
        SOLD = "SOLD", "Vendido"
        WITHDRAWN = "WITHDRAWN", "Retirado"

    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name="sale_listings")
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT, db_index=True)
    minimum_price = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    maximum_price = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    commercial_appraisal = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    cadastral_appraisal = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    has_mortgage = models.BooleanField(default=False)
    mortgage_entity = models.CharField(max_length=180, blank=True)
    mortgage_balance = models.DecimalField(max_digits=16, decimal_places=2, null=True, blank=True)
    available_from = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(maximum_price__gte=models.F("minimum_price")), name="ck_sale_price_range"
            ),
            models.UniqueConstraint(
                fields=["property"],
                condition=models.Q(status__in=["DRAFT", "AVAILABLE", "RESERVED", "NEGOTIATION"]),
                name="uq_property_open_sale_listing",
            ),
        ]


class SaleAssignment(DomainModel):
    sale_listing = models.ForeignKey(SaleListing, on_delete=models.PROTECT, related_name="assignments")
    advisor = models.ForeignKey("accounts.User", on_delete=models.PROTECT, related_name="sale_assignments")
    assigned_at = models.DateTimeField()
    unassigned_at = models.DateTimeField(null=True, blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sale_listing"],
                condition=models.Q(is_primary=True, unassigned_at__isnull=True),
                name="uq_sale_primary_advisor",
            )
        ]


class BuyerInterest(ArchivableModel):
    class Status(models.TextChoices):
        INTERESTED = "INTERESTED", "Interesado"
        VISIT_SCHEDULED = "VISIT_SCHEDULED", "Visita programada"
        OFFERED = "OFFERED", "Con oferta"
        DISCARDED = "DISCARDED", "Descartado"

    sale_listing = models.ForeignKey(SaleListing, on_delete=models.PROTECT, related_name="buyer_interests")
    buyer = models.ForeignKey(Party, on_delete=models.PROTECT, related_name="buyer_interests")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INTERESTED)
    source = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["sale_listing", "buyer"], name="uq_sale_buyer_interest")
        ]


class SaleOffer(ArchivableModel):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        ACCEPTED = "ACCEPTED", "Aceptada"
        REJECTED = "REJECTED", "Rechazada"
        WITHDRAWN = "WITHDRAWN", "Retirada"
        EXPIRED = "EXPIRED", "Vencida"

    buyer_interest = models.ForeignKey(BuyerInterest, on_delete=models.PROTECT, related_name="offers")
    amount = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    offered_at = models.DateTimeField()
    expiration_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    conditions = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["buyer_interest"], condition=models.Q(status="ACCEPTED"), name="uq_buyer_interest_accepted_offer"
            )
        ]


class SaleTransaction(ArchivableModel):
    class Status(models.TextChoices):
        NEGOTIATION = "NEGOTIATION", "Negociación"
        DOCUMENTATION = "DOCUMENTATION", "Documentación"
        SIGNING = "SIGNING", "Firma"
        CLOSED = "CLOSED", "Cerrada"
        CANCELLED = "CANCELLED", "Cancelada"

    sale_listing = models.OneToOneField(SaleListing, on_delete=models.PROTECT, related_name="transaction")
    accepted_offer = models.OneToOneField(SaleOffer, on_delete=models.PROTECT, related_name="transaction")
    buyer = models.ForeignKey(Party, on_delete=models.PROTECT, related_name="purchases")
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.NEGOTIATION, db_index=True)
    agreed_price = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(Decimal("0.01"))])
    agreement_date = models.DateField()
    deed_date = models.DateField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)


class SaleCommission(ArchivableModel):
    class CalculationType(models.TextChoices):
        PERCENTAGE = "PERCENTAGE", "Porcentaje"
        FIXED = "FIXED", "Valor fijo"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        APPROVED = "APPROVED", "Aprobada"
        PAID = "PAID", "Pagada"
        VOIDED = "VOIDED", "Anulada"

    sale_transaction = models.ForeignKey(SaleTransaction, on_delete=models.PROTECT, related_name="commissions")
    beneficiary_user = models.ForeignKey(
        "accounts.User", on_delete=models.PROTECT, null=True, blank=True, related_name="sale_commissions"
    )
    beneficiary_party = models.ForeignKey(
        Party, on_delete=models.PROTECT, null=True, blank=True, related_name="sale_commissions"
    )
    calculation_type = models.CharField(max_length=12, choices=CalculationType.choices)
    base_amount = models.DecimalField(max_digits=16, decimal_places=2)
    percentage = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(models.Q(beneficiary_user__isnull=False, beneficiary_party__isnull=True)
                           | models.Q(beneficiary_user__isnull=True, beneficiary_party__isnull=False)),
                name="ck_sale_commission_beneficiary",
            )
        ]


class SaleStatusHistory(DomainModel):
    sale_listing = models.ForeignKey(SaleListing, on_delete=models.PROTECT, related_name="status_history")
    previous_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20)
    reason = models.TextField(blank=True)
    changed_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, related_name="sale_status_changes"
    )
    changed_at = models.DateTimeField(auto_now_add=True, db_index=True)
