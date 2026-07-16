import { useState } from 'react';
import {
  Building2,
  Camera,
  ChevronLeft,
  FileText,
  MapPin,
  Plus,
  Upload,
} from 'lucide-react';
import { COLOR } from '../../styles/colors';
import { Badge, Button, Card, Field, Input, Modal, PageHeader, SearchBar, SectionTitle, Select } from '../../components/ui';

const money = (value: number) => `$${Math.round(value).toLocaleString('es-CO')}`;

const PROPIETARIOS = [
  { id: 1, nombre: 'María Elena Castaño Ruiz' },
  { id: 2, nombre: 'Jorge Iván Salazar Mosquera' },
  { id: 3, nombre: 'Inversiones Cañasgordas S.A.S.' },
  { id: 4, nombre: 'Luz Dary Ocampo Vélez' },
];

const INMUEBLES = [
  { id: 1, propietarioId: 1, tipo: 'Apartamento', direccion: 'Calle 5 #38-21, Apto 502', barrio: 'Tequendama', estrato: 5, area: 78, canon: 1450000, pctAdmin: 10, preaviso: 2, estado: 'Arrendado' },
  { id: 2, propietarioId: 1, tipo: 'Local', direccion: 'Av. 6N #23-45', barrio: 'Granada', estrato: 5, area: 45, canon: 2100000, pctAdmin: 10, preaviso: 3, estado: 'Arrendado' },
  { id: 3, propietarioId: 1, tipo: 'Apartamento', direccion: 'Cra 100 #14-32, Torre 3 Apto 801', barrio: 'Ciudad Jardín', estrato: 6, area: 95, canon: 2300000, pctAdmin: 10, preaviso: 2, estado: 'Disponible' },
  { id: 4, propietarioId: 2, tipo: 'Casa', direccion: 'Calle 13 #45-67', barrio: 'El Ingenio', estrato: 4, area: 130, canon: 1850000, pctAdmin: 12, preaviso: 2, estado: 'Arrendado' },
  { id: 5, propietarioId: 3, tipo: 'Oficina', direccion: 'Torre Empresarial Sur, Of. 304', barrio: 'San Fernando', estrato: 6, area: 60, canon: 1980000, pctAdmin: 10, preaviso: 3, estado: 'Arrendado' },
  { id: 6, propietarioId: 3, tipo: 'Oficina', direccion: 'Torre Empresarial Sur, Of. 305', barrio: 'San Fernando', estrato: 6, area: 60, canon: 1980000, pctAdmin: 10, preaviso: 3, estado: 'Arrendado' },
  { id: 7, propietarioId: 3, tipo: 'Bodega', direccion: 'Zona Industrial Acopi, Bodega 12', barrio: 'Acopi', estrato: 3, area: 320, canon: 4200000, pctAdmin: 10, preaviso: 3, estado: 'Arrendado' },
  { id: 8, propietarioId: 3, tipo: 'Apartamento', direccion: 'Cra 70 #5-12, Apto 201', barrio: 'Limonar', estrato: 5, area: 88, canon: 1750000, pctAdmin: 10, preaviso: 2, estado: 'En arreglo' },
  { id: 9, propietarioId: 3, tipo: 'Apartamento', direccion: 'Cra 70 #5-12, Apto 202', barrio: 'Limonar', estrato: 5, area: 88, canon: 1750000, pctAdmin: 10, preaviso: 2, estado: 'Arrendado' },
  { id: 10, propietarioId: 4, tipo: 'Casa', direccion: 'Calle 25 #88-14', barrio: 'Pance', estrato: 6, area: 210, canon: 3600000, pctAdmin: 10, preaviso: 3, estado: 'En venta' },
];

const statusStyle: Record<string, { color: string; bg: string }> = {
  Disponible: { color: COLOR.azul, bg: COLOR.azulClaro },
  Arrendado: { color: COLOR.verde, bg: COLOR.verdeClaro },
  'En venta': { color: COLOR.mostazaOscuro, bg: COLOR.mostazaClaro },
  'En arreglo': { color: COLOR.rojo, bg: COLOR.rojoClaro },
};

function StatusBadge({ status }: { status: string }) {
  const style = statusStyle[status] || statusStyle.Disponible;
  return <Badge color={style.color} bg={style.bg}>{status}</Badge>;
}

export default function Inmuebles() {
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('Todos');
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [showCreate, setShowCreate] = useState(false);

  const filtered = INMUEBLES.filter((property) => {
    const matchesText = `${property.direccion} ${property.barrio} ${property.tipo}`.toLowerCase().includes(search.toLowerCase());
    return matchesText && (status === 'Todos' || property.estado === status);
  });

  if (selectedId !== null) {
    const property = INMUEBLES.find((item) => item.id === selectedId)!;
    const owner = PROPIETARIOS.find((item) => item.id === property.propietarioId)!;
    return (
      <div>
        <button type="button" className="back-link" onClick={() => setSelectedId(null)}>
          <ChevronLeft size={16} /> Volver a inmuebles
        </button>
        <PageHeader
          eyebrow="Ficha del inmueble"
          title={`${property.tipo} · ${property.barrio}`}
          subtitle={property.direccion}
          action={<StatusBadge status={property.estado} />}
        />

        <div className="two-column-grid">
          <Card>
            <SectionTitle title="Información principal" description="Características y condiciones comerciales" />
            <div className="detail-list">
              {[
                ['Tipo de inmueble', property.tipo],
                ['Ubicación', `${property.barrio}, Cali`],
                ['Estrato', property.estrato],
                ['Área privada', `${property.area} m²`],
                ['Canon mensual', money(property.canon)],
                ['Administración', `${property.pctAdmin}%`],
                ['Preaviso de entrega', `${property.preaviso} meses`],
                ['Propietario', owner.nombre],
              ].map(([label, value]) => (
                <div className="detail-row" key={label}><span>{label}</span><strong>{value}</strong></div>
              ))}
            </div>
          </Card>

          <Card>
            <SectionTitle title="Fotos y documentos" description="Evidencia visual y soporte legal" />
            <div className="photo-grid">
              {[1, 2, 3].map((item) => <div className="photo-placeholder" key={item}><Camera size={20} /></div>)}
            </div>
            <Button variant="ghost" icon={Upload} size="sm">Cargar fotografías</Button>
            <div style={{ marginTop: 18, paddingTop: 12, borderTop: `1px solid ${COLOR.borde}` }}>
              <div className="document-row"><FileText size={15} /> Certificado de tradición.pdf</div>
              <div className="document-row"><FileText size={15} /> Escritura pública.pdf</div>
            </div>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div>
      <PageHeader
        eyebrow="Portafolio"
        title="Inmuebles"
        subtitle={`${INMUEBLES.length} inmuebles registrados entre arriendo, venta y disponibilidad.`}
        action={<Button icon={Plus} onClick={() => setShowCreate(true)}>Crear inmueble</Button>}
      />

      <div className="toolbar">
        <SearchBar placeholder="Buscar por dirección, barrio o tipo…" value={search} onChange={setSearch} />
        <div className="filter-pills">
          {['Todos', 'Disponible', 'Arrendado', 'En venta', 'En arreglo'].map((item) => (
            <button
              type="button"
              key={item}
              className={`filter-pill ${status === item ? 'is-active' : ''}`}
              onClick={() => setStatus(item)}
            >
              {item}
            </button>
          ))}
        </div>
      </div>

      {filtered.length > 0 ? (
        <div className="module-grid">
          {filtered.map((property) => {
            const owner = PROPIETARIOS.find((item) => item.id === property.propietarioId)!;
            return (
              <Card key={property.id} className="property-card" onClick={() => setSelectedId(property.id)}>
                <div className="property-card__visual">
                  <Building2 size={35} strokeWidth={1.65} />
                </div>
                <div className="property-card__content">
                  <div className="property-card__heading">
                    <h3>{property.tipo} · {property.barrio}</h3>
                    <StatusBadge status={property.estado} />
                  </div>
                  <div className="property-card__address"><MapPin size={12} style={{ verticalAlign: -2, marginRight: 4 }} />{property.direccion}</div>
                  <div className="property-card__footer">
                    <span className="property-card__price">{money(property.canon)}</span>
                    <span className="property-card__owner">{owner.nombre.split(' ').slice(0, 2).join(' ')}</span>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      ) : (
        <Card className="empty-state">
          <div className="empty-state__icon"><Building2 size={26} /></div>
          <h3>No hay inmuebles para mostrar</h3>
          <p>Ajusta los filtros o registra un nuevo inmueble en el portafolio.</p>
          <Button icon={Plus} onClick={() => setShowCreate(true)}>Crear inmueble</Button>
        </Card>
      )}

      {showCreate && (
        <Modal
          title="Crear inmueble"
          subtitle="Registra la ubicación, características y responsable del inmueble."
          onClose={() => setShowCreate(false)}
          width={660}
        >
          <div className="form-row">
            <Field label="Tipo de inmueble"><Select><option>Apartamento</option><option>Casa</option><option>Local</option><option>Oficina</option><option>Bodega</option></Select></Field>
            <Field label="Propietario"><Select>{PROPIETARIOS.map((owner) => <option key={owner.id}>{owner.nombre}</option>)}</Select></Field>
          </div>
          <Field label="Dirección completa"><Input placeholder="Calle, carrera, número y complemento" /></Field>
          <div className="form-row">
            <Field label="Barrio"><Input placeholder="Barrio" /></Field>
            <Field label="Ciudad"><Input defaultValue="Cali" /></Field>
          </div>
          <div className="form-row">
            <Field label="Estrato"><Select><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option><option>6</option></Select></Field>
            <Field label="Área (m²)"><Input type="number" placeholder="0" /></Field>
            <Field label="Canon mensual"><Input type="number" placeholder="$ 0" /></Field>
          </div>
          <div className="form-row">
            <Field label="Estado inicial"><Select><option>Disponible</option><option>En venta</option><option>En arreglo</option></Select></Field>
            <Field label="Administración (%)"><Input type="number" defaultValue="10" /></Field>
          </div>
          <div className="modal-actions">
            <Button variant="secondary" onClick={() => setShowCreate(false)}>Cancelar</Button>
            <Button icon={Building2} onClick={() => setShowCreate(false)}>Guardar inmueble</Button>
          </div>
        </Modal>
      )}
    </div>
  );
}
