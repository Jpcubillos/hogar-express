import React from 'react';
import { Pencil, Plus } from 'lucide-react';
import { COLOR } from '../../styles/colors';
import { Card, PageHeader, Button, Field, Input } from '../../components/ui';

export default function Configuracion() {
  return (
    <div>
      <PageHeader title="Configuración" subtitle="Parámetros generales del sistema · solo Administrador" />
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        <Card>
          <h3 style={{ fontSize: 14, fontWeight: 700, margin: "0 0 14px" }}>Parámetros financieros</h3>
          <Field label="% Recargo diario por mora"><Input defaultValue="1.76" /></Field>
          <Field label="% Administración por defecto"><Input defaultValue="10" /></Field>
          <Field label="Valor de IPC vigente (%)"><Input defaultValue="6.5" /></Field>
          <Button>Guardar parámetros</Button>
        </Card>
        <Card>
          <h3 style={{ fontSize: 14, fontWeight: 700, margin: "0 0 14px" }}>Afianzadoras</h3>
          {["AFFI", "Fianzas de Colombia"].map((a, i) => (
            <div key={i} style={{ display: "flex", justifyContent: "space-between", padding: "10px 0", borderBottom: `1px solid ${COLOR.borde}` }}>
              <span style={{ fontSize: 13.5 }}>{a}</span>
              <Button variant="ghost" size="sm" icon={Pencil}>Editar</Button>
            </div>
          ))}
          <Button variant="secondary" icon={Plus} size="sm" style={{ marginTop: 10 }}>Agregar afianzadora</Button>
        </Card>
      </div>
    </div>
  );
}
