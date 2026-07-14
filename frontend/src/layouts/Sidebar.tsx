import React, { useState } from 'react';
import {
  Home, Users, Building2, FileSignature, Tag, Wrench, BarChart3, Settings,
  ChevronDown, UserCircle
} from 'lucide-react';
import { COLOR } from '../styles/colors';

// --- LOGOMARK & LOGOFULL ---
function LogoMark({ size = 36 }: { size?: number }) {
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

interface SidebarProps {
  active: string;
  onNavigate: (page: string) => void;
  rol: string;
  setRol: (rol: string) => void;
}

export default function Sidebar({ active, onNavigate, rol, setRol }: SidebarProps) {
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
      
      {/* Dev Simulator is toggleable via import.meta.env */}
      {import.meta.env.VITE_ENABLE_ROLE_SIMULATOR !== 'false' && (
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
      )}
    </div>
  );
}
