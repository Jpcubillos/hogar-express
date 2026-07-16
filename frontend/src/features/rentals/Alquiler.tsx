import { useState } from 'react';
import {
  CalendarDays,
  ChevronRight,
  FileSignature,
  Plus,
  ReceiptText,
  ShieldAlert,
  WalletCards,
} from 'lucide-react';
import { COLOR } from '../../styles/colors';
import { Badge, Button, Card, PageHeader, SectionTitle } from '../../components/ui';

const TABS = [
  { id: 'contratos', label: 'Contratos', icon: FileSignature },
  { id: 'recibos', label: 'Recibos y pagos', icon: ReceiptText },
  { id: 'mora', label: 'Mora y afianzadora', icon: ShieldAlert },
  { id: 'liquidacion', label: 'Liquidación', icon: WalletCards },
];

const CONTRACTS = [
  { id: 'CTR-001', tenant: 'Carlos Mejía', property: 'Apartamento · Tequendama', end: '31 jul 2026', value: '$1.450.000', status: 'Vigente' },
  { id: 'CTR-002', tenant: 'Diana Rojas', property: 'Local · Granada', end: '18 dic 2026', value: '$2.100.000', status: 'Vigente' },
  { id: 'CTR-003', tenant: 'Comercializadora El Faro', property: 'Casa · El Ingenio', end: '15 ago 2026', value: '$1.850.000', status: 'Por vencer' },
];

const tabDescriptions: Record<string, { title: string; text: string; icon: typeof FileSignature }> = {
  recibos: { title: 'Control de recibos y pagos', text: 'Aquí se organizarán los cobros mensuales, pagos recibidos y comprobantes de cada contrato.', icon: ReceiptText },
  mora: { title: 'Seguimiento de mora y garantías', text: 'Visualiza obligaciones vencidas, recargos aplicados y casos trasladados a la afianzadora.', icon: ShieldAlert },
  liquidacion: { title: 'Liquidación a propietarios', text: 'Consolida el canon recaudado, descuentos y valor neto que debe girarse a cada propietario.', icon: WalletCards },
};

export default function Alquiler() {
  const [tab, setTab] = useState('contratos');

  return (
    <div>
      <PageHeader
        eyebrow="Gestión contractual"
        title="Alquiler"
        subtitle="Administra contratos, recaudos, novedades y liquidaciones desde un solo lugar."
        action={<Button icon={Plus}>Crear contrato</Button>}
      />

      <div className="tabs" role="tablist" aria-label="Secciones de alquiler">
        {TABS.map((item) => {
          const Icon = item.icon;
          return (
            <button
              type="button"
              role="tab"
              aria-selected={tab === item.id}
              key={item.id}
              className={`tab-button ${tab === item.id ? 'is-active' : ''}`}
              onClick={() => setTab(item.id)}
            >
              <Icon size={15} style={{ verticalAlign: -3, marginRight: 7 }} />
              {item.label}
            </button>
          );
        })}
      </div>

      {tab === 'contratos' ? (
        <Card className="table-shell">
          <div style={{ padding: '18px 20px 4px' }}>
            <SectionTitle
              title="Contratos activos"
              description="3 contratos requieren seguimiento durante los próximos meses"
              action={<Badge color={COLOR.verde} bg={COLOR.verdeClaro}>3 activos</Badge>}
            />
          </div>
          <div className="table-scroll">
            <table className="data-table">
              <thead><tr><th>Contrato</th><th>Arrendatario</th><th>Inmueble</th><th>Finaliza</th><th>Canon</th><th>Estado</th><th /></tr></thead>
              <tbody>
                {CONTRACTS.map((contract) => (
                  <tr key={contract.id}>
                    <td className="data-table__primary">{contract.id}</td>
                    <td>{contract.tenant}</td>
                    <td>{contract.property}</td>
                    <td><CalendarDays size={13} style={{ verticalAlign: -2, marginRight: 5 }} />{contract.end}</td>
                    <td className="data-table__primary">{contract.value}</td>
                    <td>
                      <Badge
                        color={contract.status === 'Vigente' ? COLOR.verde : COLOR.mostazaOscuro}
                        bg={contract.status === 'Vigente' ? COLOR.verdeClaro : COLOR.mostazaClaro}
                      >
                        {contract.status}
                      </Badge>
                    </td>
                    <td><button type="button" className="row-action" aria-label={`Ver ${contract.id}`}><ChevronRight size={16} /></button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      ) : (() => {
        const content = tabDescriptions[tab];
        const Icon = content.icon;
        return (
          <Card className="module-hero">
            <div className="module-hero__content">
              <div className="module-hero__icon"><Icon size={22} /></div>
              <h3>{content.title}</h3>
              <p>{content.text}</p>
              <Button variant="secondary" style={{ marginTop: 18 }}>Preparar módulo</Button>
            </div>
          </Card>
        );
      })()}
    </div>
  );
}
