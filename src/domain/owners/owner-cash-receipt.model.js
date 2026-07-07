export const ownerCashReceiptStatuses = {
  active: 'active',
  cancelled: 'cancelled',
};

export const ownerCashReceiptAssociations = [
  'owner_id',
  'property_id',
  'related_receipt_id',
  'related_settlement_id',
];

export const ownerCashReceiptRequiredFields = [
  'owner_id',
  'amount',
  'concept',
  'payment_method',
  'received_date',
  'generated_by',
];
