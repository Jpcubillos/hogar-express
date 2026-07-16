import type { CSSProperties } from 'react';
import {
  AlertTriangle,
  ArrowUpRight,
  BarChart3,
  Building2,
  CalendarDays,
  ChevronRight,
  FileSignature,
  House,
  Tag,
  Users,
  Wrench,
} from 'lucide-react';
import { COLOR } from '../../styles/colors';
import { Badge, Card, PageHeader, SectionTitle } from '../../components/ui';

interface DashboardProps {
  onNavigate: (page: string) => void;
}

const kpis = [
  { label: 'Total inmuebles', value: 10, note: '4 propietarios activos', icon: Building2, color: COLOR.azul, soft: COLOR.azulClaro },
  { label: 'En arriendo', value: 7, note: '70% de ocupación', icon: House, color: COLOR.verde, soft: COLOR.verdeClaro },
  { label: 'En venta', value: 1, note: '1 ficha publicada', icon: Tag, color: COLOR.mostazaOscuro, soft: COLOR.mostazaClaro },
  { label: 'Pendientes por arrendar', value: 2, note: '1 requiere arreglo', icon: AlertTriangle, color: COLOR.rojo, soft: COLOR.rojoClaro },
];

const alerts = [
  { title: 'Contrato próximo a vencer', description: 'Local · Av. 6N #23-45 vence en 21 días.', time: 'Hoy', icon: CalendarDays, color: COLOR.rojo, soft: COLOR.rojoClaro },
  { title: 'Pago con recargo activo', description: 'Comercializadora El Faro · contrato #003.', time: 'Hace 2 h', icon: AlertTriangle, color: COLOR.mostazaOscuro, soft: COLOR.mostazaClaro },
  { title: 'Inmueble listo para revisión', description: 'Apartamento · Limonar 201 finalizó arreglo.', time: 'Ayer', icon: Wrench, color: COLOR.azul, soft: COLOR.azulClaro },
];

export default function Dashboard({ onNavigate }: DashboardProps) {
  const date = new Intl.DateTimeFormat('es-CO', { day: 'numeric', month: 'long', year: 'numeric' }).format(new Date());

  return (
    <div>
      <PageHeader
        eyebrow="Visión general"
        title="Dashboard"
        subtitle="Consulta el estado de la operación y atiende primero lo que necesita acción."
      />

      <Card className="dashboard-welcome">
        <div className="dashboard-welcome__copy">
          <span>Resumen operativo</span>
          <h2>Todo marcha bien. Hay 3 novedades por revisar.</h2>
          <p>La ocupación se mantiene estable y tienes dos inmuebles disponibles.</p>
        </div>
        <div className="dashboard-welcome__date">Actualizado · {date}</div>
      </Card>

      <section className="kpi-grid" aria-label="Indicadores principales">
        {kpis.map((kpi) => {
          const Icon = kpi.icon;
          return (
            <Card
              key={kpi.label}
              className="kpi-card"
              style={{ '--kpi-color': kpi.color, '--kpi-soft': kpi.soft } as CSSProperties}
            >
              <div className="kpi-card__top">
                <div>
                  <div className="kpi-card__label">{kpi.label}</div>
                  <div className="kpi-card__value">{kpi.value}</div>
                </div>
                <div className="kpi-card__icon"><Icon size={20} /></div>
              </div>
              <div className="kpi-card__trend">{kpi.note}</div>
            </Card>
          );
        })}
      </section>

      <section className="dashboard-grid">
        <Card>
          <SectionTitle
            title="Novedades que requieren atención"
            description="Ordenadas por prioridad y fecha"
            action={<Badge color={COLOR.rojo} bg={COLOR.rojoClaro}>3 activas</Badge>}
          />
          {alerts.map((alert) => {
            const Icon = alert.icon;
            return (
              <div className="alert-item" key={alert.title}>
                <div className="alert-item__icon" style={{ color: alert.color, background: alert.soft }}><Icon size={17} /></div>
                <div className="alert-item__copy">
                  <strong>{alert.title}</strong>
                  <span>{alert.description}</span>
                </div>
                <span className="alert-item__time">{alert.time}</span>
              </div>
            );
          })}
        </Card>

        <Card>
          <SectionTitle title="Acciones rápidas" description="Atajos para tareas frecuentes" />
          {[
            { label: 'Crear propietario', icon: Users, target: 'propietarios' },
            { label: 'Registrar inmueble', icon: Building2, target: 'inmuebles' },
            { label: 'Nuevo contrato', icon: FileSignature, target: 'alquiler' },
            { label: 'Consultar reportes', icon: BarChart3, target: 'reportes' },
          ].map((action) => {
            const Icon = action.icon;
            return (
              <button type="button" className="quick-action" key={action.label} onClick={() => onNavigate(action.target)}>
                <span className="quick-action__icon"><Icon size={17} /></span>
                <span>{action.label}</span>
                <ChevronRight size={15} />
              </button>
            );
          })}
          <button type="button" className="ui-button ui-button--ghost ui-button--sm" onClick={() => onNavigate('reportes')} style={{ marginTop: 10 }}>
            Ver toda la operación <ArrowUpRight size={14} />
          </button>
        </Card>
      </section>
    </div>
  );
}
