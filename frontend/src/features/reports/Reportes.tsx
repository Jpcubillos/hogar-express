import React, { useState } from 'react';
import { Download } from 'lucide-react';
import { COLOR } from '../../styles/colors';
import { Card, PageHeader, Button } from '../../components/ui';

const money = (n: number) => "$" + Math.round(n).toLocaleString("es-CO");

export default function Reportes() {
  const [reporteActivo, setReporteActivo] = useState(0);

  const reportes = [
    { nombre: "Pendientes de pago", cols: ["Arrendatario", "Inmueble", "Días de atraso"], rows: [["Comercializadora El Faro", "Casa · El Ingenio", "3 días"]] },
    { nombre: "Mora / afianzadora", cols: ["Arrendatario", "Inmueble", "Días", "Valor", "Afianzadora"], rows: [["Comercializadora El Faro", "Casa · El Ingenio", "3", money(97680), "AFFI"]] },
    { nombre: "Próximos a vencer", cols: ["Arrendatario", "Inmueble", "Vencimiento"], rows: [["Comercializadora El Faro", "Casa · El Ingenio", "2026-07-15"]] },
    { nombre: "Canon al día", cols: ["Arrendatario", "Inmueble", "Fecha pago"], rows: [["Carlos Mejía", "Apto · Tequendama", "2026-06-03"], ["Diana Rojas", "Local · Granada", "2026-06-08"]] },
    { nombre: "Desocupados / pendientes reparación", cols: ["Inmueble", "Estado", "Días"], rows: [["Apto · Limonar 201", "En arreglo", "9 días"]] },
    { nombre: "Total inmuebles", cols: ["Estado", "Cantidad"], rows: [["Disponible", "2"], ["Arrendado", "6"], ["En venta", "1"], ["En arreglo", "1"]] },
  ];
  const r = reportes[reporteActivo];

  return (
    <div>
      <PageHeader title="Reportes" subtitle="Indicadores operativos exportables en PDF o Excel" />
      <div style={{ display: "flex", gap: 8, marginBottom: 18, flexWrap: "wrap" }}>
        {reportes.map((rep, i) => (
          <div key={i} onClick={() => setReporteActivo(i)} style={{
            padding: "8px 14px", borderRadius: 8, fontSize: 13, fontWeight: 600, cursor: "pointer",
            background: reporteActivo === i ? COLOR.azul : "white", color: reporteActivo === i ? "white" : COLOR.carbon,
            border: `1px solid ${reporteActivo === i ? COLOR.azul : COLOR.borde}`
          }}>{rep.nombre}</div>
        ))}
      </div>

      <Card style={{ padding: 0, overflow: "hidden" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "14px 18px", borderBottom: `1px solid ${COLOR.borde}` }}>
          <h3 style={{ fontSize: 15, fontWeight: 700, margin: 0 }}>{r.nombre}</h3>
          <div style={{ display: "flex", gap: 8 }}>
            <Button variant="secondary" icon={Download} size="sm">PDF</Button>
            <Button variant="secondary" icon={Download} size="sm">Excel</Button>
          </div>
        </div>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13.5 }}>
          <thead>
            <tr style={{ background: COLOR.fondo }}>
              {r.cols.map((colName, i) => <th key={i} style={{ textAlign: "left", padding: "10px 18px", fontSize: 12, color: COLOR.carbonSuave, fontWeight: 700, textTransform: "uppercase" }}>{colName}</th>)}
            </tr>
          </thead>
          <tbody>
            {r.rows.map((row, i) => (
              <tr key={i} style={{ borderBottom: `1px solid ${COLOR.borde}` }}>
                {row.map((cell, j) => <td key={j} style={{ padding: "12px 18px" }}>{cell}</td>)}
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  );
}
