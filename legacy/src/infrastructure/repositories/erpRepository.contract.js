export const erpRepositoryContract = {
  owners: ['list', 'getById', 'create', 'update'],
  properties: ['list', 'getById', 'create', 'update'],
  contracts: ['list', 'getById', 'create', 'updateStatus'],
  payments: ['list', 'register', 'generateReceipt'],
  settlements: ['list', 'generate'],
  repairs: ['list', 'create', 'updateStatus'],
  sales: ['list', 'create', 'updateStatus'],
};
