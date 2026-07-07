export const propertyStatuses = {
  available: 'available',
  leased: 'leased',
  forSale: 'for_sale',
  underRepair: 'under_repair',
  sold: 'sold',
  inactive: 'inactive',
};

export const propertyAvailabilityFlags = {
  availableForRent: 'available_for_rent',
  availableForSale: 'available_for_sale',
  underRepair: 'under_repair',
  sold: 'sold',
};

export const defaultLocation = {
  country: 'Colombia',
  department: 'Valle del Cauca',
  city: 'Cali',
};

export const propertyUtilityTypes = {
  water: 'water',
  electricity: 'electricity',
  gas: 'gas',
};

export const propertyDocumentTypes = {
  traditionCertificate: 'tradition_certificate',
  utilitiesBill: 'utilities_bill',
  waterBill: 'water_bill',
  electricityBill: 'electricity_bill',
  gasBill: 'gas_bill',
};

export const propertyWizardSteps = [
  'basic_information',
  'location',
  'utilities',
  'documents',
  'photos',
  'inventory',
  'commercial_status',
];
