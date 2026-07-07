export const settlementStatuses = {
  pending: 'pending',
  generated: 'generated',
  paid: 'paid',
  cancelled: 'cancelled',
};

export const ownerCollectionFilters = {
  pendingPayment: 'pending_payment',
  pendingSettlement: 'pending_settlement',
  settled: 'settled',
  overdue: 'overdue',
};

export const ownerSettlementInputs = [
  'paid_canon',
  'administration_discount',
  'guarantee_discount',
  'repairs_discount',
  'fixed_discounts',
  'owner_relevant_adjustments',
];
