from django.db import models

from apps.catalogs.models import Bank, PaymentMethod
from apps.core.models import ArchivableModel, DomainModel
from apps.people.models import Party, PartyAddress


class Owner(ArchivableModel):
    party = models.OneToOneField(Party, on_delete=models.PROTECT, related_name="owner_profile")
    internal_code = models.CharField(max_length=50, unique=True)
    default_payment_method = models.ForeignKey(
        PaymentMethod, on_delete=models.PROTECT, null=True, blank=True, related_name="default_owners"
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["party__display_name"]
        verbose_name = "Propietario"

    @property
    def name(self):
        return self.party.display_name

    @property
    def identification(self):
        return self.party.identification_number

    def __str__(self):
        return self.party.display_name


class BankAccount(ArchivableModel):
    class AccountType(models.TextChoices):
        SAVINGS = "SAVINGS", "Ahorros"
        CHECKING = "CHECKING", "Corriente"
        OTHER = "OTHER", "Otra"

    party = models.ForeignKey(Party, on_delete=models.PROTECT, related_name="bank_accounts")
    bank = models.ForeignKey(Bank, on_delete=models.PROTECT, related_name="accounts")
    account_type = models.CharField(max_length=10, choices=AccountType.choices)
    account_number = models.CharField(max_length=100)
    account_number_last4 = models.CharField(max_length=4, editable=False)
    holder_name = models.CharField(max_length=255)
    holder_identification = models.CharField(max_length=50)
    is_primary = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    verification_date = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["bank", "account_number"], name="uq_bank_account_number"),
            models.UniqueConstraint(
                fields=["party"], condition=models.Q(is_primary=True, is_active=True), name="uq_party_primary_bank"
            ),
        ]

    def save(self, *args, **kwargs):
        self.account_number_last4 = self.account_number[-4:]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bank} ****{self.account_number_last4}"


class OwnerPaymentInstruction(ArchivableModel):
    class InstructionType(models.TextChoices):
        BANK_TRANSFER = "BANK_TRANSFER", "Transferencia bancaria"
        CASH = "CASH", "Efectivo"
        OTHER = "OTHER", "Otro"

    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, related_name="payment_instructions")
    instruction_type = models.CharField(max_length=20, choices=InstructionType.choices)
    bank_account = models.ForeignKey(BankAccount, on_delete=models.PROTECT, null=True, blank=True)
    cash_delivery_address = models.ForeignKey(PartyAddress, on_delete=models.PROTECT, null=True, blank=True)
    instructions = models.TextField(blank=True)
    valid_from = models.DateField()
    valid_to = models.DateField(null=True, blank=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner"], condition=models.Q(is_default=True, is_active=True), name="uq_owner_default_payment"
            ),
            models.CheckConstraint(
                condition=(models.Q(instruction_type="BANK_TRANSFER", bank_account__isnull=False)
                           | models.Q(instruction_type="CASH", cash_delivery_address__isnull=False)
                           | models.Q(instruction_type="OTHER")),
                name="ck_owner_payment_destination",
            ),
            models.CheckConstraint(
                condition=models.Q(valid_to__isnull=True) | models.Q(valid_to__gte=models.F("valid_from")),
                name="ck_owner_payment_valid_dates",
            ),
        ]


class PowerOfAttorney(ArchivableModel):
    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Borrador"
        ACTIVE = "ACTIVE", "Vigente"
        EXPIRED = "EXPIRED", "Vencido"
        REVOKED = "REVOKED", "Revocado"

    owner = models.ForeignKey(Owner, on_delete=models.PROTECT, related_name="powers_of_attorney")
    representative = models.ForeignKey(Party, on_delete=models.PROTECT, related_name="represented_owners")
    scope = models.TextField()
    valid_from = models.DateField()
    valid_to = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    notes = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(valid_to__isnull=True) | models.Q(valid_to__gte=models.F("valid_from")),
                name="ck_power_valid_dates",
            )
        ]
