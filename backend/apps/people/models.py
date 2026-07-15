from django.db import models

from apps.catalogs.models import (
    City,
    Country,
    Department,
    IdentificationType,
    Neighborhood,
    ProviderSpecialty,
)
from apps.core.models import ArchivableModel, DomainModel


class Party(ArchivableModel):
    class PartyType(models.TextChoices):
        NATURAL = "NATURAL", "Persona natural"
        LEGAL = "LEGAL", "Persona jurídica"

    party_type = models.CharField(max_length=10, choices=PartyType.choices)
    identification_type = models.ForeignKey(IdentificationType, on_delete=models.PROTECT, related_name="parties")
    identification_number = models.CharField(max_length=50)
    verification_digit = models.CharField(max_length=2, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    second_last_name = models.CharField(max_length=100, blank=True)
    business_name = models.CharField(max_length=255, blank=True)
    display_name = models.CharField(max_length=255, blank=True, db_index=True)
    birth_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["identification_type", "identification_number"],
                name="uq_party_identification",
            ),
            models.CheckConstraint(
                condition=models.Q(party_type="NATURAL", first_name__gt="")
                | models.Q(party_type="LEGAL", business_name__gt=""),
                name="ck_party_name_for_type",
            ),
        ]
        indexes = [models.Index(fields=["display_name"]), models.Index(fields=["identification_number"])]
        ordering = ["display_name"]
        verbose_name = "Persona o empresa"

    def save(self, *args, **kwargs):
        if self.party_type == self.PartyType.LEGAL:
            self.display_name = self.business_name.strip()
        elif not self.display_name:
            self.display_name = " ".join(
                filter(None, [self.first_name, self.middle_name, self.last_name, self.second_last_name])
            ).strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.display_name


class PartyIdentification(DomainModel):
    party = models.ForeignKey(Party, on_delete=models.PROTECT, related_name="identifications")
    identification_type = models.ForeignKey(IdentificationType, on_delete=models.PROTECT)
    number = models.CharField(max_length=50)
    issue_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    issue_place = models.CharField(max_length=150, blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["identification_type", "number"], name="uq_party_extra_identification"),
            models.UniqueConstraint(
                fields=["party"], condition=models.Q(is_primary=True), name="uq_party_one_primary_identification"
            ),
        ]


class PartyPhone(DomainModel):
    class PhoneType(models.TextChoices):
        MOBILE = "MOBILE", "Celular"
        HOME = "HOME", "Residencia"
        WORK = "WORK", "Trabajo"
        OTHER = "OTHER", "Otro"

    party = models.ForeignKey(Party, on_delete=models.PROTECT, related_name="phones")
    phone_type = models.CharField(max_length=10, choices=PhoneType.choices)
    country_code = models.CharField(max_length=5, default="+57")
    number = models.CharField(max_length=30)
    extension = models.CharField(max_length=10, blank=True)
    is_primary = models.BooleanField(default=False)
    allows_notifications = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["party", "country_code", "number"], name="uq_party_phone"),
            models.UniqueConstraint(fields=["party"], condition=models.Q(is_primary=True), name="uq_party_primary_phone"),
        ]


class PartyEmail(DomainModel):
    party = models.ForeignKey(Party, on_delete=models.PROTECT, related_name="emails")
    email = models.EmailField()
    is_primary = models.BooleanField(default=False)
    allows_notifications = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["party", "email"], name="uq_party_email"),
            models.UniqueConstraint(fields=["party"], condition=models.Q(is_primary=True), name="uq_party_primary_email"),
        ]


class PartyAddress(DomainModel):
    class AddressType(models.TextChoices):
        HOME = "HOME", "Residencia"
        WORK = "WORK", "Trabajo"
        PAYMENT = "PAYMENT", "Entrega de pagos"
        OTHER = "OTHER", "Otra"

    party = models.ForeignKey(Party, on_delete=models.PROTECT, related_name="addresses")
    address_type = models.CharField(max_length=10, choices=AddressType.choices)
    address_line = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.PROTECT, null=True, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    notes = models.TextField(blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["party"], condition=models.Q(is_primary=True), name="uq_party_primary_address")
        ]


class ProviderProfile(ArchivableModel):
    class ProviderKind(models.TextChoices):
        CONTRACTOR = "CONTRACTOR", "Maestro o contratista"
        COMPANY = "COMPANY", "Empresa"
        HARDWARE_STORE = "HARDWARE_STORE", "Ferretería"
        OTHER = "OTHER", "Otro"

    party = models.OneToOneField(Party, on_delete=models.PROTECT, related_name="provider_profile")
    provider_kind = models.CharField(max_length=20, choices=ProviderKind.choices)
    specialties = models.ManyToManyField(ProviderSpecialty, blank=True, related_name="providers")
    tax_responsibility = models.CharField(max_length=100, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return str(self.party)
