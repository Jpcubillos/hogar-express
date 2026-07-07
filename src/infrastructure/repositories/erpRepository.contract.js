export const erpRepositoryContract = {
  owners: ['list', 'getById', 'create', 'update'],
  properties: ['list', 'getById', 'create', 'update'],
  rentCollections: ['list', 'getById', 'createRental', 'updateStatus', 'addNote'],
  payments: ['list', 'register', 'generateReceipt'],
  paymentHistory: ['list', 'filter'],
  tenantReceipts: ['list', 'generate', 'update', 'reprint'],
  ownerCollections: ['list', 'generateSettlement', 'print'],
  ownerCashReceipts: ['list', 'create', 'cancel'],
  settlements: ['list', 'generate'],
  repairs: ['list', 'create', 'updateStatus'],
  sales: ['list', 'create', 'updateStatus', 'closeSale'],
  catalogs: ['list', 'create', 'update', 'activate', 'deactivate'],
};
