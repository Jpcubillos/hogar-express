import { CalendarDays, ChevronRight, Plus, Wrench } from 'lucide-react';
import { COLOR } from '../../styles/colors';
import { Badge, Button, Card, PageHeader, SectionTitle } from '../../components/ui';

const ORDERS = [
  { id: 'OT-018', property: 'Apartamento · Limonar 201', issue: 'Humedad en habitación principal', provider: 'Soluciones Integrales Cali', date: '12 jul 2026', status: 'En ejecución' },
  { id: 'OT-017', property: 'Local · Granada', issue: 'Revisión de instalación eléctrica', provider: 'Electroservicios JF', date: '10 jul 2026', status: 'Cotizando' },
];

export default function Arreglos() {
  return (
    <div>
      <PageHeader
        eyebrow="Mantenimiento"
        title="Arreglos y reparaciones"
        subtitle="Gestiona novedades, proveedores, evidencias, costos y garantías."
        action={<Button icon={Plus}>Nueva orden de trabajo</Button>}
      />
      <Card className="table-shell">
        <div style={{ padding: '18px 20px 4px' }}>
          <SectionTitle title="Órdenes activas" description="Trabajos que requieren seguimiento" action={<Badge color={COLOR.azul} bg={COLOR.azulClaro}>2 abiertas</Badge>} />
        </div>
        <div className="table-scroll">
          <table className="data-table">
            <thead><tr><th>Orden</th><th>Inmueble</th><th>Novedad</th><th>Proveedor</th><th>Actualización</th><th>Estado</th><th /></tr></thead>
            <tbody>
              {ORDERS.map((order) => (
                <tr key={order.id}>
                  <td className="data-table__primary"><Wrench size={14} style={{ verticalAlign: -2, marginRight: 6 }} />{order.id}</td>
                  <td>{order.property}</td>
                  <td>{order.issue}</td>
                  <td>{order.provider}</td>
                  <td><CalendarDays size={13} style={{ verticalAlign: -2, marginRight: 5 }} />{order.date}</td>
                  <td><Badge color={order.status === 'En ejecución' ? COLOR.azul : COLOR.mostazaOscuro} bg={order.status === 'En ejecución' ? COLOR.azulClaro : COLOR.mostazaClaro}>{order.status}</Badge></td>
                  <td><button type="button" className="row-action" aria-label={`Ver ${order.id}`}><ChevronRight size={16} /></button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}
