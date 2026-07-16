import { useState } from 'react';
import { Download, FileSpreadsheet, FileText } from 'lucide-react';
import { Button, Card, PageHeader, SectionTitle } from '../../components/ui';

const money = (value: number) => `$${Math.round(value).toLocaleString('es-CO')}`;

const REPORTS = [
  { name: 'Pendientes de pago', cols: ['Arrendatario', 'Inmueble', 'Días de atraso'], rows: [['Comercializadora El Faro', 'Casa · El Ingenio', '3 días']] },
  { name: 'Mora / afianzadora', cols: ['Arrendatario', 'Inmueble', 'Días', 'Valor', 'Afianzadora'], rows: [['Comercializadora El Faro', 'Casa · El Ingenio', '3', money(97680), 'AFFI']] },
  { name: 'Próximos a vencer', cols: ['Arrendatario', 'Inmueble', 'Vencimiento'], rows: [['Comercializadora El Faro', 'Casa · El Ingenio', '15 ago 2026']] },
  { name: 'Canon al día', cols: ['Arrendatario', 'Inmueble', 'Fecha de pago'], rows: [['Carlos Mejía', 'Apto · Tequendama', '3 jul 2026'], ['Diana Rojas', 'Local · Granada', '8 jul 2026']] },
  { name: 'Disponibles y reparaciones', cols: ['Inmueble', 'Estado', 'Días'], rows: [['Apto · Limonar 201', 'En arreglo', '9 días']] },
  { name: 'Total inmuebles', cols: ['Estado', 'Cantidad'], rows: [['Disponible', '1'], ['Arrendado', '7'], ['En venta', '1'], ['En arreglo', '1']] },
];

export default function Reportes() {
  const [active, setActive] = useState(0);
  const report = REPORTS[active];

  return (
    <div>
      <PageHeader eyebrow="Analítica" title="Reportes" subtitle="Indicadores operativos listos para consultar y exportar." />
      <div className="toolbar">
        <div className="filter-pills">
          {REPORTS.map((item, index) => (
            <button type="button" key={item.name} className={`filter-pill ${active === index ? 'is-active' : ''}`} onClick={() => setActive(index)}>{item.name}</button>
          ))}
        </div>
      </div>
      <Card className="table-shell">
        <div style={{ padding: '18px 20px 4px' }}>
          <SectionTitle
            title={report.name}
            description={`${report.rows.length} registro${report.rows.length === 1 ? '' : 's'} en el periodo actual`}
            action={<div style={{ display: 'flex', gap: 8 }}><Button variant="secondary" icon={FileText} size="sm">PDF</Button><Button variant="secondary" icon={FileSpreadsheet} size="sm">Excel</Button></div>}
          />
        </div>
        <div className="table-scroll">
          <table className="data-table">
            <thead><tr>{report.cols.map((column) => <th key={column}>{column}</th>)}</tr></thead>
            <tbody>{report.rows.map((row) => <tr key={row.join('-')}>{row.map((cell, index) => <td key={`${cell}-${index}`} className={index === 0 ? 'data-table__primary' : ''}>{cell}</td>)}</tr>)}</tbody>
          </table>
        </div>
        <div style={{ padding: '13px 18px', display: 'flex', justifyContent: 'flex-end', borderTop: '1px solid #e8eef1' }}>
          <Button variant="ghost" icon={Download} size="sm">Descargar reporte</Button>
        </div>
      </Card>
    </div>
  );
}
