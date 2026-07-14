import React, { useState } from 'react';
import { Plus, Search, Building2, Upload, FileText, Camera, FileSignature, Wrench, ChevronLeft } from 'lucide-react';
import { COLOR } from '../../styles/colors';
import { Card, PageHeader, Button, SearchBar, Badge, Modal, Field, Input, Select } from '../../components/ui';

const money = (n: number) => '$' + Math.round(n).toLocaleString('es-CO');

const PROPIETARIOS = [
  { id: 1, nombre: "María Elena Castaño Ruiz" },
  { id: 2, nombre: "Jorge Iván Salazar Mosquera" },
  { id: 3, nombre: "Inversiones Cañasgordas S.A.S" },
  { id: 4, nombre: "Luz Dary Ocampo Vélez" },
];

const INMUEBLES = [
  { id: 1, propietarioId: 1, tipo: "Apartamento", direccion: "Calle 5 #38-21, Apto 502", barrio: "Tequendama", estrato: 5, area: 78, canon: 1450000, pctAdmin: 10, preaviso: 2, destino: "ALQUILER", estado: "Arrendado", fianzas: ["AFFI - Canon 2%"] },
  { id: 2, propietarioId: 1, tipo: "Local", direccion: "Av. 6N #23-45", barrio: "Granada", estrato: 5, area: 45, canon: 2100000, pctAdmin: 10, preaviso: 3, destino: "ALQUILER", estado: "Arrendado", fianzas: ["Fianzas de Colombia - Integral 3%"] },
  { id: 3, propietarioId: 1, tipo: "Apartamento", direccion: "Cra 100 #14-32, Torre 3 Apto 801", barrio: "Ciudad Jardín", estrato: 6, area: 95, canon: 2300000, pctAdmin: 10, preaviso: 2, destino: "DISPONIBLE", estado: "Disponible", fianzas: [] },
  { id: 4, propietarioId: 2, tipo: "Casa", direccion: "Calle 13 #45-67", barrio: "El Ingenio", estrato: 4, area: 130, canon: 1850000, pctAdmin: 12, preaviso: 2, destino: "ALQUILER", estado: "Arrendado", fianzas: ["AFFI - Canon 2%", "AFFI - Daños 1%"] },
  { id: 5, propietarioId: 3, tipo: "Oficina", direccion: "Torre Empresarial Sur, Of. 304", barrio: "San Fernando", estrato: 6, area: 60, canon: 1980000, pctAdmin: 10, preaviso: 3, destino: "ALQUILER", estado: "Arrendado", fianzas: ["Fianzas de Colombia - Servicios 1.5%"] },
  { id: 6, propietarioId: 3, tipo: "Oficina", direccion: "Torre Empresarial Sur, Of. 305", barrio: "San Fernando", estrato: 6, area: 60, canon: 1980000, pctAdmin: 10, preaviso: 3, destino: "ALQUILER", estado: "Arrendado", fianzas: ["Fianzas de Colombia - Servicios 1.5%"] },
  { id: 7, propietarioId: 3, tipo: "Bodega", direccion: "Zona Industrial Acopi, Bodega 12", barrio: "Acopi", estrato: 3, area: 320, canon: 4200000, pctAdmin: 10, preaviso: 3, destino: "ALQUILER", estado: "Arrendado", fianzas: ["AFFI - Canon 2%"] },
  { id: 8, propietarioId: 3, tipo: "Apartamento", direccion: "Cra 70 #5-12, Apto 201", barrio: "Limonar", estrato: 5, area: 88, canon: 1750000, pctAdmin: 10, preaviso: 2, destino: "ALQUILER", estado: "En arreglo", fianzas: ["AFFI - Canon 2%"] },
  { id: 9, propietarioId: 3, tipo: "Apartamento", direccion: "Cra 70 #5-12, Apto 202", barrio: "Limonar", estrato: 5, area: 88, canon: 1750000, pctAdmin: 10, preaviso: 2, destino: "ALQUILER", estado: "Arrendado", fianzas: ["AFFI - Canon 2%"] },
  { id: 10, propietarioId: 4, tipo: "Casa", direccion: "Calle 25 #88-14", barrio: "Pance", estrato: 6, area: 210, canon: 3600000, pctAdmin: 10, preaviso: 3, destino: "VENTA", estado: "En venta", fianzas: [] },
];

export default function Inmuebles() {
  const [busqueda, setBusqueda] = useState("");
  const [filtroEstado, setFiltroEstado] = useState("Todos");
  const [seleccionado, setSeleccionado] = useState<number | null>(null);
  const [modalNuevo, setModalNuevo] = useState(false);

  const filtrados = INMUEBLES.filter(i => {
    const matchBusqueda = i.direccion.toLowerCase().includes(busqueda.toLowerCase()) || i.barrio.toLowerCase().includes(busqueda.toLowerCase());
    const matchEstado = filtroEstado === "Todos" || i.estado === filtroEstado;
    return matchBusqueda && matchEstado;
  });

  const getEstadoBadge = (estado: string) => {
    const map: Record<string, { color: string, bg: string }> = {
      "Disponible": { color: COLOR.azul, bg: COLOR.azulClaro },
      "Arrendado": { color: COLOR.verde, bg: COLOR.verdeClaro },
      "En venta": { color: COLOR.mostazaOscuro, bg: COLOR.mostazaClaro },
      "En arreglo": { color: COLOR.rojo, bg: COLOR.rojoClaro },
    };
    const s = map[estado] || map["Disponible"];
    return <Badge color={s.color} bg={s.bg}>{estado}</Badge>;
  };

  if (seleccionado !== null) {
    const inm = INMUEBLES.find(x => x.id === seleccionado)!;
    const prop = PROPIETARIOS.find(p => p.id === inm.propietarioId)!;
    return (
      <div>
        <div onClick={() => setSeleccionado(null)} style={{ display: "flex", alignItems: "center", gap: 6, color: COLOR.azul, fontSize: 13.5, fontWeight: 600, cursor: "pointer", marginBottom: 16 }}>
          <ChevronLeft size={15} /> Volver a inmuebles
        </div>
        <PageHeader
          title={inm.tipo + " · " + inm.barrio}
          subtitle={inm.direccion}
          action={getEstadoBadge(inm.estado)}
        />
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 16 }}>
          <Card>
            <h3 style={{ fontSize: 14, fontWeight: 700, margin: "0 0 14px", color: COLOR.carbon }}>Ficha del inmueble</h3>
            {[
              ["Tipo", inm.tipo], ["Barrio / Ciudad", inm.barrio + ", Cali"], ["Estrato", inm.estrato],
              ["Área", inm.area.toString() + " m²"], ["Canon mensual", money(inm.canon)], ["% Administración", inm.pctAdmin.toString() + "%"],
              ["Preaviso de entrega", inm.preaviso.toString() + " meses"], ["Propietario", prop.nombre],
            ].map(([label, val], i) => (
              <div key={i} style={{ display: "flex", justifyContent: "space-between", padding: "8px 0", borderBottom: i < 7 ? `1px solid ${COLOR.borde}` : "none" }}>
                <span style={{ fontSize: 13, color: COLOR.carbonSuave }}>{label}</span>
                <span style={{ fontSize: 13.5, fontWeight: 600, color: COLOR.carbon }}>{val}</span>
              </div>
            ))}
          </Card>

          <Card>
            <h3 style={{ fontSize: 14, fontWeight: 700, margin: "0 0 14px", color: COLOR.carbon }}>Fotos y documentos</h3>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 8, marginBottom: 14 }}>
              {[1, 2, 3].map(n => (
                <div key={n} style={{ aspectRatio: "1", background: COLOR.fondo, borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center", border: `1px dashed ${COLOR.borde}` }}>
                  <Camera size={20} color={COLOR.carbonSuave} />
                </div>
              ))}
            </div>
            <Button variant="ghost" icon={Upload} size="sm" style={{ padding: "4px 0", marginBottom: 14 }}>Cargar fotos</Button>
            <div style={{ borderTop: `1px solid ${COLOR.borde}`, paddingTop: 12 }}>
              {["Certificado de tradición.pdf", "Escritura.pdf"].map((d, i) => (
                <div key={i} style={{ display: "flex", alignItems: "center", gap: 8, padding: "6px 0", fontSize: 13, color: COLOR.azul }}>
                  <FileText size={14} /> {d}
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div>
      <PageHeader
        title="Inmuebles"
        subtitle={INMUEBLES.length + " inmuebles registrados"}
        action={<Button icon={Plus} onClick={() => setModalNuevo(true)}>Crear inmueble</Button>}
      />
      <div style={{ display: "flex", gap: 10, marginBottom: 16, alignItems: "center" }}>
        <SearchBar placeholder="Buscar por dirección o barrio..." value={busqueda} onChange={setBusqueda} />
        <div style={{ display: "flex", gap: 6 }}>
          {["Todos", "Disponible", "Arrendado", "En venta", "En arreglo"].map(e => (
            <div key={e} onClick={() => setFiltroEstado(e)} style={{
              padding: "7px 13px", borderRadius: 7, fontSize: 12.5, fontWeight: 600, cursor: "pointer",
              background: filtroEstado === e ? COLOR.azul : "white", color: filtroEstado === e ? "white" : COLOR.carbon,
              border: `1px solid ${filtroEstado === e ? COLOR.azul : COLOR.borde}`
            }}>{e}</div>
          ))}
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 14 }}>
        {filtrados.map(inm => {
          const prop = PROPIETARIOS.find(p => p.id === inm.propietarioId)!;
          return (
            <Card key={inm.id} onClick={() => setSeleccionado(inm.id)}>
              <div style={{ aspectRatio: "16/9", background: COLOR.fondo, borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center", marginBottom: 12, border: `1px solid ${COLOR.borde}` }}>
                <Building2 size={28} color={COLOR.borde} />
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 6 }}>
                <div style={{ fontSize: 14, fontWeight: 700, color: COLOR.carbon }}>{inm.tipo} · {inm.barrio}</div>
                {getEstadoBadge(inm.estado)}
              </div>
              <div style={{ fontSize: 12.5, color: COLOR.carbonSuave, marginBottom: 10 }}>{inm.direccion}</div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", borderTop: `1px solid ${COLOR.borde}`, paddingTop: 10 }}>
                <span style={{ fontSize: 15, fontWeight: 700, color: COLOR.carbon }}>{money(inm.canon)}</span>
                <span style={{ fontSize: 12, color: COLOR.carbonSuave }}>{prop.nombre.split(" ").slice(0, 2).join(" ")}</span>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
