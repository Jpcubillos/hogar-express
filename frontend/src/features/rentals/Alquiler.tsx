import React, { useState } from 'react';
import { Plus } from 'lucide-react';
import { COLOR } from '../../styles/colors';
import { Card, PageHeader, Button, Badge } from '../../components/ui';

const money = (n: number) => '$' + Math.round(n).toLocaleString('es-CO');

export default function Alquiler() {
  const [tab, setTab] = useState("contratos");

  const tabs = [
    { id: "contratos", label: "Contratos" },
    { id: "recibos", label: "Recibos y pagos" },
    { id: "mora", label: "Mora y afianzadora" },
    { id: "liquidacion", label: "Liquidación" },
  ];

  return (
    <div>
      <PageHeader
        title="Alquiler"
        subtitle="Contratos, recibos, control de mora y liquidación a propietarios"
      />

      <div style={{ display: "flex", gap: 4, borderBottom: `1px solid ${COLOR.borde}`, marginBottom: 20 }}>
        {tabs.map(t => (
          <div key={t.id} onClick={() => setTab(t.id)} style={{
            padding: "10px 16px", fontSize: 13.5, fontWeight: 600, cursor: "pointer",
            color: tab === t.id ? COLOR.azul : COLOR.carbonSuave,
            borderBottom: tab === t.id ? `2px solid ${COLOR.azul}` : "2px solid transparent"
          }}>{t.label}</div>
        ))}
      </div>

      <Card>
        <h3 style={{ fontSize: 16, fontWeight: 700, color: COLOR.carbon, marginBottom: 12 }}>{tab.toUpperCase()}</h3>
        <p style={{ fontSize: 14, color: COLOR.carbonSuave }}>Módulo en construcción. Se encuentra configurado con enrutamiento dinámico.</p>
      </Card>
    </div>
  );
}
