import React, { useState } from 'react';
import { Plus, Search, ChevronRight, ChevronLeft, Pencil, Phone, Mail, MapPin, CreditCard, FileText, Upload } from 'lucide-react';
import { COLOR } from '../../styles/colors';
import { Card, PageHeader, Button, SearchBar, Badge, Modal, Field, Input, Select } from '../../components/ui';

const money = (n: number) => '$' + Math.round(n).toLocaleString('es-CO');

// Realist mock data
const PROPIETARIOS = [
  { id: 1, nombre: "María Elena Castaño Ruiz", identificacion: "CC 31.452.778", ciudad: "Cali", telefono: "315 442 9087", correo: "melena.castano@gmail.com", banco: "Bancolombia", cuenta: "Ahorros - **** 4521", inmuebles: [1, 2, 3], apoderado: false },
  { id: 2, nombre: "Jorge Iván Salazar Mosquera", identificacion: "CC 16.789.432", ciudad: "Cali", telefono: "300 781 2244", correo: "jisalazar@hotmail.com", banco: "Davivienda", cuenta: "Corriente - **** 8810", inmuebles: [4], apoderado: true },
  { id: 3, nombre: "Inversiones Cañasgordas S.A.S", identificacion: "NIT 900.234.561-2", ciudad: "Cali", telefono: "602 514 7733", correo: "contabilidad@canasgordas.com", banco: "BBVA", cuenta: "Corriente - **** 2290", inmuebles: [5, 6, 7, 8, 9] },
  { id: 4, nombre: "Luz Dary Ocampo Vélez", identificacion: "CC 38.221.904", ciudad: "Cali", telefono: "318 905 6612", correo: "luzdaryov@gmail.com", banco: "Bancolombia", cuenta: "Ahorros - **** 1187", inmuebles: [10] },
];

const INMUEBLES = [
  { id: 1, propietarioId: 1, tipo: "Apartamento", direccion: "Calle 5 #38-21, Apto 502", barrio: "Tequendama", canon: 1450000, estado: "Arrendado" },
  { id: 2, propietarioId: 1, tipo: "Local", direccion: "Av. 6N #23-45", barrio: "Granada", canon: 2100000, estado: "Arrendado" },
  { id: 3, propietarioId: 1, tipo: "Apartamento", direccion: "Cra 100 #14-32, Torre 3 Apto 801", barrio: "Ciudad Jardín", canon: 2300000, estado: "Disponible" },
  { id: 4, propietarioId: 2, tipo: "Casa", direccion: "Calle 13 #45-67", barrio: "El Ingenio", canon: 1850000, estado: "Arrendado" },
  { id: 5, propietarioId: 3, tipo: "Oficina", direccion: "Torre Empresarial Sur, Of. 304", barrio: "San Fernando", canon: 1980000, estado: "Arrendado" },
  { id: 6, propietarioId: 3, tipo: "Oficina", direccion: "Torre Empresarial Sur, Of. 305", barrio: "San Fernando", canon: 1980000, estado: "Arrendado" },
  { id: 7, propietarioId: 3, tipo: "Bodega", direccion: "Zona Industrial Acopi, Bodega 12", barrio: "Acopi", canon: 4200000, estado: "Arrendado" },
  { id: 8, propietarioId: 3, tipo: "Apartamento", direccion: "Cra 70 #5-12, Apto 201", barrio: "Limonar", canon: 1750000, estado: "En arreglo" },
  { id: 9, propietarioId: 3, tipo: "Apartamento", direccion: "Cra 70 #5-12, Apto 202", barrio: "Limonar", canon: 1750000, estado: "Arrendado" },
  { id: 10, propietarioId: 4, tipo: "Casa", direccion: "Calle 25 #88-14", barrio: "Pance", canon: 3600000, estado: "En venta" },
];

export default function Propietarios() {
  const [busqueda, setBusqueda] = useState("");
  const [seleccionado, setSeleccionado] = useState<number | null>(null);
  const [modalNuevo, setModalNuevo] = useState(false);

  const filtrados = PROPIETARIOS.filter(p =>
    p.nombre.toLowerCase().includes(busqueda.toLowerCase()) ||
    p.identificacion.toLowerCase().includes(busqueda.toLowerCase())
  );

  if (seleccionado !== null) {
    const p = PROPIETARIOS.find(x => x.id === seleccionado)!;
    const inmueblesProp = INMUEBLES.filter(i => p.inmuebles.includes(i.id));
    return (
      <div>
        <div onClick={() => setSeleccionado(null)} style={{ display: "flex", alignItems: "center", gap: 6, color: COLOR.azul, fontSize: 13.5, fontWeight: 600, cursor: "pointer", marginBottom: 16 }}>
          <ChevronLeft size={15} /> Volver a propietarios
        </div>
        <PageHeader
          title={p.nombre}
          subtitle={p.identificacion}
          action={<Button icon={Pencil} variant="secondary">Editar</Button>}
        />
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1.4fr", gap: 16 }}>
          <Card>
            <h3 style={{ fontSize: 14, fontWeight: 700, margin: "0 0 14px", color: COLOR.carbon }}>Datos de contacto</h3>
            {[
              { icon: Phone, label: p.telefono },
              { icon: Mail, label: p.correo },
              { icon: MapPin, label: p.ciudad },
              { icon: CreditCard, label: p.banco + " · " + p.cuenta },
            ].map((row, i) => (
              <div key={i} style={{ display: "flex", alignItems: "center", gap: 10, padding: "8px 0", borderBottom: i < 3 ? `1px solid ${COLOR.borde}` : "none" }}>
                <row.icon size={15} color={COLOR.carbonSuave} />
                <span style={{ fontSize: 13.5, color: COLOR.carbon }}>{row.label}</span>
              </div>
            ))}
            {p.apoderado && (
              <div style={{ marginTop: 12 }}><Badge color={COLOR.azul} bg={COLOR.azulClaro}>Tiene apoderado registrado</Badge></div>
            )}

            <h3 style={{ fontSize: 14, fontWeight: 700, margin: "20px 0 12px", color: COLOR.carbon }}>Documentos</h3>
            {["Cédula.pdf", "Certificado bancario.pdf"].map((d, i) => (
              <div key={i} style={{ display: "flex", alignItems: "center", gap: 8, padding: "7px 0", fontSize: 13, color: COLOR.azul }}>
                <FileText size={14} /> {d}
              </div>
            ))}
            <Button variant="ghost" icon={Upload} size="sm" style={{ marginTop: 6, padding: "6px 0" }}>Subir documento</Button>
          </Card>

          <Card>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 14 }}>
              <h3 style={{ fontSize: 14, fontWeight: 700, margin: 0, color: COLOR.carbon }}>Inmuebles asociados ({inmueblesProp.length})</h3>
            </div>
            {inmueblesProp.map(i => (
              <div key={i.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "11px 0", borderBottom: `1px solid ${COLOR.borde}` }}>
                <div>
                  <div style={{ fontSize: 13.5, fontWeight: 600, color: COLOR.carbon }}>{i.tipo} · {i.barrio}</div>
                  <div style={{ fontSize: 12.5, color: COLOR.carbonSuave }}>{i.direccion}</div>
                </div>
                <div style={{ textAlign: "right" }}>
                  <div style={{ fontSize: 13.5, fontWeight: 600, color: COLOR.carbon, marginBottom: 4 }}>{money(i.canon)}</div>
                  <Badge color={i.estado === 'Arrendado' ? COLOR.verde : COLOR.azul} bg={i.estado === 'Arrendado' ? COLOR.verdeClaro : COLOR.azulClaro}>{i.estado}</Badge>
                </div>
              </div>
            ))}

            <h3 style={{ fontSize: 14, fontWeight: 700, margin: "20px 0 12px", color: COLOR.carbon }}>Liquidaciones</h3>
            <div style={{ display: "flex", gap: 10 }}>
              <div style={{ flex: 1, background: COLOR.verdeClaro, borderRadius: 8, padding: 12 }}>
                <div style={{ fontSize: 12, color: COLOR.verde, fontWeight: 600 }}>Liquidadas (mes actual)</div>
                <div style={{ fontSize: 20, fontWeight: 700, color: COLOR.carbon }}>{inmueblesProp.length > 1 ? inmueblesProp.length - 1 : 0}</div>
              </div>
              <div style={{ flex: 1, background: COLOR.mostazaClaro, borderRadius: 8, padding: 12 }}>
                <div style={{ fontSize: 12, color: COLOR.mostazaOscuro, fontWeight: 600 }}>Pendientes</div>
                <div style={{ fontSize: 20, fontWeight: 700, color: COLOR.carbon }}>{inmueblesProp.length > 1 ? 1 : inmueblesProp.length}</div>
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
        title="Propietarios"
        subtitle={PROPIETARIOS.length + " propietarios registrados"}
        action={<Button icon={Plus} onClick={() => setModalNuevo(true)}>Crear propietario</Button>}
      />
      <div style={{ marginBottom: 16 }}>
        <SearchBar placeholder="Buscar por nombre o identificación..." value={busqueda} onChange={setBusqueda} />
      </div>
      <Card style={{ padding: 0, overflow: "hidden" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13.5 }}>
          <thead>
            <tr style={{ background: COLOR.fondo, borderBottom: `1px solid ${COLOR.borde}` }}>
              {["Nombre", "Identificación", "Ciudad", "Inmuebles", "Contacto", ""].map((h, i) => (
                <th key={i} style={{ textAlign: "left", padding: "11px 16px", fontSize: 12, color: COLOR.carbonSuave, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.3px" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtrados.map(p => (
              <tr key={p.id} onClick={() => setSeleccionado(p.id)} style={{ borderBottom: `1px solid ${COLOR.borde}`, cursor: "pointer" }}
                onMouseEnter={(e) => e.currentTarget.style.background = COLOR.fondo}
                onMouseLeave={(e) => e.currentTarget.style.background = "white"}
              >
                <td style={{ padding: "13px 16px", fontWeight: 600, color: COLOR.carbon }}>{p.nombre}</td>
                <td style={{ padding: "13px 16px", color: COLOR.carbonSuave }}>{p.identificacion}</td>
                <td style={{ padding: "13px 16px", color: COLOR.carbonSuave }}>{p.ciudad}</td>
                <td style={{ padding: "13px 16px" }}><Badge color={COLOR.azul} bg={COLOR.azulClaro}>{p.inmuebles.length} inmueble{p.inmuebles.length !== 1 ? "s" : ""}</Badge></td>
                <td style={{ padding: "13px 16px", color: COLOR.carbonSuave }}>{p.telefono}</td>
                <td style={{ padding: "13px 16px", textAlign: "right" }}><ChevronRight size={16} color={COLOR.carbonSuave} /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>

      {modalNuevo && (
        <Modal title="Crear propietario" onClose={() => setModalNuevo(false)}>
          <Field label="Tipo y número de identificación">
            <div style={{ display: "flex", gap: 8 }}>
              <Select style={{ width: 110 }}><option>CC</option><option>NIT</option><option>CE</option></Select>
              <Input placeholder="Número de documento" />
            </div>
          </Field>
          <Field label="Nombre completo o razón social"><Input placeholder="Ej: María Elena Castaño Ruiz" /></Field>
          <Field label="Dirección"><Input placeholder="Dirección de residencia" /></Field>
          <div style={{ display: "flex", gap: 10 }}>
            <Field label="Ciudad" style={{ flex: 1 }}><Input placeholder="Cali" /></Field>
            <Field label="Teléfono" style={{ flex: 1 }}><Input placeholder="300 000 0000" /></Field>
          </div>
          <Field label="Correo electrónico"><Input placeholder="correo@ejemplo.com" /></Field>
          <div style={{ display: "flex", gap: 10 }}>
            <Field label="Banco" style={{ flex: 1 }}><Input placeholder="Bancolombia" /></Field>
            <Field label="Tipo de cuenta" style={{ flex: 1 }}><Select><option>Ahorros</option><option>Corriente</option></Select></Field>
          </div>
          <Field label="Número de cuenta"><Input placeholder="N° de cuenta bancaria" /></Field>
          <div style={{ display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 18 }}>
            <Button variant="secondary" onClick={() => setModalNuevo(false)}>Cancelar</Button>
            <Button onClick={() => setModalNuevo(false)}>Guardar propietario</Button>
          </div>
        </Modal>
      )}
    </div>
  );
}
