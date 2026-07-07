export const paymentStatuses = {
  registered: 'registered',
  receiptGenerated: 'receipt_generated',
  reversed: 'reversed',
};

export const receiptGenerationRule = {
  requiresRegisteredPayment: true,
};

export const paymentHistoryReceiptTypes = {
  tenantReceipt: 'tenant_receipt',
  ownerSettlement: 'owner_settlement',
  ownerCashReceipt: 'owner_cash_receipt',
};

export const receiptTypes = {
  monthly: 'monthly',
  days: 'days',
};

export const receiptAdjustmentTypes = {
  discount: 'discount',
  additionalCharge: 'additional_charge',
};

export const tenantReceiptRequiredAuditFields = [
  'payment_date',
  'generated_at',
  'generated_by',
  'modification_history',
];

export const proratedReceiptRule = {
  fixedMonthDays: 30,
  afterDay15RequiresUserChoice: true,
};

export const lateInterestRule = {
  interestFreeUntilDay: 5,
  interestUntilDay: 30,
  reportAfterDay: 30,
  defaultDailyInterestPercentage: 1.76,
};
