export const saleStatuses = {
  available: 'available',
  inNegotiation: 'in_negotiation',
  sold: 'sold',
  inactive: 'inactive',
};

export const saleResponsibleTypes = {
  internalAdvisor: 'internal_advisor',
  agency: 'agency',
  externalAdvisor: 'external_advisor',
};

export const saleRequiredDocumentTypes = {
  mandateContract: 'mandate_contract',
  traditionCertificate: 'tradition_certificate',
  megaobras: 'megaobras',
  paidUtilitiesBills: 'paid_utilities_bills',
};

export const saleStatusTransitions = {
  [saleStatuses.available]: [
    saleStatuses.inNegotiation,
    saleStatuses.inactive,
  ],
  [saleStatuses.inNegotiation]: [
    saleStatuses.sold,
    saleStatuses.inactive,
  ],
  [saleStatuses.sold]: [],
  [saleStatuses.inactive]: [],
};

export const salePriceFields = [
  'min_sale_price',
  'max_sale_price',
  'suggested_sale_price',
  'final_sale_price',
];

export function calculateCommission(price, commissionPercentage) {
  return Math.round((price * commissionPercentage) / 100);
}

export function calculateExpectedCommissionRange({
  minSalePrice,
  maxSalePrice,
  commissionPercentage,
}) {
  return {
    expectedCommissionMin: calculateCommission(minSalePrice, commissionPercentage),
    expectedCommissionMax: calculateCommission(maxSalePrice, commissionPercentage),
  };
}
