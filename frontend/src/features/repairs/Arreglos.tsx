import React, { useState, useEffect } from 'react';
import {
  Plus,
  Search,
  Wrench,
  AlertTriangle,
  Clock,
  CheckCircle2,
  FileText,
  User,
  Building2,
  DollarSign,
  ChevronRight,
  ChevronLeft,
  Calendar,
  MessageSquare,
  ShieldCheck,
  Upload,
  ArrowRight,
  Filter,
  Check,
  X,
  AlertCircle,
  Download,
  Percent,
  TrendingUp,
  Paperclip,
  RefreshCw
} from 'lucide-react';
import { COLOR } from '../../styles/colors';
import { Card, PageHeader, Button, SearchBar, Badge, Modal, Field, Input, Select } from '../../components/ui';
import api from '../../services/api';

const money = (n: number) => '$' + Math.round(n || 0).toLocaleString('es-CO');

export default function Arreglos() {
  const [reparaciones, setReparaciones] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [kpis, setKpis] = useState({
    active: 0,
    critical: 0,
    pending_approval: 0,
    scheduled: 0,
    overdue: 0,
    sla_compliance_rate: 100.0,
    total_quoted_cost: 0,
    total_actual_cost: 0,
    avg_repair_cost: 0
  });

  // Catalog state from backend API
  const [propertiesList, setPropertiesList] = useState<any[]>([]);
  const [categoriesList, setCategoriesList] = useState<any[]>([]);
  const [providersList, setProvidersList] = useState<any[]>([]);

  // Search and Filter states
  const [busqueda, setBusqueda] = useState("");
  const [filtroEstado, setFiltroEstado] = useState("TODOS");
  const [filtroPrioridad, setFiltroPrioridad] = useState("TODOS");
  const [filtroTipo, setFiltroTipo] = useState("TODOS");

  // Selection and Modal controls
  const [seleccionada, setSeleccionada] = useState<any | null>(null);
  const [tabDetalle, setTabDetalle] = useState<string>("resumen");
  const [modalNuevo, setModalNuevo] = useState(false);
  const [pasoWizard, setPasoWizard] = useState(1);
  const [nuevoComentario, setNuevoComentario] = useState("");

  // New repair form draft
  const [draft, setDraft] = useState({
    title: "",
    description: "",
    property_id: "",
    category_id: "",
    priority: "MEDIUM",
    severity: "MEDIUM",
    repair_type: "CORRECTIVE",
    provider_id: "",
    estimated_cost: "350000",
    responsible_financial: "OWNER",
    installments: "1"
  });

  // Fetch real data from Django REST API
  const cargarDatos = async () => {
    setLoading(true);
    try {
      const [resOrders, resSummary, resProps, resCats, resProv] = await Promise.all([
        api.get('/repairs/orders/'),
        api.get('/repairs/orders/dashboard-summary/'),
        api.get('/properties/properties/'),
        api.get('/catalogs/repair-categories/'),
        api.get('/people/provider-profiles/'),
      ]);

      const rawOrders = Array.isArray(resOrders.data) ? resOrders.data : (resOrders.data.results || []);
      setReparaciones(rawOrders);
      setKpis(resSummary.data);

      const props = Array.isArray(resProps.data) ? resProps.data : (resProps.data.results || []);
      const cats = Array.isArray(resCats.data) ? resCats.data : (resCats.data.results || []);
      const provs = Array.isArray(resProv.data) ? resProv.data : (resProv.data.results || []);

      setPropertiesList(props);
      setCategoriesList(cats);
      setProvidersList(provs);

      if (props.length > 0) {
        setDraft(prev => ({
          ...prev,
          property_id: props[0].id,
          category_id: cats[0]?.id || "",
          provider_id: provs[0]?.id || ""
        }));
      }
    } catch (err) {
      console.error("Error al cargar datos del backend:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarDatos();
  }, []);

  // Filtered dataset calculation
  const filtradas = reparaciones.filter(r => {
    const titleMatch = (r.title || "").toLowerCase().includes(busqueda.toLowerCase());
    const orderNumMatch = (r.order_number || "").toLowerCase().includes(busqueda.toLowerCase());
    const propertyMatch = (r.property_address || "").toLowerCase().includes(busqueda.toLowerCase());
    const providerMatch = (r.current_provider_name || "").toLowerCase().includes(busqueda.toLowerCase());

    const matchBusqueda = titleMatch || orderNumMatch || propertyMatch || providerMatch;
    const matchEstado = filtroEstado === "TODOS" || r.status === filtroEstado;
    const matchPrioridad = filtroPrioridad === "TODOS" || r.priority === filtroPrioridad;
    const matchTipo = filtroTipo === "TODOS" || r.repair_type === filtroTipo;

    return matchBusqueda && matchEstado && matchPrioridad && matchTipo;
  });

  const getPriorityBadge = (p: string) => {
    const map: Record<string, { label: string, color: string, bg: string }> = {
      CRITICAL: { label: "Crítica", color: COLOR.rojo, bg: COLOR.rojoClaro },
      HIGH: { label: "Alta", color: COLOR.mostazaOscuro, bg: COLOR.mostazaClaro },
      MEDIUM: { label: "Media", color: COLOR.azul, bg: COLOR.azulClaro },
      LOW: { label: "Baja", color: COLOR.carbonSuave, bg: COLOR.fondo },
    };
    const b = map[p] || map.MEDIUM;
    return <Badge color={b.color} bg={b.bg}>{b.label}</Badge>;
  };

  const getStatusBadge = (s: string, label: string) => {
    const map: Record<string, { color: string, bg: string }> = {
      REPORTED: { color: COLOR.carbonSuave, bg: COLOR.fondo },
      IN_REVIEW: { color: COLOR.azul, bg: COLOR.azulClaro },
      PENDING_QUOTE: { color: COLOR.mostazaOscuro, bg: COLOR.mostazaClaro },
      PENDING_APPROVAL: { color: COLOR.rojo, bg: COLOR.rojoClaro },
      APPROVED: { color: COLOR.verde, bg: COLOR.verdeClaro },
      SCHEDULED: { color: COLOR.azul, bg: COLOR.azulClaro },
      IN_PROGRESS: { color: COLOR.mostazaOscuro, bg: COLOR.mostazaClaro },
      COMPLETED: { color: COLOR.verde, bg: COLOR.verdeClaro },
      CLOSED: { color: COLOR.carbon, bg: COLOR.borde },
      CANCELLED: { color: COLOR.rojo, bg: COLOR.rojoClaro },
    };
    const b = map[s] || { color: COLOR.carbon, bg: COLOR.fondo };
    return <Badge color={b.color} bg={b.bg}>{label || s}</Badge>;
  };

  const handleCrearOrden = async () => {
    try {
      const payload = {
        order_number: `OT-2026-${Math.floor(1000 + Math.random() * 9000)}`,
        title: draft.title || "Reparación General",
        description: draft.description || "Sin descripción especificada",
        property: draft.property_id || propertiesList[0]?.id,
        category: draft.category_id || categoriesList[0]?.id,
        priority: draft.priority,
        severity: draft.severity,
        repair_type: draft.repair_type,
        current_provider: draft.provider_id || null,
        status: "REPORTED",
      };

      await api.post('/repairs/orders/', payload);
      setModalNuevo(false);
      setPasoWizard(1);
      cargarDatos();
    } catch (err: any) {
      alert("No se pudo crear la orden: " + (err.response?.data?.error || err.message));
    }
  };

  const handleAddComment = async () => {
    if (!nuevoComentario.trim() || !seleccionada) return;
    try {
      await api.post('/repairs/comments/', {
        repair: seleccionada.id,
        text: nuevoComentario,
        is_internal: true
      });
      setNuevoComentario("");
      // Reload order detail
      const res = await api.get(`/repairs/orders/${seleccionada.id}/`);
      setSeleccionada(res.data);
    } catch (err: any) {
      alert("Error al guardar comentario: " + (err.response?.data?.error || err.message));
    }
  };

  const handleCambiarEstado = async (nuevoEstado: string) => {
    if (!seleccionada) return;
    try {
      const res = await api.post(`/repairs/orders/${seleccionada.id}/change-status/`, {
        status: nuevoEstado,
        reason: "Cambio de estado desde la interfaz de usuario."
      });
      setSeleccionada(res.data);
      cargarDatos();
    } catch (err: any) {
      alert("Error al cambiar estado: " + (err.response?.data?.error || err.message));
    }
  };

  return (
    <div>
      <PageHeader
        eyebrow="Módulo Interno de Mantenimiento"
        title="Gestión de Reparaciones"
        subtitle="Órdenes de trabajo, cotizaciones, desgloses de costos y trazabilidad estilo GitHub"
        action={
          <div style={{ display: "flex", gap: 10 }}>
            <Button variant="secondary" icon={RefreshCw} onClick={cargarDatos}>Refrescar</Button>
            <Button icon={Plus} onClick={() => setModalNuevo(true)}>Crear Orden de Trabajo</Button>
          </div>
        }
      />

      {/* KPI Header Dashboard */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: 12, marginBottom: 24 }}>
        <Card style={{ padding: 16, borderLeft: `4px solid ${COLOR.azul}` }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
            <span style={{ fontSize: 12.5, color: COLOR.carbonSuave, fontWeight: 600 }}>Órdenes Activas</span>
            <Wrench size={18} color={COLOR.azul} />
          </div>
          <div style={{ fontSize: 24, fontWeight: 700, color: COLOR.carbon }}>{kpis.active}</div>
          <div style={{ fontSize: 11.5, color: COLOR.carbonSuave, marginTop: 4 }}>En gestión u homologación</div>
        </Card>

        <Card style={{ padding: 16, borderLeft: `4px solid ${COLOR.rojo}` }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
            <span style={{ fontSize: 12.5, color: COLOR.carbonSuave, fontWeight: 600 }}>Prioridad Crítica</span>
            <AlertTriangle size={18} color={COLOR.rojo} />
          </div>
          <div style={{ fontSize: 24, fontWeight: 700, color: COLOR.rojo }}>{kpis.critical}</div>
          <div style={{ fontSize: 11.5, color: COLOR.rojo, marginTop: 4, fontWeight: 600 }}>Atención en 24h máx</div>
        </Card>

        <Card style={{ padding: 16, borderLeft: `4px solid ${COLOR.mostazaOscuro}` }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
            <span style={{ fontSize: 12.5, color: COLOR.carbonSuave, fontWeight: 600 }}>Pendientes Aprobación</span>
            <ShieldCheck size={18} color={COLOR.mostazaOscuro} />
          </div>
          <div style={{ fontSize: 24, fontWeight: 700, color: COLOR.carbon }}>{kpis.pending_approval}</div>
          <div style={{ fontSize: 11.5, color: COLOR.mostazaOscuro, marginTop: 4 }}>En espera de visto bueno</div>
        </Card>

        <Card style={{ padding: 16, borderLeft: `4px solid ${COLOR.verde}` }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
            <span style={{ fontSize: 12.5, color: COLOR.carbonSuave, fontWeight: 600 }}>Cumplimiento SLA</span>
            <Percent size={18} color={COLOR.verde} />
          </div>
          <div style={{ fontSize: 24, fontWeight: 700, color: COLOR.verde }}>{kpis.sla_compliance_rate}%</div>
          <div style={{ fontSize: 11.5, color: COLOR.verde, marginTop: 4 }}>Dentro del límite SLA</div>
        </Card>

        <Card style={{ padding: 16, borderLeft: `4px solid ${COLOR.carbon}` }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 6 }}>
            <span style={{ fontSize: 12.5, color: COLOR.carbonSuave, fontWeight: 600 }}>Presupuesto Total</span>
            <TrendingUp size={18} color={COLOR.carbon} />
          </div>
          <div style={{ fontSize: 20, fontWeight: 700, color: COLOR.carbon }}>{money(kpis.total_quoted_cost)}</div>
          <div style={{ fontSize: 11.5, color: COLOR.carbonSuave, marginTop: 4 }}>Ejecutado: {money(kpis.total_actual_cost)}</div>
        </Card>
      </div>

      {/* Filters and Search Bar */}
      <div style={{ display: "flex", flexDirection: "column", gap: 12, marginBottom: 20 }}>
        <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
          <SearchBar
            placeholder="Buscar por N° Orden, título, inmueble o proveedor..."
            value={busqueda}
            onChange={setBusqueda}
            className="search-bar-flexible"
          />
          
          <Select
            value={filtroPrioridad}
            onChange={(e) => setFiltroPrioridad(e.target.value)}
            style={{ width: 170 }}
          >
            <option value="TODOS">Todas las Prioridades</option>
            <option value="CRITICAL">Crítica</option>
            <option value="HIGH">Alta</option>
            <option value="MEDIUM">Media</option>
            <option value="LOW">Baja</option>
          </Select>

          <Select
            value={filtroTipo}
            onChange={(e) => setFiltroTipo(e.target.value)}
            style={{ width: 190 }}
          >
            <option value="TODOS">Todos los Tipos</option>
            <option value="CORRECTIVE">Correctiva</option>
            <option value="PREVENTIVE">Preventivo</option>
            <option value="PERIODIC_MAINTENANCE">Periódico / Inspección</option>
          </Select>
        </div>

        {/* State Tabs Pill Filters */}
        <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
          {[
            { id: "TODOS", label: "Todas" },
            { id: "REPORTED", label: "Reportadas" },
            { id: "IN_REVIEW", label: "En Revisión" },
            { id: "PENDING_QUOTE", label: "Pend. Cotización" },
            { id: "PENDING_APPROVAL", label: "Pend. Aprobación" },
            { id: "APPROVED", label: "Aprobadas" },
            { id: "SCHEDULED", label: "Programadas" },
            { id: "IN_PROGRESS", label: "En Progreso" },
            { id: "COMPLETED", label: "Terminadas" },
            { id: "CLOSED", label: "Cerradas" },
          ].map(st => (
            <button
              key={st.id}
              onClick={() => setFiltroEstado(st.id)}
              style={{
                padding: "6px 13px",
                borderRadius: 8,
                fontSize: 12.5,
                fontWeight: 600,
                cursor: "pointer",
                border: "none",
                background: filtroEstado === st.id ? COLOR.azul : COLOR.fondo,
                color: filtroEstado === st.id ? "white" : COLOR.carbon,
                transition: "all 0.15s ease"
              }}
            >
              {st.label}
            </button>
          ))}
        </div>
      </div>

      {/* Main Repair Orders Table */}
      <Card style={{ padding: 0, overflow: "hidden" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", fontSize: 13.5 }}>
          <thead>
            <tr style={{ background: COLOR.fondo, borderBottom: `1px solid ${COLOR.borde}` }}>
              {["Orden / Inmueble", "Prioridad", "Estado", "Responsable / Proveedor", "Reloj SLA", ""].map((h, i) => (
                <th key={i} style={{ textAlign: "left", padding: "12px 16px", fontSize: 12, color: COLOR.carbonSuave, fontWeight: 700, textTransform: "uppercase", letterSpacing: "0.4px" }}>
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={6} style={{ textAlign: "center", padding: 36, color: COLOR.carbonSuave }}>
                  Cargando órdenes de reparación desde PostgreSQL...
                </td>
              </tr>
            ) : filtradas.length === 0 ? (
              <tr>
                <td colSpan={6} style={{ textAlign: "center", padding: 36, color: COLOR.carbonSuave }}>
                  No se encontraron órdenes de trabajo registradas.
                </td>
              </tr>
            ) : (
              filtradas.map(r => (
                <tr
                  key={r.id}
                  onClick={() => setSeleccionada(r)}
                  style={{ borderBottom: `1px solid ${COLOR.borde}`, cursor: "pointer" }}
                  onMouseEnter={(e) => e.currentTarget.style.background = COLOR.fondo}
                  onMouseLeave={(e) => e.currentTarget.style.background = "white"}
                >
                  <td style={{ padding: "14px 16px" }}>
                    <div style={{ fontSize: 12, fontWeight: 700, color: COLOR.azul, marginBottom: 2 }}>{r.order_number} · {r.category_name || "General"}</div>
                    <div style={{ fontSize: 14, fontWeight: 700, color: COLOR.carbon }}>{r.title}</div>
                    <div style={{ fontSize: 12.5, color: COLOR.carbonSuave }}>{r.property_address || "Inmueble Registrado"}</div>
                  </td>
                  <td style={{ padding: "14px 16px" }}>{getPriorityBadge(r.priority)}</td>
                  <td style={{ padding: "14px 16px" }}>{getStatusBadge(r.status, r.status)}</td>
                  <td style={{ padding: "14px 16px" }}>
                    <div style={{ fontSize: 13, fontWeight: 600, color: COLOR.carbon }}>{r.internal_responsible_name || "Sin Asignar"}</div>
                  </td>
                  <td style={{ padding: "14px 16px" }}>
                    <div style={{ display: "flex", alignItems: "center", gap: 5, fontSize: 12.5, color: r.is_overdue ? COLOR.rojo : COLOR.verde, fontWeight: 600 }}>
                      <Clock size={14} />
                      <span>{r.is_overdue ? "SLA Vencido" : "SLA A tiempo"}</span>
                    </div>
                  </td>
                  <td style={{ padding: "14px 16px", textAlign: "right" }}>
                    <ChevronRight size={18} color={COLOR.carbonSuave} />
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </Card>

      {/* MODAL / WIZARD DE CREACIÓN PASO A PASO */}
      {modalNuevo && (
        <Modal
          title={`Nueva Orden de Trabajo - Paso ${pasoWizard} de 5`}
          subtitle="Formulario guiado para el registro de órdenes de reparación"
          onClose={() => setModalNuevo(false)}
          width={640}
        >
          {pasoWizard === 1 && (
            <div>
              <Field label="Inmueble Afectado">
                <Select value={draft.property_id} onChange={(e) => setDraft({ ...draft, property_id: e.target.value })}>
                  {propertiesList.map(p => (
                    <option key={p.id} value={p.id}>{p.address_line} ({p.internal_code})</option>
                  ))}
                </Select>
              </Field>
              <Field label="Título descriptivo del problema">
                <Input
                  placeholder="Ej: Filtración de agua en tubería del baño"
                  value={draft.title}
                  onChange={(e) => setDraft({ ...draft, title: e.target.value })}
                />
              </Field>
              <Field label="Descripción detallada de la novedad">
                <Input
                  placeholder="Escriba aquí los detalles reportados por el inquilino o inspector..."
                  value={draft.description}
                  onChange={(e) => setDraft({ ...draft, description: e.target.value })}
                />
              </Field>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
                <Field label="Categoría de Mantenimiento">
                  <Select value={draft.category_id} onChange={(e) => setDraft({ ...draft, category_id: e.target.value })}>
                    {categoriesList.map(c => (
                      <option key={c.id} value={c.id}>{c.name}</option>
                    ))}
                  </Select>
                </Field>
                <Field label="Tipo de Orden">
                  <Select value={draft.repair_type} onChange={(e) => setDraft({ ...draft, repair_type: e.target.value })}>
                    <option value="CORRECTIVE">Reparación Correctiva</option>
                    <option value="PREVENTIVE">Mantenimiento Preventivo</option>
                    <option value="PERIODIC_MAINTENANCE">Inspección / Periódico</option>
                  </Select>
                </Field>
              </div>
            </div>
          )}

          {pasoWizard === 2 && (
            <div>
              <h4 style={{ fontSize: 14, fontWeight: 700, color: COLOR.carbon, marginBottom: 12 }}>Clasificación de Impacto y SLA</h4>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
                <Field label="Prioridad Operativa">
                  <Select value={draft.priority} onChange={(e) => setDraft({ ...draft, priority: e.target.value })}>
                    <option value="CRITICAL">Crítica (Atención en 24h)</option>
                    <option value="HIGH">Alta (Atención en 48h)</option>
                    <option value="MEDIUM">Media (Atención en 5 días)</option>
                    <option value="LOW">Baja (Atención en 10 días)</option>
                  </Select>
                </Field>
                <Field label="Severidad Estructural">
                  <Select value={draft.severity} onChange={(e) => setDraft({ ...draft, severity: e.target.value })}>
                    <option value="CRITICAL">Crítica (Riesgo habitabilidad)</option>
                    <option value="HIGH">Alta (Humedad/Daño activo)</option>
                    <option value="MEDIUM">Media (Deterioro funcional)</option>
                    <option value="LOW">Baja (Estética/Cosmética)</option>
                  </Select>
                </Field>
              </div>
              <div style={{ background: COLOR.azulClaro, borderRadius: 8, padding: 14, marginTop: 12, fontSize: 13, color: COLOR.azul, display: "flex", gap: 10, alignItems: "center" }}>
                <Clock size={20} />
                <span>Basado en la prioridad seleccionada, el <b>Límite de SLA</b> se calculará automáticamente en el sistema.</span>
              </div>
            </div>
          )}

          {pasoWizard === 3 && (
            <div>
              <h4 style={{ fontSize: 14, fontWeight: 700, color: COLOR.carbon, marginBottom: 12 }}>Proveedor y Estimación de Costos</h4>
              <Field label="Proveedor o Maestro Asignado">
                <Select value={draft.provider_id} onChange={(e) => setDraft({ ...draft, provider_id: e.target.value })}>
                  {providersList.map(p => (
                    <option key={p.id} value={p.id}>{p.provider_kind} - {p.id}</option>
                  ))}
                </Select>
              </Field>
              <Field label="Costo Estimado Inicial (COP)">
                <Input
                  type="number"
                  placeholder="350000"
                  value={draft.estimated_cost}
                  onChange={(e) => setDraft({ ...draft, estimated_cost: e.target.value })}
                />
              </Field>
            </div>
          )}

          {pasoWizard === 4 && (
            <div>
              <h4 style={{ fontSize: 14, fontWeight: 700, color: COLOR.carbon, marginBottom: 12 }}>Distribución Financiera del Costo</h4>
              <Field label="Responsable Financiero del Pago">
                <Select value={draft.responsible_financial} onChange={(e) => setDraft({ ...draft, responsible_financial: e.target.value })}>
                  <option value="OWNER">Propietario (Descuento en Liquidación de Canon)</option>
                  <option value="TENANT">Arrendatario (Cargo en Recibo de Arriendo)</option>
                  <option value="SHARED">Compartido (50% Propietario / 50% Arrendatario)</option>
                </Select>
              </Field>
              <Field label="Número de Cuotas de Descuento">
                <Select value={draft.installments} onChange={(e) => setDraft({ ...draft, installments: e.target.value })}>
                  <option value="1">1 Cuota (Pago Único)</option>
                  <option value="2">2 Cuotas Mensuales</option>
                  <option value="3">3 Cuotas Mensuales</option>
                </Select>
              </Field>
            </div>
          )}

          {pasoWizard === 5 && (
            <div>
              <h4 style={{ fontSize: 14, fontWeight: 700, color: COLOR.carbon, marginBottom: 12 }}>Confirmación y Guardado en PostgreSQL</h4>
              <div style={{ background: COLOR.fondo, padding: 16, borderRadius: 8, fontSize: 13, color: COLOR.carbon }}>
                <div><b>Título:</b> {draft.title || "Reparación General"}</div>
                <div><b>Prioridad:</b> {draft.priority}</div>
                <div><b>Costo Estimado:</b> {money(parseInt(draft.estimated_cost) || 0)}</div>
              </div>
            </div>
          )}

          <div style={{ display: "flex", justifyContent: "space-between", marginTop: 24, paddingTop: 16, borderTop: `1px solid ${COLOR.borde}` }}>
            {pasoWizard > 1 ? (
              <Button variant="secondary" icon={ChevronLeft} onClick={() => setPasoWizard(pasoWizard - 1)}>Anterior</Button>
            ) : <div />}

            {pasoWizard < 5 ? (
              <Button icon={ChevronRight} onClick={() => setPasoWizard(pasoWizard + 1)}>Siguiente Paso</Button>
            ) : (
              <Button icon={CheckCircle2} onClick={handleCrearOrden}>Guardar y Registrar Orden</Button>
            )}
          </div>
        </Modal>
      )}

      {/* DRAWER / MODAL DE DETALLE DE LA REPARACIÓN */}
      {seleccionada && (
        <Modal
          title={`${seleccionada.order_number} — ${seleccionada.title}`}
          subtitle={`Inmueble: ${seleccionada.property_address || 'Inmueble Registrado'}`}
          onClose={() => setSeleccionada(null)}
          width={780}
        >
          {/* Navigation Tabs */}
          <div style={{ display: "flex", gap: 4, borderBottom: `1px solid ${COLOR.borde}`, marginBottom: 20 }}>
            {[
              { id: "resumen", label: "Resumen" },
              { id: "tareas", label: `Tareas (${(seleccionada.tasks || []).length})` },
              { id: "cotizaciones", label: `Cotizaciones (${(seleccionada.quotes || []).length})` },
              { id: "timeline", label: `Timeline (${(seleccionada.timeline_events || []).length})` },
              { id: "comentarios", label: `Comentarios (${(seleccionada.comments || []).length})` },
            ].map(t => (
              <button
                key={t.id}
                onClick={() => setTabDetalle(t.id)}
                style={{
                  padding: "8px 14px",
                  fontSize: 13,
                  fontWeight: 600,
                  cursor: "pointer",
                  border: "none",
                  background: "transparent",
                  color: tabDetalle === t.id ? COLOR.azul : COLOR.carbonSuave,
                  borderBottom: tabDetalle === t.id ? `2px solid ${COLOR.azul}` : "2px solid transparent"
                }}
              >
                {t.label}
              </button>
            ))}
          </div>

          {/* TAB 1: RESUMEN */}
          {tabDetalle === "resumen" && (
            <div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 16 }}>
                <div style={{ background: COLOR.fondo, padding: 16, borderRadius: 8 }}>
                  <h4 style={{ fontSize: 13, fontWeight: 700, color: COLOR.carbon, margin: "0 0 10px" }}>Ficha General</h4>
                  <div style={{ fontSize: 13, display: "flex", flexDirection: "column", gap: 8 }}>
                    <div><b>Categoría:</b> {seleccionada.category_name || "General"}</div>
                    <div><b>Prioridad:</b> {getPriorityBadge(seleccionada.priority)}</div>
                    <div><b>Estado Actual:</b> {getStatusBadge(seleccionada.status, seleccionada.status)}</div>
                    <div><b>Responsable:</b> {seleccionada.internal_responsible_name || "Sin Asignar"}</div>
                  </div>
                </div>

                <div style={{ background: COLOR.fondo, padding: 16, borderRadius: 8 }}>
                  <h4 style={{ fontSize: 13, fontWeight: 700, color: COLOR.carbon, margin: "0 0 10px" }}>Acciones Rápidas de Estado</h4>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                    {seleccionada.status === "REPORTED" && (
                      <Button size="sm" onClick={() => handleCambiarEstado("IN_REVIEW")}>Pasar a En Revisión</Button>
                    )}
                    {seleccionada.status === "IN_REVIEW" && (
                      <Button size="sm" onClick={() => handleCambiarEstado("PENDING_APPROVAL")}>Pasar a Pendiente Aprobación</Button>
                    )}
                    {seleccionada.status === "PENDING_APPROVAL" && (
                      <Button size="sm" onClick={() => handleCambiarEstado("APPROVED")}>Aprobar Orden</Button>
                    )}
                    {seleccionada.status === "APPROVED" && (
                      <Button size="sm" onClick={() => handleCambiarEstado("SCHEDULED")}>Programar Cita</Button>
                    )}
                    {seleccionada.status === "SCHEDULED" && (
                      <Button size="sm" onClick={() => handleCambiarEstado("IN_PROGRESS")}>Iniciar Trabajos</Button>
                    )}
                    {seleccionada.status === "IN_PROGRESS" && (
                      <Button size="sm" onClick={() => handleCambiarEstado("COMPLETED")}>Marcar como Terminada</Button>
                    )}
                    {seleccionada.status === "COMPLETED" && (
                      <Button size="sm" onClick={() => handleCambiarEstado("CLOSED")}>Cerrar y Verificar</Button>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: TAREAS */}
          {tabDetalle === "tareas" && (
            <div>
              <h4 style={{ fontSize: 14, fontWeight: 700, color: COLOR.carbon, marginBottom: 12 }}>Sub-actividades Registradas</h4>
              {(seleccionada.tasks || []).map((task: any) => (
                <div key={task.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: 12, background: COLOR.fondo, borderRadius: 8, marginBottom: 8 }}>
                  <div>
                    <div style={{ fontSize: 13.5, fontWeight: 600, color: COLOR.carbon }}>#{task.sequence_order} · {task.title}</div>
                  </div>
                  <Badge color={task.status === 'COMPLETED' ? COLOR.verde : COLOR.azul} bg={task.status === 'COMPLETED' ? COLOR.verdeClaro : COLOR.azulClaro}>
                    {task.status}
                  </Badge>
                </div>
              ))}
            </div>
          )}

          {/* TAB 3: TIMELINE */}
          {tabDetalle === "timeline" && (
            <div>
              <h4 style={{ fontSize: 14, fontWeight: 700, color: COLOR.carbon, marginBottom: 16 }}>Event Stream Cronológico de PostgreSQL</h4>
              <div style={{ position: "relative", paddingLeft: 24, borderLeft: `2px solid ${COLOR.borde}` }}>
                {(seleccionada.timeline_events || []).map((event: any, idx: number) => (
                  <div key={event.id || idx} style={{ marginBottom: 20, position: "relative" }}>
                    <div style={{
                      position: "absolute", left: -31, top: 0, width: 14, height: 14, borderRadius: "50%",
                      background: COLOR.azul, border: "2px solid white"
                    }} />
                    <div style={{ fontSize: 13.5, fontWeight: 700, color: COLOR.carbon }}>{event.title}</div>
                    <div style={{ fontSize: 12.5, color: COLOR.carbonSuave, margin: "2px 0 4px" }}>{event.description}</div>
                    <div style={{ fontSize: 11.5, color: COLOR.carbonSuave }}>Por: {event.performed_by_name || 'Sistema'} · {new Date(event.occurred_at).toLocaleString('es-CO')}</div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 4: COMENTARIOS */}
          {tabDetalle === "comentarios" && (
            <div>
              <div style={{ marginBottom: 16 }}>
                <Field label="Agregar Observación o Nota Interna">
                  <Input
                    placeholder="Escriba una observación..."
                    value={nuevoComentario}
                    onChange={(e) => setNuevoComentario(e.target.value)}
                  />
                </Field>
                <Button size="sm" icon={MessageSquare} onClick={handleAddComment} style={{ marginTop: 8 }}>Publicar Comentario</Button>
              </div>

              <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
                {(seleccionada.comments || []).map((c: any) => (
                  <div key={c.id} style={{ background: COLOR.fondo, padding: 12, borderRadius: 8, fontSize: 13 }}>
                    <div style={{ display: "flex", justifyContent: "space-between", fontWeight: 600, color: COLOR.carbon, marginBottom: 4 }}>
                      <span>{c.user_name || 'Usuario'}</span>
                    </div>
                    <div style={{ color: COLOR.carbon }}>{c.text}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </Modal>
      )}
    </div>
  );
}
