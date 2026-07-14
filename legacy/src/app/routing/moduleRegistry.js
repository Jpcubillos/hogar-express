import { dashboardModule } from '../../features/dashboard/index.js';
import { ownersModule } from '../../features/owners/index.js';
import { propertiesModule } from '../../features/properties/index.js';
import { leasingModule } from '../../features/leasing/index.js';
import { paymentsModule } from '../../features/payments/index.js';
import { settlementsModule } from '../../features/settlements/index.js';
import { salesModule } from '../../features/sales/index.js';
import { repairsModule } from '../../features/repairs/index.js';
import { reportsModule } from '../../features/reports/index.js';
import { settingsModule } from '../../features/settings/index.js';

export const moduleRegistry = [
  dashboardModule,
  ownersModule,
  propertiesModule,
  leasingModule,
  paymentsModule,
  settlementsModule,
  salesModule,
  repairsModule,
  reportsModule,
  settingsModule,
];
