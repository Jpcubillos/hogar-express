import { useState, useMemo } from "react";
import {
  Home, Users, Building2, FileSignature, Tag, Wrench, BarChart3, Settings,
  Search, Plus, ChevronRight, ChevronDown, X, Check, AlertTriangle,
  Calendar, Phone, Mail, MapPin, FileText, Download, Upload, Camera,
  CreditCard, Clock,
  Pencil, ChevronLeft, Bell, UserCircle
} from "lucide-react";

/* ============================================================
   PALETA DE MARCA — Hogar Expres
   ============================================================ */
const COLOR = {
  mostaza: "#E0A52C",
  mostazaOscuro: "#B8821E",
  mostazaClaro: "#FBF1DD",
  azul: "#2C5F8A",
  azulOscuro: "#1F4565",
  azulClaro: "#E8F0F7",
  carbon: "#363432",
  carbonSuave: "#6B6764",
  verde: "#5B7F3C",
  verdeClaro: "#EBF1E3",
  rojo: "#B6422E",
  rojoClaro: "#F8E8E4",
  fondo: "#FBF9F5",
  borde: "#E5E0D6",
};

/* ============================================================
   LOGO — recreado en SVG a partir del logo original del cliente
   ============================================================ */
function LogoMark({ size = 36 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 100 100" fill="none">
      <path d="M50 8 L80 34 L80 78 L20 78 L20 34 Z" fill={COLOR.mostaza} stroke={COLOR.carbon} strokeWidth="3" strokeLinejoin="round"/>
      <rect x="40" y="42" width="20" height="20" rx="2" fill={COLOR.azul} stroke={COLOR.carbon} strokeWidth="2.5"/>
      <line x1="50" y1="42" x2="50" y2="62" stroke="white" strokeWidth="2"/>
      <line x1="40" y1="52" x2="60" y2="52" stroke="white" strokeWidth="2"/>
      <path d="M20 78 L78 24" stroke={COLOR.azul} strokeWidth="5" strokeLinecap="round"/>
    </svg>
  );
}

function LogoFull() {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
      <LogoMark size={34} />
      <div style={{ lineHeight: 1.05 }}>
        <div style={{ fontFamily: "Georgia, serif", fontSize: 19, fontWeight: 700, color: COLOR.carbon, letterSpacing: "-0.3px" }}>
          Hogar<span style={{ color: COLOR.mostaza }}>E</span>xpres
        </div>
        <div style={{ fontSize: 10, color: COLOR.carbonSuave, letterSpacing: "0.5px", textTransform: "uppercase" }}>
          Hecho a tu medida
        </div>
      </div>
    </div>
  );
}

/* ============================================================
   DATOS SIMULADOS (mock data realista para la demo)
   ============================================================ */
const PROPIETARIOS = [
  { id: 1, nombre: "María Elena Castaño Ruiz", identificacion: "CC 31.452.778", ciudad: "Cali", telefono: "315 442 9087", correo: "melena.castano@gmail.com", banco: "Bancolombia", cuenta: "Ahorros - **** 4521", inmuebles: [1, 2, 3], apoderado: false },
  { id: 2, nombre: "Jorge Iván Salazar Mosquera", identificacion: "CC 16.789.432", ciudad: "Cali", telefono: "300 781 2244", correo: "jisalazar@hotmail.com", banco: "Davivienda", cuenta: "Corriente - **** 8810", inmuebles: [4], apoderado: true },
  { id: 3, nombre: "Inversiones Cañasgordas S.A.S", identificacion: "NIT 900.234.561-2", ciudad: "Cali", telefono: "602 514 7733", correo: "contabilidad@canasgordas.com", banco: "BBVA", cuenta: "Corriente - **** 2290", inmuebles: [5, 6, 7, 8, 9] },
  { id: 4, nombre: "Luz Dary Ocampo Vélez", identificacion: "CC 38.221.904", ciudad: "Cali", telefono: "318 905 6612", correo: "luzdaryov@gmail.com", banco: "Bancolombia", cuenta: "Ahorros - **** 1187", inmuebles: [10] },
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

const ARRENDATARIOS = [
  { id: 1, nombre: "Carlos Andrés Mejía Londoño", identificacion: "CC 1.114.567.890", telefono: "311 245 7890", correo: "camejia@gmail.com", inmuebleId: 1 },
  { id: 2, nombre: "Diana Patricia Rojas Tamayo", identificacion: "CC 1.045.223.117", telefono: "320 556 8821", correo: "dprojas@outlook.com", inmuebleId: 2 },
  { id: 3, nombre: "Comercializadora El Faro Ltda", identificacion: "NIT 901.112.334-5", telefono: "602 333 1190", correo: "gerencia@elfaro.co", inmuebleId: 4 },
  { id: 4, nombre: "Andrés Felipe Gómez Cardona", identificacion: "CC 94.412.330", telefono: "314 778 2200", correo: "afgomezc@gmail.com", inmuebleId: 5 },
];

const CONTRATOS = [
  { id: 1, inmuebleId: 1, arrendatarioId: 1, fechaInicio: "2025-08-01", duracion: 12, fechaFin: "2026-07-31", canon: 1450000, canonVigente: 1450000, estado: "Activo", diaPago: 3 },
  { id: 2, inmuebleId: 2, arrendatarioId: 2, fechaInicio: "2025-03-15", duracion: 12, fechaFin: "2026-03-14", canon: 2100000, canonVigente: 2100000, estado: "Activo", diaPago: 8 },
  { id: 3, inmuebleId: 4, arrendatarioId: 3, fechaInicio: "2024-01-01", duracion: 24, fechaFin: "2026-07-15", canon: 1850000, canonVigente: 1850000, estado: "Activo", diaPago: 11 },
  { id: 4, inmuebleId: 5, arrendatarioId: 4, fechaInicio: "2025-11-01", duracion: 12, fechaFin: "2026-10-31", canon: 1980000, canonVigente: 1980000, estado: "Activo", diaPago: 1 },
];

const VENTAS = [
  { id: 1, inmuebleId: 10, precio: 480000000, comision: 3, responsable: "Asesor Interno - Paola Jiménez", estado: "En negociación" },
];

const ARREGLOS = [
  { id: 1, inmuebleId: 8, descripcion: "Cambio de tubería baño principal + pintura general", fecha: "2026-06-15", responsable: "Técnico - Wilson Cardona", estado: "En progreso", costoTotal: 980000, cargoA: "Propietario" },
  { id: 2, inmuebleId: 3, descripcion: "Mantenimiento preventivo antes de nueva entrega", fecha: "2026-06-10", responsable: "Técnico - Wilson Cardona", estado: "Terminado", costoTotal: 320000, cargoA: "Propietario" },
];

const money = (n) => "$" + Math.round(n).toLocaleString("es-CO");

function diaDelMes() { return 8; } // simulado para demo: hoy = día 8

function estadoMora() {
  const hoy = diaDelMes();
  if (hoy <= 5) return { estado: "ok", label: "Sin recargo", color: COLOR.verde, bg: COLOR.verdeClaro };
  if (hoy <= 10) return { estado: "recargo", label: `Recargo día ${hoy}`, color: COLOR.mostazaOscuro, bg: COLOR.mostazaClaro };
  return { estado: "mora", label: "En afianzadora", color: COLOR.rojo, bg: COLOR.rojoClaro };
}

/* ============================================================
   COMPONENTES BASE REUTILIZABLES
   ============================================================ */
function Badge({ children, color, bg, style }) {
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: 4, fontSize: 12, fontWeight: 600,
      color, background: bg, padding: "3px 10px", borderRadius: 20, whiteSpace: "nowrap", ...style
    }}>
      {children}
    </span>
  );
}

function EstadoInmuebleBadge({ estado }) {
  const map = {
    "Disponible": { color: COLOR.azul, bg: COLOR.azulClaro },
    "Arrendado": { color: COLOR.verde, bg: COLOR.verdeClaro },
    "En venta": { color: COLOR.mostazaOscuro, bg: COLOR.mostazaClaro },
    "En arreglo": { color: COLOR.rojo, bg: COLOR.rojoClaro },
  };
  const s = map[estado] || map["Disponible"];
  return <Badge color={s.color} bg={s.bg}>{estado}</Badge>;
}

function Card({ children, style, ...rest }) {
  return (
    <div
      style={{
        background: "white", border: `1px solid ${COLOR.borde}`, borderRadius: 10,
        padding: 20, ...style
      }}
      {...rest}
    >
      {children}
    </div>
  );
}

function Button({ children, variant = "primary", icon: Icon, onClick, style, size = "md" }) {
  const variants = {
    primary: { background: COLOR.azul, color: "white", border: "none" },
    secondary: { background: "white", color: COLOR.carbon, border: `1px solid ${COLOR.borde}` },
    accent: { background: COLOR.mostaza, color: COLOR.carbon, border: "none" },
    ghost: { background: "transparent", color: COLOR.azul, border: "none" },
    danger: { background: COLOR.rojoClaro, color: COLOR.rojo, border: "none" },
  };
  const sizes = { sm: "6px 12px", md: "9px 16px" };
  return (
    <button
      onClick={onClick}
      style={{
        display: "inline-flex", alignItems: "center", gap: 6, fontSize: 13.5, fontWeight: 600,
        padding: sizes[size], borderRadius: 8, cursor: "pointer", fontFamily: "inherit",
        transition: "opacity 0.15s", ...variants[variant], ...style
      }}
      onMouseDown={(e) => e.currentTarget.style.opacity = "0.8"}
      onMouseUp={(e) => e.currentTarget.style.opacity = "1"}
    >
      {Icon && <Icon size={15} />}
      {children}
    </button>
  );
}

function PageHeader({ title, subtitle, action }) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 24 }}>
      <div>
        <h1 style={{ fontFamily: "Georgia, serif", fontSize: 26, fontWeight: 700, color: COLOR.carbon, margin: 0 }}>{title}</h1>
        {subtitle && <p style={{ fontSize: 14, color: COLOR.carbonSuave, margin: "4px 0 0" }}>{subtitle}</p>}
      </div>
      {action}
    </div>
  );
}

function SearchBar({ placeholder, value, onChange }) {
  return (
    <div style={{
      display: "flex", alignItems: "center", gap: 8, background: "white",
      border: `1px solid ${COLOR.borde}`, borderRadius: 8, padding: "8px 12px", width: 280
    }}>
      <Search size={15} color={COLOR.carbonSuave} />
      <input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        style={{ border: "none", outline: "none", fontSize: 13.5, width: "100%", fontFamily: "inherit", background: "transparent" }}
      />
    </div>
  );
}

function Modal({ title, onClose, children, width = 520 }) {
  return (
    <div style={{
      position: "fixed", inset: 0, background: "rgba(54,52,50,0.45)", display: "flex",
      alignItems: "center", justifyContent: "center", zIndex: 100, padding: 20
    }} onClick={onClose}>
      <div onClick={(e) => e.stopPropagation()} style={{
        background: "white", borderRadius: 12, width, maxHeight: "85vh", overflow: "auto",
        boxShadow: "0 12px 40px rgba(0,0,0,0.18)"
      }}>
        <div style={{
          display: "flex", justifyContent: "space-between", alignItems: "center",
          padding: "18px 22px", borderBottom: `1px solid ${COLOR.borde}`
        }}>
          <h3 style={{ fontFamily: "Georgia, serif", fontSize: 18, fontWeight: 700, margin: 0, color: COLOR.carbon }}>{title}</h3>
          <button onClick={onClose} style={{ background: "none", border: "none", cursor: "pointer", color: COLOR.carbonSuave, padding: 4 }}>
            <X size={20} />
          </button>
        </div>
        <div style={{ padding: 22 }}>{children}</div>
      </div>
    </div>
  );
}

function Field({ label, children, style }) {
  return (
    <div style={{ marginBottom: 14, ...style }}>
      <label style={{ display: "block", fontSize: 12.5, fontWeight: 600, color: COLOR.carbonSuave, marginBottom: 5 }}>{label}</label>
      {children}
    </div>
  );
}

const inputStyle = {
  width: "100%", padding: "9px 11px", border: `1px solid ${COLOR.borde}`, borderRadius: 7,
  fontSize: 13.5, fontFamily: "inherit", outline: "none", boxSizing: "border-box"
};

function Input(props) { return <input {...props} style={{ ...inputStyle, ...props.style }} />; }
function Select({ children, ...props }) { return <select {...props} style={inputStyle}>{children}</select>; }

/* ============================================================
   SIDEBAR / NAVEGACIÓN
   ============================================================ */
const NAV_ITEMS = [
  { id: "dashboard", label: "Dashboard", icon: Home },
  { id: "propietarios", label: "Propietarios", icon: Users },
  { id: "inmuebles", label: "Inmuebles", icon: Building2 },
  { id: "alquiler", label: "Alquiler", icon: FileSignature },
  { id: "venta", label: "Venta", icon: Tag },
  { id: "arreglos", label: "Arreglos", icon: Wrench },
  { id: "reportes", label: "Reportes", icon: BarChart3 },
  { id: "configuracion", label: "Configuración", icon: Settings },
];

const ROLES = ["Administrador", "Asesor Interno", "Asesor Externo", "Consulta"];

function Sidebar({ active, onNavigate, rol, setRol }) {
  const [rolOpen, setRolOpen] = useState(false);
  const visibleItems = NAV_ITEMS.filter(item => {
    if (rol === "Asesor Externo") return ["dashboard", "venta"].includes(item.id);
    if (rol === "Consulta") return item.id !== "configuracion";
    if (rol === "Asesor Interno") return item.id !== "configuracion";
    return true;
  });

  return (
    <div style={{
      width: 232, background: COLOR.azulOscuro, height: "100vh", position: "fixed",
      display: "flex", flexDirection: "column", color: "white"
    }}>
      <div style={{ padding: "20px 18px", background: "white" }}>
        <LogoFull />
      </div>
      <div style={{ flex: 1, padding: "14px 10px", overflowY: "auto" }}>
        {visibleItems.map(item => {
          const Icon = item.icon;
          const isActive = active === item.id;
          return (
            <div
              key={item.id}
              onClick={() => onNavigate(item.id)}
              style={{
                display: "flex", alignItems: "center", gap: 11, padding: "10px 12px",
                borderRadius: 8, cursor: "pointer", marginBottom: 2, fontSize: 13.5, fontWeight: 600,
                background: isActive ? COLOR.mostaza : "transparent",
                color: isActive ? COLOR.carbon : "rgba(255,255,255,0.82)",
              }}
            >
              <Icon size={17} />
              {item.label}
            </div>
          );
        })}
      </div>
      <div style={{ padding: 14, borderTop: "1px solid rgba(255,255,255,0.12)", position: "relative" }}>
        <div onClick={() => setRolOpen(!rolOpen)} style={{
          display: "flex", alignItems: "center", gap: 10, cursor: "pointer", padding: "8px 10px",
          borderRadius: 8, background: "rgba(255,255,255,0.06)"
        }}>
          <UserCircle size={26} color="rgba(255,255,255,0.85)" />
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 12.5, fontWeight: 600 }}>Usuario demo</div>
            <div style={{ fontSize: 11, color: "rgba(255,255,255,0.6)" }}>{rol}</div>
          </div>
          <ChevronDown size={14} color="rgba(255,255,255,0.6)" />
        </div>
        {rolOpen && (
          <div style={{
            position: "absolute", bottom: "100%", left: 14, right: 14, background: "white",
            borderRadius: 8, marginBottom: 6, boxShadow: "0 4px 16px rgba(0,0,0,0.2)", overflow: "hidden"
          }}>
            <div style={{ padding: "8px 12px", fontSize: 11, color: COLOR.carbonSuave, fontWeight: 600, borderBottom: `1px solid ${COLOR.borde}` }}>
              Simular rol (demo)
            </div>
            {ROLES.map(r => (
              <div key={r} onClick={() => { setRol(r); setRolOpen(false); onNavigate("dashboard"); }} style={{
                padding: "9px 12px", fontSize: 13, cursor: "pointer", color: COLOR.carbon,
                background: r === rol ? COLOR.mostazaClaro : "white"
              }}>
                {r}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

/* ============================================================
   DASHBOARD
   ============================================================ */
function Dashboard({ onNavigate }) {
  const totalInmuebles = INMUEBLES.length;
  const arrendados = INMUEBLES.filter(i => i.estado === "Arrendado").length;
  const enMora = CONTRATOS.filter(c => estadoMora(c.diaPago).estado !== "ok").length;
  const proximosVencer = CONTRATOS.filter(c => {
    const fin = new Date(c.fechaFin);
    const hoy = new Date("2026-06-24");
    const dias = (fin - hoy) / (1000 * 60 * 60 * 24);
    return dias > 0 && dias <= 60;
  });

  const kpis = [
    { label: "Total inmuebles", valor: totalInmuebles, icon: Building2, color: COLOR.azul },
    { label: "Arrendados", valor: arrendados, icon: Check, color: COLOR.verde },
    { label: "En mora / afianzadora", valor: enMora, icon: AlertTriangle, color: COLOR.rojo },
    { label: "Contratos próx. a vencer", valor: proximosVencer.length, icon: Clock, color: COLOR.mostazaOscuro },
  ];

  return (
    <div>
      <PageHeader title="Dashboard" subtitle="Resumen general de la operación · hoy, 24 de junio de 2026" />

      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 14, marginBottom: 22 }}>
        {kpis.map((k, i) => (
          <Card key={i} style={{ position: "relative", overflow: "hidden" }}>
            <div style={{ position: "absolute", top: -2, left: 0, width: "100%", height: 3, background: COLOR.azul }} />
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
              <div>
                <div style={{ fontSize: 12.5, color: COLOR.carbonSuave, fontWeight: 600, marginBottom: 6 }}>{k.label}</div>
                <div style={{ fontSize: 30, fontWeight: 700, color: COLOR.carbon, fontFamily: "Georgia, serif" }}>{k.valor}</div>
              </div>
              <div style={{ background: k.color + "18", padding: 9, borderRadius: 9 }}>
                <k.icon size={18} color={k.color} />
              </div>
            </div>
          </Card>
        ))}
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1.3fr 1fr", gap: 16 }}>
        <Card>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14 }}>
            <h3 style={{ fontSize: 15, fontWeight: 700, margin: 0, color: COLOR.carbon }}>Alertas activas</h3>
            <Badge color={COLOR.rojo} bg={COLOR.rojoClaro}>3 nuevas</Badge>
          </div>
          {[
            { tipo: "Mora", texto: "Comercializadora El Faro Ltda. — contrato #3, día 8, recargo activo", color: COLOR.mostazaOscuro },
            { tipo: "IPC", texto: "Enero: pendiente actualizar valor de IPC del año en curso", color: COLOR.azul },
            { tipo: "Vencimiento", texto: "Contrato #3 (Local, Av. 6N) vence en 21 días — recordar renovación", color: COLOR.rojo },
          ].map((a, i) => (
            <div key={i} style={{
              display: "flex", gap: 12, padding: "11px 0",
              borderBottom: i < 2 ? `1px solid ${COLOR.borde}` : "none"
            }}>
              <Bell size={15} color={a.color} style={{ marginTop: 2, flexShrink: 0 }} />
              <div>
                <div style={{ fontSize: 12, fontWeight: 700, color: a.color, marginBottom: 2 }}>{a.tipo}</div>
                <div style={{ fontSize: 13.5, color: COLOR.carbon }}>{a.texto}</div>
              </div>
            </div>
          ))}
        </Card>

        <Card>
          <h3 style={{ fontSize: 15, fontWeight: 700, margin: "0 0 14px", color: COLOR.carbon }}>Accesos rápidos</h3>
          {[
            { label: "Crear propietario", icon: Users, target: "propietarios" },
            { label: "Crear inmueble", icon: Building2, target: "inmuebles" },
            { label: "Nuevo contrato de alquiler", icon: FileSignature, target: "alquiler" },
            { label: "Ver reportes", icon: BarChart3, target: "reportes" },
          ].map((a, i) => (
            <div key={i} onClick={() => onNavigate(a.target)} style={{
              display: "flex", alignItems: "center", gap: 10, padding: "10px 8px",
              borderRadius: 8, cursor: "pointer", marginBottom: 2
            }}
              onMouseEnter={(e) => e.currentTarget.style.background = COLOR.mostazaClaro}
              onMouseLeave={(e) => e.currentTarget.style.background = "transparent"}
            >
              <a.icon size={16} color={COLOR.azul} />
              <span style={{ fontSize: 13.5, color: COLOR.carbon, flex: 1 }}>{a.label}</span>
              <ChevronRight size={14} color={COLOR.carbonSuave} />
            </div>
          ))}
        </Card>
      </div>
    </div>
  );
}

/* ============================================================
   PROPIETARIOS
   ============================================================ */
function Propietarios() {
  const [busqueda, setBusqueda] = useState("");
  const [seleccionado, setSeleccionado] = useState(null);
  const [modalNuevo, setModalNuevo] = useState(false);

  const filtrados = PROPIETARIOS.filter(p =>
    p.nombre.toLowerCase().includes(busqueda.toLowerCase()) ||
    p.identificacion.toLowerCase().includes(busqueda.toLowerCase())
  );

  if (seleccionado) {
    const p = PROPIETARIOS.find(x => x.id === seleccionado);
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
              { icon: CreditCard, label: `${p.banco} · ${p.cuenta}` },
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
                  <EstadoInmuebleBadge estado={i.estado} />
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
        subtitle={`${PROPIETARIOS.length} propietarios registrados`}
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

/* ============================================================
   INMUEBLES
   ============================================================ */
function Inmuebles() {
  const [busqueda, setBusqueda] = useState("");
  const [filtroEstado, setFiltroEstado] = useState("Todos");
  const [seleccionado, setSeleccionado] = useState(null);
  const [modalNuevo, setModalNuevo] = useState(false);

  const filtrados = INMUEBLES.filter(i => {
    const matchBusqueda = i.direccion.toLowerCase().includes(busqueda.toLowerCase()) || i.barrio.toLowerCase().includes(busqueda.toLowerCase());
    const matchEstado = filtroEstado === "Todos" || i.estado === filtroEstado;
    return matchBusqueda && matchEstado;
  });

  if (seleccionado) {
    const inm = INMUEBLES.find(x => x.id === seleccionado);
    const prop = PROPIETARIOS.find(p => p.id === inm.propietarioId);
    const contrato = CONTRATOS.find(c => c.inmuebleId === inm.id);
    const arrendatario = contrato ? ARRENDATARIOS.find(a => a.id === contrato.arrendatarioId) : null;
    const historialArreglos = ARREGLOS.filter(a => a.inmuebleId === inm.id);

    return (
      <div>
        <div onClick={() => setSeleccionado(null)} style={{ display: "flex", alignItems: "center", gap: 6, color: COLOR.azul, fontSize: 13.5, fontWeight: 600, cursor: "pointer", marginBottom: 16 }}>
          <ChevronLeft size={15} /> Volver a inmuebles
        </div>
        <PageHeader
          title={`${inm.tipo} · ${inm.barrio}`}
          subtitle={inm.direccion}
          action={<EstadoInmuebleBadge estado={inm.estado} />}
        />
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 16 }}>
          <Card>
            <h3 style={{ fontSize: 14, fontWeight: 700, margin: "0 0 14px", color: COLOR.carbon }}>Ficha del inmueble</h3>
            {[
              ["Tipo", inm.tipo], ["Barrio / Ciudad", `${inm.barrio}, Cali`], ["Estrato", inm.estrato],
              ["Área", `${inm.area} m²`], ["Canon mensual", money(inm.canon)], ["% Administración", `${inm.pctAdmin}%`],
              ["Preaviso de entrega", `${inm.preaviso} meses`], ["Propietario", prop.nombre],
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

            <h3 style={{ fontSize: 14, fontWeight: 700, margin: "16px 0 10px", color: COLOR.carbon }}>Fianzas asociadas</h3>
            {inm.fianzas.length === 0 ? (
              <p style={{ fontSize: 13, color: COLOR.carbonSuave, margin: 0 }}>Sin fianzas asociadas.</p>
            ) : inm.fianzas.map((f, i) => <Badge key={i} color={COLOR.azul} bg={COLOR.azulClaro} style={{ marginRight: 6, marginBottom: 6 }}>{f}</Badge>)}
          </Card>
        </div>

        <Card>
          <h3 style={{ fontSize: 14, fontWeight: 700, margin: "0 0 14px", color: COLOR.carbon }}>Historial</h3>
          {contrato && (
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "10px 0", borderBottom: `1px solid ${COLOR.borde}` }}>
              <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
                <FileSignature size={15} color={COLOR.azul} />
                <span style={{ fontSize: 13.5 }}>Contrato activo con {arrendatario.nombre} · desde {contrato.fechaInicio}</span>
              </div>
              <Badge color={COLOR.verde} bg={COLOR.verdeClaro}>{contrato.estado}</Badge>
            </div>
          )}
          {historialArreglos.map(a => (
            <div key={a.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "10px 0", borderBottom: `1px solid ${COLOR.borde}` }}>
              <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
                <Wrench size={15} color={COLOR.mostazaOscuro} />
                <span style={{ fontSize: 13.5 }}>{a.descripcion} · {a.fecha}</span>
              </div>
              <span style={{ fontSize: 13.5, fontWeight: 600 }}>{money(a.costoTotal)}</span>
            </div>
          ))}
          {!contrato && historialArreglos.length === 0 && (
            <p style={{ fontSize: 13, color: COLOR.carbonSuave, margin: 0 }}>Sin historial registrado todavía.</p>
          )}
        </Card>
      </div>
    );
  }

  return (
    <div>
      <PageHeader
        title="Inmuebles"
        subtitle={`${INMUEBLES.length} inmuebles registrados`}
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
          const prop = PROPIETARIOS.find(p => p.id === inm.propietarioId);
          return (
            <Card key={inm.id} style={{ cursor: "pointer" }} onClick={() => setSeleccionado(inm.id)}>
              <div style={{ aspectRatio: "16/9", background: COLOR.fondo, borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center", marginBottom: 12, border: `1px solid ${COLOR.borde}` }}>
                <Building2 size={28} color={COLOR.borde} />
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 6 }}>
                <div style={{ fontSize: 14, fontWeight: 700, color: COLOR.carbon }}>{inm.tipo} · {inm.barrio}</div>
                <EstadoInmuebleBadge estado={inm.estado} />
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

      {modalNuevo && (
        <Modal title="Crear inmueble" onClose={() => setModalNuevo(false)} width={580}>
          <div style={{ display: "flex", gap: 10 }}>
            <Field label="Tipo de inmueble" style={{ flex: 1 }}>
              <Select><option>Apartamento</option><option>Casa</option><option>Local</option><option>Bodega</option><option>Oficina</option></Select>
            </Field>
            <Field label="Propietario" style={{ flex: 1 }}>
              <Select>{PROPIETARIOS.map(p => <option key={p.id}>{p.nombre}</option>)}</Select>
            </Field>
          </div>
          <Field label="Dirección"><Input placeholder="Dirección completa" /></Field>
          <div style={{ display: "flex", gap: 10 }}>
            <Field label="Barrio" style={{ flex: 1 }}><Input placeholder="Barrio" /></Field>
            <Field label="Estrato" style={{ flex: 1 }}><Select><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option><option>6</option></Select></Field>
            <Field label="Área (m²)" style={{ flex: 1 }}><Input type="number" placeholder="80" /></Field>
          </div>
          <div style={{ display: "flex", gap: 10 }}>
            <Field label="Canon de arrendamiento" style={{ flex: 1 }}><Input placeholder="$ 1.500.000" /></Field>
            <Field label="% Administración" style={{ flex: 1 }}><Select><option>10%</option><option>11%</option><option>12%</option></Select></Field>
            <Field label="Preaviso (meses)" style={{ flex: 1 }}><Select><option>2</option><option>3</option></Select></Field>
          </div>
          <Field label="Fotos">
            <div style={{ border: `1px dashed ${COLOR.borde}`, borderRadius: 8, padding: 20, textAlign: "center" }}>
              <Upload size={18} color={COLOR.carbonSuave} style={{ marginBottom: 6 }} />
              <div style={{ fontSize: 12.5, color: COLOR.carbonSuave }}>Arrastra fotos o haz clic para subir</div>
            </div>
          </Field>
          <div style={{ display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 18 }}>
            <Button variant="secondary" onClick={() => setModalNuevo(false)}>Cancelar</Button>
            <Button onClick={() => setModalNuevo(false)}>Guardar inmueble</Button>
          </div>
        </Modal>
      )}
    </div>
  );
}

/* ============================================================
   ALQUILER — el módulo más complejo: contratos, recibos, mora, liquidación
   ============================================================ */
function Alquiler() {
  const [tab, setTab] = useState("contratos");
  const [modalContrato, setModalContrato] = useState(false);
  const [contratoSel, setContratoSel] = useState(null);
  const [simDia, setSimDia] = useState(8);

  const tabs = [
    { id: "contratos", label: "Contratos" },
    { id: "recibos", label: "Recibos y pagos" },
    { id: "mora", label: "Mora y afianzadora" },
    { id: "liquidacion", label: "Liquidación" },
  ];

  return (
    <div>
      <PageHeader
        title="Alquiler"
        subtitle="Contratos, recibos, control de mora y liquidación a propietarios"
        action={tab === "contratos" && <Button icon={Plus} onClick={() => setModalContrato(true)}>Nuevo contrato</Button>}
      />

      <div style={{ display: "flex", gap: 4, borderBottom: `1px solid ${COLOR.borde}`, marginBottom: 20 }}>
        {tabs.map(t => (
          <div key={t.id} onClick={() => setTab(t.id)} style={{
            padding: "10px 16px", fontSize: 13.5, fontWeight: 600, cursor: "pointer",
            color: tab === t.id ? COLOR.azul : COLOR.carbonSuave,
            borderBottom: tab === t.id ? `2px solid ${COLOR.azul}` : "2px solid transparent"
          }}>{t.label}</div>
        ))}
      </div>

      {tab === "contratos" && (
        <Card style={{ padding: 0, overflow: "hidden" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13.5 }}>
            <thead>
              <tr style={{ background: COLOR.fondo, borderBottom: `1px solid ${COLOR.borde}` }}>
                {["Inmueble", "Arrendatario", "Inicio", "Vence", "Canon vigente", "Estado", ""].map((h, i) => (
                  <th key={i} style={{ textAlign: "left", padding: "11px 16px", fontSize: 12, color: COLOR.carbonSuave, fontWeight: 700, textTransform: "uppercase" }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {CONTRATOS.map(c => {
                const inm = INMUEBLES.find(i => i.id === c.inmuebleId);
                const arr = ARRENDATARIOS.find(a => a.id === c.arrendatarioId);
                return (
                  <tr key={c.id} onClick={() => setContratoSel(c.id)} style={{ borderBottom: `1px solid ${COLOR.borde}`, cursor: "pointer" }}
                    onMouseEnter={(e) => e.currentTarget.style.background = COLOR.fondo}
                    onMouseLeave={(e) => e.currentTarget.style.background = "white"}>
                    <td style={{ padding: "13px 16px", fontWeight: 600 }}>{inm.tipo} · {inm.barrio}</td>
                    <td style={{ padding: "13px 16px" }}>{arr.nombre}</td>
                    <td style={{ padding: "13px 16px", color: COLOR.carbonSuave }}>{c.fechaInicio}</td>
                    <td style={{ padding: "13px 16px", color: COLOR.carbonSuave }}>{c.fechaFin}</td>
                    <td style={{ padding: "13px 16px", fontWeight: 600 }}>{money(c.canonVigente)}</td>
                    <td style={{ padding: "13px 16px" }}><Badge color={COLOR.verde} bg={COLOR.verdeClaro}>{c.estado}</Badge></td>
                    <td style={{ padding: "13px 16px", textAlign: "right" }}><ChevronRight size={16} color={COLOR.carbonSuave} /></td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </Card>
      )}

      {tab === "recibos" && <RecibosPanel />}
      {tab === "mora" && <MoraPanel simDia={simDia} setSimDia={setSimDia} />}
      {tab === "liquidacion" && <LiquidacionPanel />}

      {contratoSel && <ContratoDetalle contratoId={contratoSel} onClose={() => setContratoSel(null)} />}
      {modalContrato && <NuevoContratoModal onClose={() => setModalContrato(false)} />}
    </div>
  );
}

function ContratoDetalle({ contratoId, onClose }) {
  const c = CONTRATOS.find(x => x.id === contratoId);
  const inm = INMUEBLES.find(i => i.id === c.inmuebleId);
  const arr = ARRENDATARIOS.find(a => a.id === c.arrendatarioId);
  const mora = estadoMora(c.diaPago);
  const [pagoRegistrado, setPagoRegistrado] = useState(true);

  return (
    <Modal title={`Contrato · ${inm.tipo} ${inm.barrio}`} onClose={onClose} width={620}>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 16 }}>
        <div>
          <div style={{ fontSize: 12, color: COLOR.carbonSuave, marginBottom: 3 }}>Arrendatario</div>
          <div style={{ fontSize: 14, fontWeight: 600 }}>{arr.nombre}</div>
        </div>
        <div>
          <div style={{ fontSize: 12, color: COLOR.carbonSuave, marginBottom: 3 }}>Canon vigente</div>
          <div style={{ fontSize: 14, fontWeight: 600 }}>{money(c.canonVigente)}</div>
        </div>
        <div>
          <div style={{ fontSize: 12, color: COLOR.carbonSuave, marginBottom: 3 }}>Duración</div>
          <div style={{ fontSize: 14, fontWeight: 600 }}>{c.duracion} meses ({c.fechaInicio} → {c.fechaFin})</div>
        </div>
        <div>
          <div style={{ fontSize: 12, color: COLOR.carbonSuave, marginBottom: 3 }}>Estado de pago (mes actual)</div>
          <Badge color={mora.color} bg={mora.bg}>{mora.label}</Badge>
        </div>
      </div>

      <div style={{ background: COLOR.fondo, borderRadius: 8, padding: 14, marginBottom: 16 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div>
            <div style={{ fontSize: 13, fontWeight: 600, color: COLOR.carbon }}>Pago del mes en curso</div>
            <div style={{ fontSize: 12, color: COLOR.carbonSuave }}>{pagoRegistrado ? "Pago registrado el día 8 de junio" : "Sin registrar"}</div>
          </div>
          {!pagoRegistrado ? (
            <Button size="sm" onClick={() => setPagoRegistrado(true)}>Registrar pago</Button>
          ) : (
            <Badge color={COLOR.verde} bg={COLOR.verdeClaro}><Check size={12} /> Registrado</Badge>
          )}
        </div>
      </div>

      <div style={{ display: "flex", gap: 8 }}>
        <Button icon={FileText} variant={pagoRegistrado ? "primary" : "secondary"} style={!pagoRegistrado ? { opacity: 0.5, cursor: "not-allowed" } : {}}>
          Generar recibo PDF
        </Button>
        <Button icon={Mail} variant="secondary">Enviar al arrendatario</Button>
        <Button icon={Calendar} variant="secondary">Renovar contrato</Button>
      </div>
      {!pagoRegistrado && (
        <p style={{ fontSize: 12, color: COLOR.rojo, marginTop: 8 }}>El recibo solo se puede generar una vez registrado el pago (RN-01).</p>
      )}
    </Modal>
  );
}

function NuevoContratoModal({ onClose }) {
  const disponibles = INMUEBLES.filter(i => i.estado === "Disponible");
  const [duracion, setDuracion] = useState(12);
  const [fechaInicio, setFechaInicio] = useState("2026-07-01");
  const [numCodeudores, setNumCodeudores] = useState(1);

  const fechaFinCalculada = useMemo(() => {
    const d = new Date(fechaInicio);
    d.setMonth(d.getMonth() + Number(duracion));
    d.setDate(d.getDate() - 1);
    return d.toISOString().split("T")[0];
  }, [fechaInicio, duracion]);

  return (
    <Modal title="Nuevo contrato de alquiler" onClose={onClose} width={620}>
      <Field label="Inmueble disponible">
        <Select>
          {disponibles.length === 0 && <option>No hay inmuebles disponibles</option>}
          {disponibles.map(i => <option key={i.id}>{i.tipo} · {i.barrio} — {i.direccion} ({money(i.canon)})</option>)}
        </Select>
      </Field>
      <Field label="Arrendatario">
        <Select><option>Crear nuevo arrendatario...</option>{ARRENDATARIOS.map(a => <option key={a.id}>{a.nombre}</option>)}</Select>
      </Field>
      <Field label={`Codeudores (0–3)`}>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <Select value={numCodeudores} onChange={(e) => setNumCodeudores(Number(e.target.value))} style={{ width: 100 }}>
            <option value={0}>0</option><option value={1}>1</option><option value={2}>2</option><option value={3}>3</option>
          </Select>
          <span style={{ fontSize: 12.5, color: COLOR.carbonSuave }}>codeudor(es) — mismos datos que el arrendatario</span>
        </div>
      </Field>
      <div style={{ display: "flex", gap: 10 }}>
        <Field label="Fecha de inicio" style={{ flex: 1 }}>
          <Input type="date" value={fechaInicio} onChange={(e) => setFechaInicio(e.target.value)} />
        </Field>
        <Field label="Duración" style={{ flex: 1 }}>
          <Select value={duracion} onChange={(e) => setDuracion(e.target.value)}>
            <option value={3}>3 meses</option><option value={6}>6 meses</option><option value={12}>12 meses</option>
            <option value={24}>24 meses</option><option value={36}>36 meses</option>
          </Select>
        </Field>
      </div>
      <div style={{ background: COLOR.azulClaro, borderRadius: 8, padding: "10px 12px", marginBottom: 14, display: "flex", justifyContent: "space-between" }}>
        <span style={{ fontSize: 13, color: COLOR.azul, fontWeight: 600 }}>Fecha fin calculada automáticamente</span>
        <span style={{ fontSize: 13, fontWeight: 700, color: COLOR.azul }}>{fechaFinCalculada}</span>
      </div>
      <div style={{ display: "flex", gap: 10 }}>
        <Field label="% Administración" style={{ flex: 1 }}><Select><option>10%</option><option>11%</option><option>12%</option></Select></Field>
        <Field label="Preaviso de entrega" style={{ flex: 1 }}><Select><option>2 meses</option><option>3 meses</option></Select></Field>
        <Field label="N° de personas" style={{ flex: 1 }}><Input type="number" placeholder="2" /></Field>
      </div>
      <Field label="Afianzadora y tipo de fianza">
        <div style={{ display: "flex", gap: 8 }}>
          <Select style={{ flex: 1 }}><option>AFFI</option><option>Fianzas de Colombia</option></Select>
          <Select style={{ flex: 1 }}><option>Canon (2%)</option><option>Integral (3%)</option><option>Servicios (1.5%)</option></Select>
        </div>
      </Field>
      <div style={{ display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 18 }}>
        <Button variant="secondary" onClick={onClose}>Cancelar</Button>
        <Button onClick={onClose}>Guardar contrato</Button>
      </div>
    </Modal>
  );
}

function RecibosPanel() {
  const [diaInicio, setDiaInicio] = useState(20);
  const canonEjemplo = 800000;
  const diasRestantes = 30 - diaInicio;
  const valorDias = Math.round((canonEjemplo / 30) * diasRestantes);
  const generaDoble = diaInicio > 15;

  return (
    <div>
      <Card style={{ marginBottom: 16 }}>
        <h3 style={{ fontSize: 14, fontWeight: 700, margin: "0 0 6px", color: COLOR.carbon }}>Simulador de prorrateo (primer recibo)</h3>
        <p style={{ fontSize: 12.5, color: COLOR.carbonSuave, margin: "0 0 14px" }}>Regla RN-02 / RN-04: si el contrato inicia después del día 15, se generan dos recibos.</p>
        <div style={{ display: "flex", gap: 20, alignItems: "center" }}>
          <div style={{ flex: 1 }}>
            <label style={{ fontSize: 12.5, color: COLOR.carbonSuave, fontWeight: 600 }}>Día de inicio del contrato: {diaInicio}</label>
            <input type="range" min={1} max={29} value={diaInicio} onChange={(e) => setDiaInicio(Number(e.target.value))} style={{ width: "100%", marginTop: 8 }} />
          </div>
          <div style={{ fontSize: 13, color: COLOR.carbonSuave }}>Canon ejemplo: <b style={{ color: COLOR.carbon }}>{money(canonEjemplo)}</b></div>
        </div>

        <div style={{ display: "flex", gap: 12, marginTop: 16 }}>
          <div style={{ flex: 1, background: COLOR.fondo, borderRadius: 8, padding: 14 }}>
            <div style={{ fontSize: 12, fontWeight: 700, color: COLOR.azul, marginBottom: 4 }}>RECIBO 1 — Días</div>
            <div style={{ fontSize: 12.5, color: COLOR.carbonSuave, marginBottom: 8 }}>Días {diaInicio} al 30 ({diasRestantes} días) · {money(canonEjemplo)} / 30 × {diasRestantes}</div>
            <div style={{ fontSize: 22, fontWeight: 700, color: COLOR.carbon, fontFamily: "Georgia, serif" }}>{money(valorDias)}</div>
          </div>
          {generaDoble && (
            <div style={{ flex: 1, background: COLOR.mostazaClaro, borderRadius: 8, padding: 14 }}>
              <div style={{ fontSize: 12, fontWeight: 700, color: COLOR.mostazaOscuro, marginBottom: 4 }}>RECIBO 2 — Mensualidad</div>
              <div style={{ fontSize: 12.5, color: COLOR.carbonSuave, marginBottom: 8 }}>Mes siguiente completo</div>
              <div style={{ fontSize: 22, fontWeight: 700, color: COLOR.carbon, fontFamily: "Georgia, serif" }}>{money(canonEjemplo)}</div>
            </div>
          )}
        </div>
        {generaDoble && (
          <div style={{ marginTop: 10, fontSize: 12.5, color: COLOR.mostazaOscuro, display: "flex", alignItems: "center", gap: 6 }}>
            <AlertTriangle size={14} /> Inicio después del día 15: se generan dos recibos simultáneamente (RN-04).
          </div>
        )}
      </Card>

      <Card style={{ padding: 0, overflow: "hidden" }}>
        <div style={{ padding: "14px 16px", borderBottom: `1px solid ${COLOR.borde}`, fontWeight: 700, fontSize: 14 }}>Recibos recientes</div>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13.5 }}>
          <thead>
            <tr style={{ background: COLOR.fondo }}>
              {["Arrendatario", "Tipo", "Período", "Valor", "Método", "Estado"].map((h, i) => (
                <th key={i} style={{ textAlign: "left", padding: "10px 16px", fontSize: 12, color: COLOR.carbonSuave, fontWeight: 700, textTransform: "uppercase" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {[
              { arr: "Carlos Andrés Mejía Londoño", tipo: "Mensualidad", periodo: "Junio 2026", valor: 1450000, metodo: "Transferencia", estado: "PAGADO" },
              { arr: "Diana Patricia Rojas Tamayo", tipo: "Mensualidad", periodo: "Junio 2026", valor: 2100000, metodo: "Efectivo", estado: "PAGADO" },
              { arr: "Comercializadora El Faro Ltda", tipo: "Mensualidad", periodo: "Junio 2026", valor: 1850000, metodo: "—", estado: "PENDIENTE" },
              { arr: "Andrés Felipe Gómez Cardona", tipo: "Mensualidad", periodo: "Junio 2026", valor: 1980000, metodo: "Transferencia", estado: "PAGADO" },
            ].map((r, i) => (
              <tr key={i} style={{ borderBottom: `1px solid ${COLOR.borde}` }}>
                <td style={{ padding: "12px 16px", fontWeight: 600 }}>{r.arr}</td>
                <td style={{ padding: "12px 16px", color: COLOR.carbonSuave }}>{r.tipo}</td>
                <td style={{ padding: "12px 16px", color: COLOR.carbonSuave }}>{r.periodo}</td>
                <td style={{ padding: "12px 16px", fontWeight: 600 }}>{money(r.valor)}</td>
                <td style={{ padding: "12px 16px", color: COLOR.carbonSuave }}>{r.metodo}</td>
                <td style={{ padding: "12px 16px" }}>
                  <Badge color={r.estado === "PAGADO" ? COLOR.verde : COLOR.mostazaOscuro} bg={r.estado === "PAGADO" ? COLOR.verdeClaro : COLOR.mostazaClaro}>{r.estado}</Badge>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  );
}

function MoraPanel({ simDia, setSimDia }) {
  const canonEjemplo = 1200000;
  const diasRecargo = simDia >= 6 ? Math.min(simDia, 10) - 5 : 0;
  const recargo = Math.round(canonEjemplo * 0.0176 * diasRecargo);

  const rangos = [
    { rango: "Días 1–5", label: "Sin recargo", color: COLOR.verde, bg: COLOR.verdeClaro, activo: simDia <= 5 },
    { rango: "Días 6–10", label: "Recargo 1,76% diario", color: COLOR.mostazaOscuro, bg: COLOR.mostazaClaro, activo: simDia > 5 && simDia <= 10 },
    { rango: "Después del día 10", label: "Bloqueo · pasa a afianzadora", color: COLOR.rojo, bg: COLOR.rojoClaro, activo: simDia > 10 },
  ];

  return (
    <div>
      <Card style={{ marginBottom: 16 }}>
        <h3 style={{ fontSize: 14, fontWeight: 700, margin: "0 0 6px", color: COLOR.carbon }}>Simulador de mora</h3>
        <p style={{ fontSize: 12.5, color: COLOR.carbonSuave, margin: "0 0 14px" }}>Ajusta el día del mes para ver cómo cambia el estado del contrato (RN-07 / RN-08 / RN-09).</p>
        <label style={{ fontSize: 12.5, color: COLOR.carbonSuave, fontWeight: 600 }}>Día del mes: {simDia}</label>
        <input type="range" min={1} max={15} value={simDia} onChange={(e) => setSimDia(Number(e.target.value))} style={{ width: "100%", margin: "8px 0 16px" }} />

        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 10 }}>
          {rangos.map((r, i) => (
            <div key={i} style={{
              padding: 14, borderRadius: 8, background: r.activo ? r.bg : COLOR.fondo,
              border: r.activo ? `2px solid ${r.color}` : `1px solid ${COLOR.borde}`, transition: "all 0.15s"
            }}>
              <div style={{ fontSize: 12, fontWeight: 700, color: r.activo ? r.color : COLOR.carbonSuave }}>{r.rango}</div>
              <div style={{ fontSize: 13, fontWeight: 600, color: COLOR.carbon, marginTop: 2 }}>{r.label}</div>
            </div>
          ))}
        </div>

        {simDia > 5 && simDia <= 10 && (
          <div style={{ marginTop: 14, background: COLOR.fondo, borderRadius: 8, padding: 12, fontSize: 13 }}>
            Recargo sobre canon de {money(canonEjemplo)}: <b>{money(canonEjemplo)} × 1,76% × {diasRecargo} día(s) = {money(recargo)}</b>
          </div>
        )}
        {simDia > 10 && (
          <div style={{ marginTop: 14, background: COLOR.rojoClaro, borderRadius: 8, padding: 12, fontSize: 13, color: COLOR.rojo, display: "flex", alignItems: "center", gap: 8 }}>
            <AlertTriangle size={15} /> "El plazo de pago venció. Este caso debe tramitarse a través de la afianzadora." — botón de pago deshabilitado.
          </div>
        )}
      </Card>

      <Card style={{ padding: 0, overflow: "hidden" }}>
        <div style={{ padding: "14px 16px", borderBottom: `1px solid ${COLOR.borde}`, fontWeight: 700, fontSize: 14 }}>Reporte de mora / afianzadora</div>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13.5 }}>
          <thead>
            <tr style={{ background: COLOR.fondo }}>
              {["Arrendatario", "Inmueble", "Días de atraso", "Valor recargo", "Afianzadora", "Estado"].map((h, i) => (
                <th key={i} style={{ textAlign: "left", padding: "10px 16px", fontSize: 12, color: COLOR.carbonSuave, fontWeight: 700, textTransform: "uppercase" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            <tr style={{ borderBottom: `1px solid ${COLOR.borde}` }}>
              <td style={{ padding: "12px 16px", fontWeight: 600 }}>Comercializadora El Faro Ltda</td>
              <td style={{ padding: "12px 16px" }}>Casa · El Ingenio</td>
              <td style={{ padding: "12px 16px" }}>3 días</td>
              <td style={{ padding: "12px 16px", fontWeight: 600 }}>{money(1850000 * 0.0176 * 3)}</td>
              <td style={{ padding: "12px 16px", color: COLOR.carbonSuave }}>AFFI</td>
              <td style={{ padding: "12px 16px" }}><Badge color={COLOR.mostazaOscuro} bg={COLOR.mostazaClaro}>Con recargo</Badge></td>
            </tr>
          </tbody>
        </table>
      </Card>
    </div>
  );
}

function LiquidacionPanel() {
  const [propietarioId, setPropietarioId] = useState(3);
  const [filtro, setFiltro] = useState("Todos");
  const prop = PROPIETARIOS.find(p => p.id === propietarioId);
  const inmueblesProp = INMUEBLES.filter(i => prop.inmuebles.includes(i.id) && i.estado === "Arrendado");
  const esConsolidada = inmueblesProp.length >= 4;

  const calcular = (inm) => {
    const admin = Math.round(inm.canon * inm.pctAdmin / 100);
    const fianza = inm.fianzas.length > 0 ? Math.round(inm.canon * 0.02) : 0;
    const neto = inm.canon - admin - fianza;
    return { admin, fianza, neto };
  };

  const totalNeto = inmueblesProp.reduce((sum, i) => sum + calcular(i).neto, 0);

  return (
    <div>
      <Card style={{ marginBottom: 16 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
          <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
            <Select value={propietarioId} onChange={(e) => setPropietarioId(Number(e.target.value))} style={{ width: 280 }}>
              {PROPIETARIOS.map(p => <option key={p.id} value={p.id}>{p.nombre}</option>)}
            </Select>
            <Badge color={esConsolidada ? COLOR.mostazaOscuro : COLOR.azul} bg={esConsolidada ? COLOR.mostazaClaro : COLOR.azulClaro}>
              {esConsolidada ? "Liquidación consolidada (4+ inmuebles)" : "Liquidación individual"}
            </Badge>
          </div>
          <Button icon={Download} variant="secondary">Exportar PDF</Button>
        </div>

        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13.5 }}>
          <thead>
            <tr style={{ borderBottom: `2px solid ${COLOR.borde}` }}>
              {["Inmueble", "Canon", "Administración", "Fianza", "Neto a transferir"].map((h, i) => (
                <th key={i} style={{ textAlign: i === 0 ? "left" : "right", padding: "8px 10px", fontSize: 12, color: COLOR.carbonSuave, fontWeight: 700, textTransform: "uppercase" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {inmueblesProp.map(inm => {
              const c = calcular(inm);
              return (
                <tr key={inm.id} style={{ borderBottom: `1px solid ${COLOR.borde}` }}>
                  <td style={{ padding: "10px", fontWeight: 600 }}>{inm.tipo} · {inm.barrio}</td>
                  <td style={{ padding: "10px", textAlign: "right" }}>{money(inm.canon)}</td>
                  <td style={{ padding: "10px", textAlign: "right", color: COLOR.rojo }}>-{money(c.admin)}</td>
                  <td style={{ padding: "10px", textAlign: "right", color: COLOR.rojo }}>-{money(c.fianza)}</td>
                  <td style={{ padding: "10px", textAlign: "right", fontWeight: 700 }}>{money(c.neto)}</td>
                </tr>
              );
            })}
            {inmueblesProp.length === 0 && (
              <tr><td colSpan={5} style={{ padding: 20, textAlign: "center", color: COLOR.carbonSuave }}>Este propietario no tiene inmuebles arrendados con pago registrado.</td></tr>
            )}
          </tbody>
          {inmueblesProp.length > 0 && (
            <tfoot>
              <tr style={{ borderTop: `2px solid ${COLOR.borde}` }}>
                <td colSpan={4} style={{ padding: "12px 10px", fontWeight: 700, textAlign: "right" }}>Total neto a transferir</td>
                <td style={{ padding: "12px 10px", textAlign: "right", fontWeight: 700, fontSize: 16, color: COLOR.azul }}>{money(totalNeto)}</td>
              </tr>
            </tfoot>
          )}
        </table>
      </Card>

      <div style={{ display: "flex", gap: 6 }}>
        {["Todos", "Pendientes por liquidar", "Liquidados", "En mora"].map(f => (
          <div key={f} onClick={() => setFiltro(f)} style={{
            padding: "7px 13px", borderRadius: 7, fontSize: 12.5, fontWeight: 600, cursor: "pointer",
            background: filtro === f ? COLOR.azul : "white", color: filtro === f ? "white" : COLOR.carbon,
            border: `1px solid ${filtro === f ? COLOR.azul : COLOR.borde}`
          }}>{f}</div>
        ))}
      </div>
    </div>
  );
}

/* ============================================================
   VENTA
   ============================================================ */
function Venta() {
  const [modalNuevo, setModalNuevo] = useState(false);
  const disponiblesVenta = INMUEBLES.filter(i => i.destino === "VENTA");

  const estadoColor = {
    "Disponible": { color: COLOR.azul, bg: COLOR.azulClaro },
    "En negociación": { color: COLOR.mostazaOscuro, bg: COLOR.mostazaClaro },
    "Vendido": { color: COLOR.verde, bg: COLOR.verdeClaro },
    "Inactivo": { color: COLOR.carbonSuave, bg: COLOR.fondo },
  };

  return (
    <div>
      <PageHeader title="Venta" subtitle="Fichas de venta, comisiones y estados" action={<Button icon={Plus} onClick={() => setModalNuevo(true)}>Crear ficha de venta</Button>} />

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 14 }}>
        {VENTAS.map(v => {
          const inm = INMUEBLES.find(i => i.id === v.inmuebleId);
          const comisionValor = Math.round(v.precio * v.comision / 100);
          const e = estadoColor[v.estado];
          return (
            <Card key={v.id}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 10 }}>
                <div style={{ fontSize: 14, fontWeight: 700, color: COLOR.carbon }}>{inm.tipo} · {inm.barrio}</div>
                <Badge color={e.color} bg={e.bg}>{v.estado}</Badge>
              </div>
              <div style={{ fontSize: 12.5, color: COLOR.carbonSuave, marginBottom: 14 }}>{inm.direccion}</div>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
                <span style={{ fontSize: 12.5, color: COLOR.carbonSuave }}>Precio de venta</span>
                <span style={{ fontSize: 14, fontWeight: 700 }}>{money(v.precio)}</span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
                <span style={{ fontSize: 12.5, color: COLOR.carbonSuave }}>Comisión ({v.comision}%)</span>
                <span style={{ fontSize: 13.5, fontWeight: 600, color: COLOR.azul }}>{money(comisionValor)}</span>
              </div>
              <div style={{ borderTop: `1px solid ${COLOR.borde}`, paddingTop: 10, marginTop: 8 }}>
                <span style={{ fontSize: 12, color: COLOR.carbonSuave }}>Responsable: </span>
                <span style={{ fontSize: 12.5, fontWeight: 600 }}>{v.responsable}</span>
              </div>
            </Card>
          );
        })}
        {disponiblesVenta.filter(i => !VENTAS.find(v => v.inmuebleId === i.id)).map(inm => (
          <Card key={inm.id} style={{ border: `1px dashed ${COLOR.borde}`, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", color: COLOR.carbonSuave }}>
            <Tag size={20} style={{ marginBottom: 8 }} />
            <div style={{ fontSize: 13, fontWeight: 600, textAlign: "center" }}>{inm.tipo} · {inm.barrio}</div>
            <div style={{ fontSize: 12, marginTop: 4 }}>Sin ficha de venta creada</div>
          </Card>
        ))}
      </div>

      {modalNuevo && (
        <Modal title="Crear ficha de venta" onClose={() => setModalNuevo(false)}>
          <Field label="Inmueble"><Select>{INMUEBLES.map(i => <option key={i.id}>{i.tipo} · {i.barrio} — {i.direccion}</option>)}</Select></Field>
          <div style={{ display: "flex", gap: 10 }}>
            <Field label="Precio de venta" style={{ flex: 1 }}><Input placeholder="$ 480.000.000" /></Field>
            <Field label="% Comisión" style={{ flex: 1 }}><Input placeholder="3" type="number" /></Field>
          </div>
          <Field label="Responsable de venta">
            <Select><option>Asesor interno</option><option>Inmobiliaria (genérico)</option><option>Asesor externo</option></Select>
          </Field>
          <Field label="Documentos obligatorios">
            <div style={{ border: `1px dashed ${COLOR.borde}`, borderRadius: 8, padding: 16, textAlign: "center" }}>
              <Upload size={16} color={COLOR.carbonSuave} style={{ marginBottom: 6 }} />
              <div style={{ fontSize: 12, color: COLOR.carbonSuave }}>Certificado de tradición, cédulas, fotos, contrato PDF</div>
            </div>
          </Field>
          <div style={{ display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 18 }}>
            <Button variant="secondary" onClick={() => setModalNuevo(false)}>Cancelar</Button>
            <Button onClick={() => setModalNuevo(false)}>Guardar ficha</Button>
          </div>
        </Modal>
      )}
    </div>
  );
}

/* ============================================================
   ARREGLOS / REPARACIÓN
   ============================================================ */
function Arreglos() {
  const [modalNuevo, setModalNuevo] = useState(false);
  const estadoColor = {
    "Pendiente": { color: COLOR.azul, bg: COLOR.azulClaro },
    "En progreso": { color: COLOR.mostazaOscuro, bg: COLOR.mostazaClaro },
    "Terminado": { color: COLOR.verde, bg: COLOR.verdeClaro },
  };

  return (
    <div>
      <PageHeader title="Arreglos / Reparación" subtitle="Órdenes de trabajo, costos y evidencias" action={<Button icon={Plus} onClick={() => setModalNuevo(true)}>Nueva orden de trabajo</Button>} />

      {ARREGLOS.map(a => {
        const inm = INMUEBLES.find(i => i.id === a.inmuebleId);
        const e = estadoColor[a.estado];
        return (
          <Card key={a.id} style={{ marginBottom: 14 }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
              <div style={{ display: "flex", gap: 14 }}>
                <div style={{ background: COLOR.mostazaClaro, padding: 10, borderRadius: 9, height: "fit-content" }}>
                  <Wrench size={18} color={COLOR.mostazaOscuro} />
                </div>
                <div>
                  <div style={{ fontSize: 14, fontWeight: 700, color: COLOR.carbon, marginBottom: 3 }}>{a.descripcion}</div>
                  <div style={{ fontSize: 12.5, color: COLOR.carbonSuave }}>{inm.tipo} · {inm.barrio} · {a.fecha} · {a.responsable}</div>
                  <div style={{ display: "flex", gap: 8, marginTop: 10 }}>
                    <Badge color={e.color} bg={e.bg}>{a.estado}</Badge>
                    <Badge color={COLOR.carbon} bg={COLOR.fondo}>Se descuenta de: {a.cargoA}</Badge>
                  </div>
                </div>
              </div>
              <div style={{ textAlign: "right" }}>
                <div style={{ fontSize: 18, fontWeight: 700, fontFamily: "Georgia, serif" }}>{money(a.costoTotal)}</div>
                <div style={{ display: "flex", gap: 6, marginTop: 8, justifyContent: "flex-end" }}>
                  <div style={{ width: 36, height: 36, borderRadius: 6, background: COLOR.fondo, display: "flex", alignItems: "center", justifyContent: "center", border: `1px dashed ${COLOR.borde}` }}>
                    <Camera size={14} color={COLOR.carbonSuave} />
                  </div>
                  <div style={{ width: 36, height: 36, borderRadius: 6, background: COLOR.fondo, display: "flex", alignItems: "center", justifyContent: "center", border: `1px dashed ${COLOR.borde}` }}>
                    <Camera size={14} color={COLOR.carbonSuave} />
                  </div>
                </div>
              </div>
            </div>
          </Card>
        );
      })}

      {modalNuevo && (
        <Modal title="Nueva orden de trabajo" onClose={() => setModalNuevo(false)}>
          <Field label="Inmueble"><Select>{INMUEBLES.map(i => <option key={i.id}>{i.tipo} · {i.barrio}</option>)}</Select></Field>
          <Field label="Descripción"><textarea style={{ ...inputStyle, minHeight: 70, resize: "vertical" }} placeholder="Describe el trabajo a realizar..." /></Field>
          <div style={{ display: "flex", gap: 10 }}>
            <Field label="Fecha" style={{ flex: 1 }}><Input type="date" /></Field>
            <Field label="Responsable" style={{ flex: 1 }}><Input placeholder="Nombre del técnico" /></Field>
          </div>
          <Field label="Ítems de costo">
            <div style={{ display: "flex", gap: 8, marginBottom: 8 }}>
              <Input placeholder="Descripción" style={{ flex: 2 }} />
              <Input placeholder="Valor" style={{ flex: 1 }} />
              <Input placeholder="Cant." style={{ flex: 1 }} />
            </div>
            <Button variant="ghost" icon={Plus} size="sm" style={{ padding: "4px 0" }}>Agregar ítem</Button>
          </Field>
          <Field label="¿El costo se descuenta de...?">
            <div style={{ display: "flex", gap: 10 }}>
              <label style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 13 }}><input type="radio" name="cargo" defaultChecked /> Propietario (liquidación)</label>
              <label style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 13 }}><input type="radio" name="cargo" /> Arrendatario (recibo)</label>
            </div>
          </Field>
          <div style={{ display: "flex", justifyContent: "flex-end", gap: 8, marginTop: 18 }}>
            <Button variant="secondary" onClick={() => setModalNuevo(false)}>Cancelar</Button>
            <Button onClick={() => setModalNuevo(false)}>Guardar orden</Button>
          </div>
        </Modal>
      )}
    </div>
  );
}

/* ============================================================
   REPORTES
   ============================================================ */
function Reportes() {
  const [reporteActivo, setReporteActivo] = useState(0);

  const reportes = [
    { nombre: "Pendientes de pago", cols: ["Arrendatario", "Inmueble", "Días de atraso"], rows: [["Comercializadora El Faro", "Casa · El Ingenio", "3 días"]] },
    { nombre: "Mora / afianzadora", cols: ["Arrendatario", "Inmueble", "Días", "Valor", "Afianzadora"], rows: [["Comercializadora El Faro", "Casa · El Ingenio", "3", money(97680), "AFFI"]] },
    { nombre: "Próximos a vencer", cols: ["Arrendatario", "Inmueble", "Vencimiento"], rows: [["Comercializadora El Faro", "Casa · El Ingenio", "2026-07-15"]] },
    { nombre: "Canon al día", cols: ["Arrendatario", "Inmueble", "Fecha pago"], rows: [["Carlos Mejía", "Apto · Tequendama", "2026-06-03"], ["Diana Rojas", "Local · Granada", "2026-06-08"]] },
    { nombre: "Desocupados / pendientes reparación", cols: ["Inmueble", "Estado", "Días"], rows: [["Apto · Limonar 201", "En arreglo", "9 días"]] },
    { nombre: "Total inmuebles", cols: ["Estado", "Cantidad"], rows: [["Disponible", "2"], ["Arrendado", "6"], ["En venta", "1"], ["En arreglo", "1"]] },
  ];
  const r = reportes[reporteActivo];

  return (
    <div>
      <PageHeader title="Reportes" subtitle="Indicadores operativos exportables en PDF o Excel" />
      <div style={{ display: "flex", gap: 8, marginBottom: 18, flexWrap: "wrap" }}>
        {reportes.map((rep, i) => (
          <div key={i} onClick={() => setReporteActivo(i)} style={{
            padding: "8px 14px", borderRadius: 8, fontSize: 13, fontWeight: 600, cursor: "pointer",
            background: reporteActivo === i ? COLOR.azul : "white", color: reporteActivo === i ? "white" : COLOR.carbon,
            border: `1px solid ${reporteActivo === i ? COLOR.azul : COLOR.borde}`
          }}>{rep.nombre}</div>
        ))}
      </div>

      <Card style={{ padding: 0, overflow: "hidden" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "14px 18px", borderBottom: `1px solid ${COLOR.borde}` }}>
          <h3 style={{ fontSize: 15, fontWeight: 700, margin: 0 }}>{r.nombre}</h3>
          <div style={{ display: "flex", gap: 8 }}>
            <Button variant="secondary" icon={Download} size="sm">PDF</Button>
            <Button variant="secondary" icon={Download} size="sm">Excel</Button>
          </div>
        </div>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13.5 }}>
          <thead>
            <tr style={{ background: COLOR.fondo }}>
              {r.cols.map((c, i) => <th key={i} style={{ textAlign: "left", padding: "10px 18px", fontSize: 12, color: COLOR.carbonSuave, fontWeight: 700, textTransform: "uppercase" }}>{c}</th>)}
            </tr>
          </thead>
          <tbody>
            {r.rows.map((row, i) => (
              <tr key={i} style={{ borderBottom: `1px solid ${COLOR.borde}` }}>
                {row.map((cell, j) => <td key={j} style={{ padding: "12px 18px" }}>{cell}</td>)}
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
    </div>
  );
}

/* ============================================================
   CONFIGURACIÓN
   ============================================================ */
function Configuracion() {
  return (
    <div>
      <PageHeader title="Configuración" subtitle="Parámetros generales del sistema · solo Administrador" />
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        <Card>
          <h3 style={{ fontSize: 14, fontWeight: 700, margin: "0 0 14px" }}>Parámetros financieros</h3>
          <Field label="% Recargo diario por mora"><Input defaultValue="1.76" /></Field>
          <Field label="% Administración por defecto"><Input defaultValue="10" /></Field>
          <Field label="Valor de IPC vigente (%)"><Input defaultValue="6.5" /></Field>
          <Button>Guardar parámetros</Button>
        </Card>
        <Card>
          <h3 style={{ fontSize: 14, fontWeight: 700, margin: "0 0 14px" }}>Afianzadoras</h3>
          {["AFFI", "Fianzas de Colombia"].map((a, i) => (
            <div key={i} style={{ display: "flex", justifyContent: "space-between", padding: "10px 0", borderBottom: `1px solid ${COLOR.borde}` }}>
              <span style={{ fontSize: 13.5 }}>{a}</span>
              <Button variant="ghost" size="sm" icon={Pencil}>Editar</Button>
            </div>
          ))}
          <Button variant="secondary" icon={Plus} size="sm" style={{ marginTop: 10 }}>Agregar afianzadora</Button>
        </Card>
      </div>
    </div>
  );
}

/* ============================================================
   APP PRINCIPAL
   ============================================================ */
export default function App() {
  const [pagina, setPagina] = useState("dashboard");
  const [rol, setRol] = useState("Administrador");

  const paginas = {
    dashboard: <Dashboard onNavigate={setPagina} />,
    propietarios: <Propietarios />,
    inmuebles: <Inmuebles />,
    alquiler: <Alquiler />,
    venta: <Venta />,
    arreglos: <Arreglos />,
    reportes: <Reportes />,
    configuracion: <Configuracion />,
  };

  return (
    <div style={{ fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif", background: COLOR.fondo, minHeight: "100vh" }}>
      <Sidebar active={pagina} onNavigate={setPagina} rol={rol} setRol={setRol} />
      <div style={{ marginLeft: 232, padding: "28px 32px" }}>
        {paginas[pagina] || <Dashboard onNavigate={setPagina} />}
      </div>
    </div>
  );
}
