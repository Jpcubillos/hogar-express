import { useMemo, useState, type FormEvent } from 'react';
import axios from 'axios';
import {
  AlertCircle,
  ArrowRight,
  Bell,
  Building2,
  CheckCircle2,
  Eye,
  EyeOff,
  KeyRound,
  LockKeyhole,
  Menu,
  ShieldCheck,
  UserRound,
  Users,
} from 'lucide-react';
import Sidebar from '../layouts/Sidebar';
import BrandLogo from '../components/BrandLogo';
import { AppProviders, useAuth } from './providers/AppProviders';
import { Button, Field, Input } from '../components/ui';
import Dashboard from '../features/dashboard/Dashboard';
import Propietarios from '../features/owners/Propietarios';
import Inmuebles from '../features/properties/Inmuebles';
import Alquiler from '../features/rentals/Alquiler';
import Venta from '../features/sales/Venta';
import Arreglos from '../features/repairs/Arreglos';
import Reportes from '../features/reports/Reportes';
import Configuracion from '../features/settings/Configuracion';

const PAGE_META: Record<string, { section: string; title: string }> = {
  dashboard: { section: 'Inicio', title: 'Panel operativo' },
  propietarios: { section: 'Gestión', title: 'Propietarios' },
  inmuebles: { section: 'Gestión', title: 'Inmuebles' },
  alquiler: { section: 'Operación', title: 'Alquiler' },
  venta: { section: 'Comercial', title: 'Venta' },
  arreglos: { section: 'Operación', title: 'Arreglos y reparaciones' },
  reportes: { section: 'Analítica', title: 'Reportes' },
  configuracion: { section: 'Administración', title: 'Configuración' },
};

function LoginScreen() {
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(username, password);
    } catch (requestError: unknown) {
      const apiMessage = axios.isAxiosError(requestError)
        ? requestError.response?.data?.message || requestError.response?.data?.detail
        : null;
      setError(apiMessage || 'No fue posible iniciar sesión. Verifica tu usuario y contraseña.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="login-page">
      <section className="login-brand-panel" aria-label="Hogar Express">
        <BrandLogo className="login-brand-logo" />
        <div className="login-hero">
          <span className="login-kicker"><ShieldCheck size={15} /> Plataforma interna segura</span>
          <h1>La operación inmobiliaria, clara y bajo control.</h1>
          <p>
            Centraliza propietarios, inmuebles, contratos y novedades en un espacio diseñado
            para que tu equipo trabaje con confianza.
          </p>
          <div className="login-benefits">
            <span className="login-benefit"><Users size={15} /> Propietarios</span>
            <span className="login-benefit"><Building2 size={15} /> Inmuebles</span>
            <span className="login-benefit"><CheckCircle2 size={15} /> Seguimiento operativo</span>
          </div>
        </div>
        <div className="login-brand-footer">Hogar Express · Hecho a tu medida</div>
      </section>

      <section className="login-form-panel">
        <div className="login-form-wrap">
          <BrandLogo className="login-mobile-logo" />
          <header className="login-form-header">
            <div className="login-form-header__icon"><KeyRound size={22} /></div>
            <h2>Bienvenido de nuevo</h2>
            <p>Ingresa con las credenciales asignadas por el administrador.</p>
          </header>

          {error && (
            <div className="login-error" role="alert">
              <AlertCircle size={17} />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <Field label="Usuario">
              <div className="login-field">
                <UserRound size={17} />
                <Input
                  value={username}
                  onChange={(event) => setUsername(event.target.value)}
                  placeholder="Ingresa tu usuario"
                  autoComplete="username"
                  required
                  autoFocus
                />
              </div>
            </Field>
            <Field label="Contraseña">
              <div className="login-field">
                <LockKeyhole size={17} />
                <Input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  placeholder="Ingresa tu contraseña"
                  autoComplete="current-password"
                  required
                  style={{ paddingRight: 44 }}
                />
                <button
                  type="button"
                  className="password-toggle"
                  onClick={() => setShowPassword((visible) => !visible)}
                  aria-label={showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'}
                >
                  {showPassword ? <EyeOff size={17} /> : <Eye size={17} />}
                </button>
              </div>
            </Field>
            <Button type="submit" className="login-submit" disabled={loading}>
              {loading ? 'Validando acceso…' : 'Ingresar al sistema'}
              {!loading && <ArrowRight size={17} />}
            </Button>
          </form>

          <div className="login-security"><ShieldCheck size={14} /> Conexión protegida y acceso auditado</div>
        </div>
      </section>
    </main>
  );
}

function AppContent() {
  const { isAuthenticated, isLoading, user } = useAuth();
  const [page, setPage] = useState('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const formattedDate = useMemo(() => new Intl.DateTimeFormat('es-CO', {
    weekday: 'long', day: 'numeric', month: 'long', year: 'numeric',
  }).format(new Date()), []);

  if (isLoading) {
    return (
      <div className="app-loading">
        <div className="app-loading__content">
          <BrandLogo className="app-loading__logo" />
          <div className="app-loading__spinner" aria-hidden="true" />
          <h3>Cargando Hogar Express...</h3>
          <p>Estamos preparando tu espacio de trabajo.</p>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) return <LoginScreen />;

  const pages: Record<string, React.ReactNode> = {
    dashboard: <Dashboard onNavigate={setPage} />,
    propietarios: <Propietarios />,
    inmuebles: <Inmuebles />,
    alquiler: <Alquiler />,
    venta: <Venta />,
    arreglos: <Arreglos />,
    reportes: <Reportes />,
    configuracion: <Configuracion />,
  };

  const meta = PAGE_META[page] || PAGE_META.dashboard;
  const displayName = user?.display_name || user?.username || 'Usuario';
  const userInitials = displayName.split(' ').filter(Boolean).slice(0, 2).map((part) => part[0]).join('').toUpperCase();

  return (
    <div className="app-shell">
      <Sidebar active={page} onNavigate={setPage} isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="app-main">
        <header className="app-topbar">
          <div className="app-topbar__left">
            <button type="button" className="icon-button mobile-menu-button" onClick={() => setSidebarOpen(true)} aria-label="Abrir menú">
              <Menu size={19} />
            </button>
            <div className="app-topbar__context">
              <span>{meta.section}</span>
              <strong>{meta.title}</strong>
            </div>
          </div>
          <div className="app-topbar__right">
            <span className="topbar-date">{formattedDate}</span>
            <button type="button" className="icon-button" aria-label="Notificaciones"><Bell size={18} /></button>
            <div className="topbar-user" title={displayName}>{userInitials || 'HE'}</div>
          </div>
        </header>
        <main key={page} className="app-content">
          {pages[page] || <Dashboard onNavigate={setPage} />}
        </main>
      </div>
    </div>
  );
}

export default function App() {
  return <AppProviders><AppContent /></AppProviders>;
}
