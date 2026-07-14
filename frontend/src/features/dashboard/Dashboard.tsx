import React from 'react';
import { Building2, Check, AlertTriangle, Clock, Bell, Users, FileSignature, BarChart3, ChevronRight } from 'lucide-react';
import { COLOR } from '../../styles/colors';
import { Card, PageHeader, Badge } from '../../components/ui';

// Mock values matching legacy
const MOCK_INMUEBLES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
const MOCK_CONTRATOS = [
  { id: 1, diaPago: 3, fechaFin: "2026-07-31" },
  { id: 2, diaPago: 8, fechaFin: "2026-03-14" },
  { id: 3, diaPago: 11, fechaFin: "2026-07-15" },
  { id: 4, diaPago: 1, fechaFin: "2026-10-31" },
];

function estadoMora(diaPago: number) {
  // Hoy = día 8
  const hoy = 8;
  if (hoy <= 5) return { estado: "ok", label: "Sin recargo", color: COLOR.verde, bg: COLOR.verdeClaro };
  if (hoy <= 10) return { estado: "recargo", label: `Recargo día ${hoy}`, color: COLOR.mostazaOscuro, bg: COLOR.mostazaClaro };
  return { estado: "mora", label: "En afianzadora", color: COLOR.rojo, bg: COLOR.rojoClaro };
}

interface DashboardProps {
  onNavigate: (page: string) => void;
}

export default function Dashboard({ onNavigate }: DashboardProps) {
  const totalInmuebles = MOCK_INMUEBLES.length;
  const arrendados = 8; // Simulado
  const enMora = MOCK_CONTRATOS.filter(c => estadoMora(c.diaPago).estado !== "ok").length;
  
  const proximosVencer = MOCK_CONTRATOS.filter(c => {
    const fin = new Date(c.fechaFin);
    const hoy = new Date("2026-06-24");
    const diffTime = fin.getTime() - hoy.getTime();
    const dias = diffTime / (1000 * 60 * 60 * 24);
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
            { tipo: "IPC", texto: "Enero: pendiente actualizar IPC del año en curso", color: COLOR.azul },
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
