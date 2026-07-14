import React, { useState } from 'react';
import { Plus, Wrench } from 'lucide-react';
import { COLOR } from '../../styles/colors';
import { Card, PageHeader, Button } from '../../components/ui';

export default function Arreglos() {
  return (
    <div>
      <PageHeader title="Arreglos / Reparación" subtitle="Órdenes de trabajo, costos y evidencias" action={<Button icon={Plus}>Nueva orden de trabajo</Button>} />
      <Card>
        <p style={{ fontSize: 14, color: COLOR.carbonSuave }}>Módulo en construcción. Se encuentra configurado con enrutamiento dinámico.</p>
      </Card>
    </div>
  );
}
