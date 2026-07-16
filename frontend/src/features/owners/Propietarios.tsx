import { useState } from 'react';
import {
  Building2,
  ChevronLeft,
  ChevronRight,
  CreditCard,
  FileText,
  Mail,
  MapPin,
  Pencil,
  Phone,
  Plus,
  Upload,
  UserRound,
} from 'lucide-react';
import { COLOR } from '../../styles/colors';
import { Badge, Button, Card, Field, Input, Modal, PageHeader, SearchBar, SectionTitle, Select } from '../../components/ui';

const money = (value: number) => `$${Math.round(value).toLocaleString('es-CO')}`;

const PROPIETARIOS = [
  { id: 1, nombre: 'María Elena Castaño Ruiz', identificacion: 'CC 31.452.778', ciudad: 'Cali', telefono: '315 442 9087', correo: 'melena.castano@gmail.com', banco: 'Bancolombia', cuenta: 'Ahorros · **** 4521', inmuebles: [1, 2, 3], apoderado: false },
  { id: 2, nombre: 'Jorge Iván Salazar Mosquera', identificacion: 'CC 16.789.432', ciudad: 'Cali', telefono: '300 781 2244', correo: 'jisalazar@hotmail.com', banco: 'Davivienda', cuenta: 'Corriente · **** 8810', inmuebles: [4], apoderado: true },
  { id: 3, nombre: 'Inversiones Cañasgordas S.A.S.', identificacion: 'NIT 900.234.561-2', ciudad: 'Cali', telefono: '602 514 7733', correo: 'contabilidad@canasgordas.com', banco: 'BBVA', cuenta: 'Corriente · **** 2290', inmuebles: [5, 6, 7, 8, 9], apoderado: false },
  { id: 4, nombre: 'Luz Dary Ocampo Vélez', identificacion: 'CC 38.221.904', ciudad: 'Cali', telefono: '318 905 6612', correo: 'luzdaryov@gmail.com', banco: 'Bancolombia', cuenta: 'Ahorros · **** 1187', inmuebles: [10], apoderado: false },
];

const INMUEBLES = [
  { id: 1, tipo: 'Apartamento', direccion: 'Calle 5 #38-21, Apto 502', barrio: 'Tequendama', canon: 1450000, estado: 'Arrendado' },
  { id: 2, tipo: 'Local', direccion: 'Av. 6N #23-45', barrio: 'Granada', canon: 2100000, estado: 'Arrendado' },
  { id: 3, tipo: 'Apartamento', direccion: 'Cra 100 #14-32, Torre 3 Apto 801', barrio: 'Ciudad Jardín', canon: 2300000, estado: 'Disponible' },
  { id: 4, tipo: 'Casa', direccion: 'Calle 13 #45-67', barrio: 'El Ingenio', canon: 1850000, estado: 'Arrendado' },
  { id: 5, tipo: 'Oficina', direccion: 'Torre Empresarial Sur, Of. 304', barrio: 'San Fernando', canon: 1980000, estado: 'Arrendado' },
  { id: 6, tipo: 'Oficina', direccion: 'Torre Empresarial Sur, Of. 305', barrio: 'San Fernando', canon: 1980000, estado: 'Arrendado' },
  { id: 7, tipo: 'Bodega', direccion: 'Zona Industrial Acopi, Bodega 12', barrio: 'Acopi', canon: 4200000, estado: 'Arrendado' },
  { id: 8, tipo: 'Apartamento', direccion: 'Cra 70 #5-12, Apto 201', barrio: 'Limonar', canon: 1750000, estado: 'En arreglo' },
  { id: 9, tipo: 'Apartamento', direccion: 'Cra 70 #5-12, Apto 202', barrio: 'Limonar', canon: 1750000, estado: 'Arrendado' },
  { id: 10, tipo: 'Casa', direccion: 'Calle 25 #88-14', barrio: 'Pance', canon: 3600000, estado: 'En venta' },
];

function ownerInitials(name: string) {
  return name.split(' ').slice(0, 2).map((part) => part[0]).join('').toUpperCase();
}

export default function Propietarios() {
  const [search, setSearch] = useState('');
  const [selectedId, setSelectedId] = useState<number | null>(null);
  const [showCreate, setShowCreate] = useState(false);

  const filtered = PROPIETARIOS.filter((owner) =>
    `${owner.nombre} ${owner.identificacion}`.toLowerCase().includes(search.toLowerCase()),
  );

  if (selectedId !== null) {
    const owner = PROPIETARIOS.find((item) => item.id === selectedId)!;
    const properties = INMUEBLES.filter((property) => owner.inmuebles.includes(property.id));
    return (
      <div>
        <button type="button" className="back-link" onClick={() => setSelectedId(null)}>
          <ChevronLeft size={16} /> Volver a propietarios
        </button>
        <PageHeader
          eyebrow="Ficha del propietario"
          title={owner.nombre}
          subtitle={`${owner.identificacion} · ${properties.length} inmueble${properties.length === 1 ? '' : 's'} asociado${properties.length === 1 ? '' : 's'}`}
          action={<Button icon={Pencil} variant="secondary">Editar información</Button>}
        />

        <div className="details-grid">
          <Card>
            <SectionTitle title="Información de contacto" description="Datos personales y bancarios" />
            <div className="contact-row"><Phone size={16} /><span>{owner.telefono}</span></div>
            <div className="contact-row"><Mail size={16} /><span>{owner.correo}</span></div>
            <div className="contact-row"><MapPin size={16} /><span>{owner.ciudad}, Valle del Cauca</span></div>
            <div className="contact-row"><CreditCard size={16} /><span>{owner.banco} · {owner.cuenta}</span></div>
            {owner.apoderado && <div style={{ marginTop: 13 }}><Badge color={COLOR.azul} bg={COLOR.azulClaro}>Apoderado registrado</Badge></div>}

            <div style={{ marginTop: 24 }}>
              <SectionTitle title="Documentos" description="2 archivos vigentes" />
              <div className="document-row"><FileText size={15} /> Documento de identidad.pdf</div>
              <div className="document-row"><FileText size={15} /> Certificación bancaria.pdf</div>
              <Button variant="ghost" icon={Upload} size="sm" style={{ marginTop: 8 }}>Subir documento</Button>
            </div>
          </Card>

          <Card>
            <SectionTitle title="Inmuebles asociados" description="Portafolio administrado para este propietario" />
            {properties.map((property) => (
              <div className="associated-row" key={property.id}>
                <div className="associated-row__copy">
                  <strong>{property.tipo} · {property.barrio}</strong>
                  <span>{property.direccion}</span>
                </div>
                <div className="associated-row__value">
                  <strong>{money(property.canon)}</strong>
                  <Badge
                    color={property.estado === 'Arrendado' ? COLOR.verde : COLOR.azul}
                    bg={property.estado === 'Arrendado' ? COLOR.verdeClaro : COLOR.azulClaro}
                  >
                    {property.estado}
                  </Badge>
                </div>
              </div>
            ))}
            <div className="summary-panels">
              <div className="summary-panel" style={{ background: COLOR.verdeClaro }}>
                <span style={{ color: COLOR.verde }}>Liquidados este mes</span>
                <strong>{Math.max(properties.length - 1, 0)}</strong>
              </div>
              <div className="summary-panel" style={{ background: COLOR.mostazaClaro }}>
                <span style={{ color: COLOR.mostazaOscuro }}>Liquidaciones pendientes</span>
                <strong>{properties.length ? 1 : 0}</strong>
              </div>
            </div>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div>
      <PageHeader
        eyebrow="Directorio"
        title="Propietarios"
        subtitle={`${PROPIETARIOS.length} propietarios activos con información centralizada.`}
        action={<Button icon={Plus} onClick={() => setShowCreate(true)}>Crear propietario</Button>}
      />

      <div className="toolbar">
        <SearchBar placeholder="Buscar por nombre o identificación…" value={search} onChange={setSearch} />
        <Badge color={COLOR.verde} bg={COLOR.verdeClaro}>{PROPIETARIOS.length} activos</Badge>
      </div>

      <Card className="table-shell">
        <div className="table-scroll">
          <table className="data-table">
            <thead>
              <tr>
                <th>Propietario</th>
                <th>Identificación</th>
                <th>Ciudad</th>
                <th>Portafolio</th>
                <th>Contacto</th>
                <th aria-label="Acciones" />
              </tr>
            </thead>
            <tbody>
              {filtered.map((owner) => (
                <tr key={owner.id} onClick={() => setSelectedId(owner.id)} style={{ cursor: 'pointer' }}>
                  <td className="data-table__primary">
                    <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                      <span className="topbar-user" style={{ width: 34, height: 34, borderRadius: 10 }}>{ownerInitials(owner.nombre)}</span>
                      {owner.nombre}
                    </div>
                  </td>
                  <td>{owner.identificacion}</td>
                  <td>{owner.ciudad}</td>
                  <td><Badge color={COLOR.azul} bg={COLOR.azulClaro}>{owner.inmuebles.length} inmueble{owner.inmuebles.length === 1 ? '' : 's'}</Badge></td>
                  <td>{owner.telefono}</td>
                  <td><button type="button" className="row-action" aria-label={`Ver ${owner.nombre}`}><ChevronRight size={16} /></button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {filtered.length === 0 && (
          <div className="empty-state">
            <div className="empty-state__icon"><UserRound size={25} /></div>
            <h3>No encontramos propietarios</h3>
            <p>Prueba con otro nombre o número de identificación.</p>
          </div>
        )}
      </Card>

      {showCreate && (
        <Modal
          title="Crear propietario"
          subtitle="Completa los datos básicos. Podrás agregar documentos después."
          onClose={() => setShowCreate(false)}
          width={620}
        >
          <div className="form-row">
            <Field label="Tipo de identificación" style={{ flex: '.45' }}><Select><option>CC</option><option>NIT</option><option>CE</option></Select></Field>
            <Field label="Número de identificación"><Input placeholder="Ej. 31.452.778" /></Field>
          </div>
          <Field label="Nombre completo o razón social"><Input placeholder="Nombre del propietario" /></Field>
          <Field label="Dirección"><Input placeholder="Dirección principal" /></Field>
          <div className="form-row">
            <Field label="Ciudad"><Input placeholder="Cali" /></Field>
            <Field label="Teléfono"><Input placeholder="300 000 0000" /></Field>
          </div>
          <Field label="Correo electrónico"><Input type="email" placeholder="correo@ejemplo.com" /></Field>
          <div className="form-row">
            <Field label="Banco"><Input placeholder="Entidad bancaria" /></Field>
            <Field label="Tipo de cuenta"><Select><option>Ahorros</option><option>Corriente</option></Select></Field>
          </div>
          <Field label="Número de cuenta"><Input placeholder="Número de cuenta bancaria" /></Field>
          <div className="modal-actions">
            <Button variant="secondary" onClick={() => setShowCreate(false)}>Cancelar</Button>
            <Button icon={Building2} onClick={() => setShowCreate(false)}>Guardar propietario</Button>
          </div>
        </Modal>
      )}
    </div>
  );
}
