import { Building2, ChevronRight, Plus, Tag, UserRoundSearch } from 'lucide-react';
import { COLOR } from '../../styles/colors';
import { Badge, Button, Card, PageHeader, SectionTitle } from '../../components/ui';

export default function Venta() {
  return (
    <div>
      <PageHeader
        eyebrow="Gestión comercial"
        title="Venta"
        subtitle="Controla publicaciones, interesados, ofertas y cierres de inmuebles en venta."
        action={<Button icon={Plus}>Crear ficha de venta</Button>}
      />
      <div className="kpi-grid kpi-grid--three">
        {[
          { label: 'Inmuebles publicados', value: 1, icon: Building2, color: COLOR.azul, soft: COLOR.azulClaro },
          { label: 'Interesados activos', value: 3, icon: UserRoundSearch, color: COLOR.mostazaOscuro, soft: COLOR.mostazaClaro },
          { label: 'Ofertas en estudio', value: 1, icon: Tag, color: COLOR.verde, soft: COLOR.verdeClaro },
        ].map((item) => {
          const Icon = item.icon;
          return (
            <Card key={item.label}>
              <div className="kpi-card__top">
                <div><div className="kpi-card__label">{item.label}</div><div className="kpi-card__value">{item.value}</div></div>
                <div className="kpi-card__icon" style={{ color: item.color, background: item.soft }}><Icon size={20} /></div>
              </div>
            </Card>
          );
        })}
      </div>
      <Card>
        <SectionTitle title="Portafolio en venta" description="Seguimiento comercial de publicaciones vigentes" />
        <div className="associated-row">
          <div className="associated-row__copy"><strong>Casa · Pance</strong><span>Calle 25 #88-14 · Luz Dary Ocampo Vélez</span></div>
          <div className="associated-row__value"><strong>$680.000.000</strong><Badge color={COLOR.mostazaOscuro} bg={COLOR.mostazaClaro}>Publicada</Badge></div>
          <button type="button" className="row-action" aria-label="Ver ficha"><ChevronRight size={16} /></button>
        </div>
      </Card>
    </div>
  );
}
