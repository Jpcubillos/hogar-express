import {
  BarChart3,
  BriefcaseBusiness,
  Building2,
  FileSignature,
  Home,
  LogOut,
  Settings,
  Tag,
  Users,
  Wrench,
  X,
} from 'lucide-react';
import BrandLogo from '../components/BrandLogo';
import { useAuth } from '../app/providers/AppProviders';

const NAV_ITEMS = [
  { id: 'dashboard', label: 'Dashboard', icon: Home },
  { id: 'propietarios', label: 'Propietarios', icon: Users },
  { id: 'inmuebles', label: 'Inmuebles', icon: Building2 },
  { id: 'alquiler', label: 'Alquiler', icon: FileSignature },
  { id: 'venta', label: 'Venta', icon: Tag },
  { id: 'arreglos', label: 'Arreglos', icon: Wrench },
  { id: 'reportes', label: 'Reportes', icon: BarChart3 },
  { id: 'configuracion', label: 'Configuración', icon: Settings },
];

interface SidebarProps {
  active: string;
  onNavigate: (page: string) => void;
  isOpen: boolean;
  onClose: () => void;
}

function initials(value: string) {
  return value
    .split(' ')
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase())
    .join('') || 'HE';
}

export default function Sidebar({ active, onNavigate, isOpen, onClose }: SidebarProps) {
  const { user, logout } = useAuth();
  const role = user?.groups?.[0] || (user?.is_superuser ? 'Administrador' : 'Usuario');
  const displayName = user?.display_name || user?.username || 'Usuario Hogar Express';

  const visibleItems = NAV_ITEMS.filter((item) => {
    if (user?.is_superuser || role === 'Administrador') return true;
    if (role === 'Asesor Externo') return ['dashboard', 'venta'].includes(item.id);
    return item.id !== 'configuracion';
  });

  const navigate = (page: string) => {
    onNavigate(page);
    onClose();
  };

  return (
    <>
      {isOpen && <div className="sidebar-backdrop" onClick={onClose} aria-hidden="true" />}
      <aside className={`sidebar ${isOpen ? 'is-open' : ''}`} aria-label="Navegación principal">
        <div className="sidebar__brand">
          <BrandLogo />
          <button type="button" className="sidebar__close" onClick={onClose} aria-label="Cerrar menú">
            <X size={18} />
          </button>
        </div>

        <div className="sidebar__workspace">
          <div className="sidebar__workspace-icon"><BriefcaseBusiness size={17} /></div>
          <div>
            <span>Espacio de trabajo</span>
            <strong>Gestión inmobiliaria</strong>
          </div>
        </div>

        <div className="sidebar__section-label">Operación</div>
        <nav className="sidebar__nav">
          {visibleItems.map((item) => {
            const Icon = item.icon;
            const isActive = active === item.id;
            return (
              <button
                type="button"
                key={item.id}
                className={`sidebar__nav-item ${isActive ? 'is-active' : ''}`}
                onClick={() => navigate(item.id)}
                aria-current={isActive ? 'page' : undefined}
              >
                <Icon size={18} strokeWidth={2.1} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="sidebar__footer">
          <div className="sidebar__profile">
            <div className="sidebar__avatar">{initials(displayName)}</div>
            <div className="sidebar__profile-copy">
              <strong>{displayName}</strong>
              <span>{role}</span>
            </div>
            <button type="button" className="sidebar__logout" onClick={logout} aria-label="Cerrar sesión" title="Cerrar sesión">
              <LogOut size={17} />
            </button>
          </div>
        </div>
      </aside>
    </>
  );
}
