import React, { useState } from 'react';
import { Plus } from 'lucide-react';
import { COLOR } from '../../styles/colors';
import { Card, PageHeader, Button } from '../../components/ui';

export default function Venta() {
  return (
    <div>
      <PageHeader title="Venta" subtitle="Fichas de venta, comisiones y estados" action={<Button icon={Plus}>Crear ficha de venta</Button>} />
      <Card>
        <p style={{ fontSize: 14, color: COLOR.carbonSuave }}>Módulo en construcción. Se encuentra configurado con enrutamiento dinámico.</p>
      </Card>
    </div>
  );
}
