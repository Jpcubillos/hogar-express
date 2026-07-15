from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone

from apps.configuration.models import NumberSequence
from apps.configuration.services import next_document_number

from .models import (
    Charge,
    OwnerSettlement,
    Payment,
    PaymentAllocation,
    Receipt,
    ReceiptPayment,
    ReceiptVersion,
    ReceiptVersionLine,
)


@transaction.atomic
def allocate_payment(payment_id, allocations, actor=None):
    """Allocate one payment across charges while locking all affected balances."""
    payment = Payment.objects.select_for_update().get(pk=payment_id)
    requested_total = sum(Decimal(str(item["amount"])) for item in allocations)
    if requested_total > payment.amount:
        raise ValidationError("La suma aplicada no puede superar el valor del pago.")
    existing_total = payment.allocations.aggregate(total=Sum("amount"))["total"] or Decimal("0")
    if existing_total:
        raise ValidationError("El pago ya tiene aplicaciones; debe reversarse antes de reaplicarlo.")
    for item in allocations:
        amount = Decimal(str(item["amount"]))
        if amount <= 0:
            raise ValidationError("Cada aplicación debe ser mayor que cero.")
        charge = Charge.objects.select_for_update().get(pk=item["charge_id"])
        if charge.party_id != payment.payer_id:
            raise ValidationError("El pago y la obligación pertenecen a personas diferentes.")
        if amount > charge.outstanding_amount:
            raise ValidationError("La aplicación supera el saldo de una obligación.")
        PaymentAllocation.objects.create(
            payment=payment,
            charge=charge,
            amount=amount,
            created_by=actor,
            updated_by=actor,
        )
        charge.outstanding_amount -= amount
        charge.status = Charge.Status.PAID if charge.outstanding_amount == 0 else Charge.Status.PARTIAL
        charge.updated_by = actor
        charge.save(update_fields=["outstanding_amount", "status", "updated_by", "updated_at"])
    payment.status = Payment.Status.CONFIRMED
    payment.confirmed_by = actor
    payment.confirmed_at = timezone.now()
    payment.updated_by = actor
    payment.save(update_fields=["status", "confirmed_by", "confirmed_at", "updated_by", "updated_at"])
    return payment


@transaction.atomic
def issue_payment_receipt(payment_id, organization_id, office_id, lines, actor=None):
    payment = Payment.objects.select_for_update().select_related("payer").get(pk=payment_id)
    if payment.status != Payment.Status.CONFIRMED:
        raise ValidationError("Solo se puede generar recibo para un pago confirmado.")
    sequence = NumberSequence.objects.get(
        organization_id=organization_id, office_id=office_id, document_kind=Receipt.ReceiptType.TENANT
    )
    number = next_document_number(sequence.id, payment.received_at)
    total = sum(Decimal(str(line["amount"])) for line in lines)
    if total != payment.amount:
        raise ValidationError("El total del recibo debe coincidir con el valor del pago.")
    receipt = Receipt.objects.create(
        organization_id=organization_id,
        office_id=office_id,
        receipt_type=Receipt.ReceiptType.TENANT,
        number=number,
        party=payment.payer,
        issued_at=timezone.now(),
        total=total,
        created_by=actor,
        updated_by=actor,
    )
    version = ReceiptVersion.objects.create(
        receipt=receipt,
        version_number=1,
        snapshot_data={"payer": payment.payer.display_name, "payment_id": str(payment.id)},
        created_by=actor,
        updated_by=actor,
    )
    for order, line in enumerate(lines):
        ReceiptVersionLine.objects.create(
            receipt_version=version,
            concept_id=line.get("concept_id"),
            description=line["description"],
            quantity=line.get("quantity", 1),
            unit_value=line.get("unit_value", line["amount"]),
            amount=line["amount"],
            display_order=order,
            created_by=actor,
            updated_by=actor,
        )
    receipt.current_version = version
    receipt.save(update_fields=["current_version", "updated_at"])
    ReceiptPayment.objects.create(receipt=receipt, payment=payment, created_by=actor, updated_by=actor)
    return receipt


def recalculate_owner_settlement(settlement_id):
    settlement = OwnerSettlement.objects.get(pk=settlement_id)
    lines = settlement.lines.values("line_type").annotate(total=Sum("amount"))
    totals = {row["line_type"]: row["total"] for row in lines}
    settlement.gross_income = totals.get("INCOME", Decimal("0"))
    deductions = totals.get("DEDUCTION", Decimal("0")) + totals.get("RETENTION", Decimal("0"))
    adjustments = totals.get("ADJUSTMENT", Decimal("0"))
    settlement.other_deductions = deductions
    settlement.net_payable = settlement.gross_income - deductions + adjustments - settlement.repair_deductions
    settlement.save(
        update_fields=["gross_income", "other_deductions", "net_payable", "updated_at"]
    )
    return settlement
