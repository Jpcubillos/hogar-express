import { Building2, Landmark, Pencil, Plus, Save, ShieldCheck } from 'lucide-react';
import { COLOR } from '../../styles/colors';
import { Badge, Button, Card, Field, Input, PageHeader, SectionTitle } from '../../components/ui';

export default function Configuracion() {
  return (
    <div>
      <PageHeader
        eyebrow="Administración"
        title="Configuración"
        subtitle="Parámetros generales, políticas y catálogos de Hogar Express."
        action={<Badge color={COLOR.azul} bg={COLOR.azulClaro}>Solo administradores</Badge>}
      />
      <div className="two-column-grid">
        <Card>
          <SectionTitle title="Parámetros financieros" description="Valores predeterminados para nuevos contratos" action={<Landmark size={19} color={COLOR.azul} />} />
          <Field label="Recargo diario por mora (%)"><Input defaultValue="1.76" /></Field>
          <Field label="Administración por defecto (%)"><Input defaultValue="10" /></Field>
          <Field label="IPC vigente (%)"><Input defaultValue="6.5" /></Field>
          <Button icon={Save}>Guardar parámetros</Button>
        </Card>
        <Card>
          <SectionTitle title="Afianzadoras" description="Empresas disponibles para coberturas" action={<ShieldCheck size={19} color={COLOR.verde} />} />
          {['AFFI', 'Fianzas de Colombia'].map((company) => (
            <div className="associated-row" key={company}>
              <div className="associated-row__copy"><strong>{company}</strong><span>Configuración activa</span></div>
              <Badge color={COLOR.verde} bg={COLOR.verdeClaro}>Activa</Badge>
              <Button variant="ghost" size="sm" icon={Pencil}>Editar</Button>
            </div>
          ))}
          <Button variant="secondary" icon={Plus} size="sm" style={{ marginTop: 12 }}>Agregar afianzadora</Button>
        </Card>
        <Card className="module-hero" style={{ gridColumn: '1 / -1' }}>
          <div className="module-hero__content">
            <div className="module-hero__icon"><Building2 size={22} /></div>
            <h3>Organización y sedes</h3>
            <p>Administra los datos jurídicos de Hogar Express, sus oficinas y los consecutivos utilizados en documentos.</p>
            <Button variant="secondary" style={{ marginTop: 18 }}>Ver configuración empresarial</Button>
          </div>
        </Card>
      </div>
    </div>
  );
}
