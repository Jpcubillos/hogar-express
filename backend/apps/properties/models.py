from decimal import Decimal

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.catalogs.models import (
    City,
    Country,
    Department,
    InventoryCategory,
    InventoryConcept,
    MeasureUnit,
    Neighborhood,
    PropertyType,
    UtilityProvider,
    UtilityType,
)
from apps.configuration.models import AdministrationFeePlan
from apps.core.models import ArchivableModel, DomainModel
from apps.owners.models import Owner


class Property(ArchivableModel):
    class OperationalStatus(models.TextChoices):
        ACTIVE = "ACTIVE", "Activo"
        PAUSED = "PAUSED", "Pausado"
        RETIRED = "RETIRED", "Retirado"

    internal_code = models.CharField(max_length=50, unique=True)
    property_type = models.ForeignKey(PropertyType, on_delete=models.PROTECT, related_name="properties")
    owners = models.ManyToManyField(Owner, through="PropertyOwnership", related_name="properties")
    address_line = models.CharField(max_length=255, db_index=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name="properties")
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name="properties")
    city = models.ForeignKey(City, on_delete=models.PROTECT, related_name="properties")
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.PROTECT, related_name="properties")
    unit_number = models.CharField(max_length=50, blank=True)
    building_name = models.CharField(max_length=150, blank=True)
    cadastral_number = models.CharField(max_length=100, blank=True, db_index=True)
    real_estate_registration = models.CharField(max_length=100, blank=True, db_index=True)
    stratum = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(6)])
    private_area = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    built_area = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    land_area = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    bedrooms = models.PositiveSmallIntegerField(null=True, blank=True)
    bathrooms = models.PositiveSmallIntegerField(null=True, blank=True)
    parking_spaces = models.PositiveSmallIntegerField(default=0)
    operational_status = models.CharField(
        max_length=10, choices=OperationalStatus.choices, default=OperationalStatus.ACTIVE, db_index=True
    )
    description = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)

    class Meta:
        ordering = ["internal_code"]
        indexes = [
            models.Index(fields=["city", "neighborhood"]),
            models.Index(fields=["property_type", "operational_status"]),
        ]
        verbose_name = "Inmueble"

    def __str__(self):
        unit = f" {self.unit_number}" if self.unit_number else ""
        return f"{self.internal_code} - {self.address_line}{unit}"


class PropertyOwnership(DomainModel):
    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name="ownerships")
    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, related_name="ownerships")
    ownership_percentage = models.DecimalField(
        max_digits=7, decimal_places=4, validators=[MinValueValidator(Decimal("0.0001")), MaxValueValidator(100)]
    )
    is_primary = models.BooleanField(default=False)
    valid_from = models.DateField()
    valid_to = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["property", "owner", "valid_from"], name="uq_property_owner_period"),
            models.UniqueConstraint(
                fields=["property"],
                condition=models.Q(is_primary=True, valid_to__isnull=True),
                name="uq_property_primary_owner",
            ),
            models.CheckConstraint(
                condition=models.Q(valid_to__isnull=True) | models.Q(valid_to__gte=models.F("valid_from")),
                name="ck_ownership_valid_dates",
            ),
        ]


class PropertyLevel(DomainModel):
    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name="levels")
    label = models.CharField(max_length=100)
    level_from = models.SmallIntegerField(null=True, blank=True)
    level_to = models.SmallIntegerField(null=True, blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["display_order", "level_from"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(level_to__isnull=True) | models.Q(level_to__gte=models.F("level_from")),
                name="ck_property_level_range",
            )
        ]


class RentalListing(ArchivableModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Borrador"
        AVAILABLE = "AVAILABLE", "Disponible"
        PAUSED = "PAUSED", "Pausado"
        LEASED = "LEASED", "Arrendado"
        WITHDRAWN = "WITHDRAWN", "Retirado"

    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name="rental_listings")
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT, db_index=True)
    asking_rent = models.DecimalField(max_digits=16, decimal_places=2, validators=[MinValueValidator(0)])
    administration_amount = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    administration_fee_plan = models.ForeignKey(
        AdministrationFeePlan, on_delete=models.PROTECT, null=True, blank=True, related_name="rental_listings"
    )
    available_from = models.DateField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    withdrawn_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["property"],
                condition=models.Q(status__in=["DRAFT", "AVAILABLE", "PAUSED"]),
                name="uq_property_open_rental_listing",
            )
        ]


class PropertyUtilityAccount(ArchivableModel):
    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name="utility_accounts")
    utility_type = models.ForeignKey(UtilityType, on_delete=models.PROTECT, related_name="property_accounts")
    provider = models.ForeignKey(UtilityProvider, on_delete=models.PROTECT, related_name="property_accounts")
    contract_number = models.CharField(max_length=100)
    meter_number = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["provider", "contract_number"], name="uq_utility_contract_provider")
        ]


class UtilityEvent(DomainModel):
    class EventType(models.TextChoices):
        INSPECTION = "INSPECTION", "Revisión"
        METER_CHANGE = "METER_CHANGE", "Cambio de contador"
        REPAIR = "REPAIR", "Reparación"
        READING = "READING", "Lectura"

    utility_account = models.ForeignKey(PropertyUtilityAccount, on_delete=models.PROTECT, related_name="events")
    event_type = models.CharField(max_length=20, choices=EventType.choices)
    occurred_on = models.DateField(db_index=True)
    next_due_on = models.DateField(null=True, blank=True, db_index=True)
    old_meter_number = models.CharField(max_length=100, blank=True)
    new_meter_number = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    performed_by = models.CharField(max_length=255, blank=True)


class PropertyNote(DomainModel):
    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name="notes")
    note_type = models.CharField(max_length=50, blank=True, db_index=True)
    text = models.TextField()
    is_pinned = models.BooleanField(default=False)
    visible_until = models.DateField(null=True, blank=True)


class PropertyInventory(DomainModel):
    class InventoryType(models.TextChoices):
        INITIAL = "INITIAL", "Inicial"
        DELIVERY = "DELIVERY", "Entrega"
        RETURN = "RETURN", "Devolución"
        PERIODIC = "PERIODIC", "Periódico"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Borrador"
        COMPLETED = "COMPLETED", "Completado"
        SIGNED = "SIGNED", "Firmado"
        VOIDED = "VOIDED", "Anulado"

    property = models.ForeignKey(Property, on_delete=models.PROTECT, related_name="inventories")
    rental = models.ForeignKey("rentals.Rental", on_delete=models.PROTECT, null=True, blank=True, related_name="inventories")
    inventory_type = models.CharField(max_length=10, choices=InventoryType.choices)
    inspection_date = models.DateField(db_index=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    general_condition = models.TextField(blank=True)
    observations = models.TextField(blank=True)
    completed_by = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="completed_inventories"
    )
    signed_at = models.DateTimeField(null=True, blank=True)


class InventoryItem(DomainModel):
    class Condition(models.TextChoices):
        GOOD = "GOOD", "Bueno"
        FAIR = "FAIR", "Regular"
        POOR = "POOR", "Malo"
        MISSING = "MISSING", "Faltante"
        DAMAGED = "DAMAGED", "Dañado"

    inventory = models.ForeignKey(PropertyInventory, on_delete=models.PROTECT, related_name="items")
    category = models.ForeignKey(InventoryCategory, on_delete=models.PROTECT)
    concept = models.ForeignKey(InventoryConcept, on_delete=models.PROTECT, null=True, blank=True)
    custom_name = models.CharField(max_length=150, blank=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=1, validators=[MinValueValidator(0)])
    unit = models.ForeignKey(MeasureUnit, on_delete=models.PROTECT, null=True, blank=True)
    condition = models.CharField(max_length=10, choices=Condition.choices)
    description = models.TextField(blank=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "category", "custom_name"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(concept__isnull=False) | ~models.Q(custom_name=""), name="ck_inventory_item_name"
            )
        ]
