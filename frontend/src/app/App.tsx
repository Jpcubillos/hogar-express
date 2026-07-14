import React, { useState } from 'react';
import Sidebar from '../layouts/Sidebar';
import { COLOR } from '../styles/colors';
import { AppProviders, useAuth } from './providers/AppProviders';
import { Card, Button, Input, Field } from '../components/ui';

// Import Features
import Dashboard from '../features/dashboard/Dashboard';
import Propietarios from '../features/owners/Propietarios';
import Inmuebles from '../features/properties/Inmuebles';
import Alquiler from '../features/rentals/Alquiler';
import Venta from '../features/sales/Venta';
import Arreglos from '../features/repairs/Arreglos';
import Reportes from '../features/reports/Reportes';
import Configuracion from '../features/settings/Configuracion';

function LoginScreen() {
  const { login } = useAuth();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(username, password);
    } catch (err: any) {
      setError(err.response?.data?.message || "Error al iniciar sesión. Por favor verifique sus credenciales.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      minHeight: '100vh', background: COLOR.fondo, padding: 20
    }}>
      <Card style={{ width: 400, boxShadow: '0 8px 30px rgba(0,0,0,0.08)', padding: 30 }}>
        <div style={{ textAlign: 'center', marginBottom: 25 }}>
          <h2 style={{ fontFamily: 'Georgia, serif', fontSize: 24, fontWeight: 700, color: COLOR.carbon, margin: '0 0 6px' }}>
            Hogar<span style={{ color: COLOR.mostaza }}>E</span>xpres
          </h2>
          <p style={{ fontSize: 13.5, color: COLOR.carbonSuave, margin: 0 }}>Ingreso al sistema administrativo</p>
        </div>

        {error && (
          <div style={{
            background: COLOR.rojoClaro, color: COLOR.rojo, padding: '10px 12px',
            borderRadius: 8, fontSize: 12.5, marginBottom: 16, fontWeight: 600
          }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <Field label="Usuario">
            <Input 
              value={username} 
              onChange={(e) => setUsername(e.target.value)} 
              placeholder="admin" 
              required 
            />
          </Field>
          <Field label="Contraseña">
            <Input 
              type="password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              placeholder="••••••••" 
              required 
            />
          </Field>
          <Button type="submit" style={{ width: '100%', marginTop: 10 }} disabled={loading}>
            {loading ? "Iniciando sesión..." : "Iniciar Sesión"}
          </Button>
        </form>
      </Card>
    </div>
  );
}

function AppContent() {
  const { isAuthenticated, isLoading } = useAuth();
  const [pagina, setPagina] = useState<string>("dashboard");
  const [rol, setRol] = useState<string>("Administrador");

  if (isLoading) {
    return (
      <div style={{
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
        minHeight: '100vh', background: COLOR.fondo, color: COLOR.carbonSuave
      }}>
        <h3 style={{ fontFamily: 'Georgia, serif', fontSize: 20, color: COLOR.azul, marginBottom: 10 }}>Cargando Hogar Express...</h3>
        <div style={{ fontSize: 13 }}>Por favor espere un momento.</div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <LoginScreen />;
  }

  const paginas: Record<string, React.ReactNode> = {
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
    <div style={{ 
      fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif", 
      background: COLOR.fondo, 
      minHeight: "100vh" 
    }}>
      <Sidebar active={pagina} onNavigate={setPagina} rol={rol} setRol={setRol} />
      <div style={{ marginLeft: 232, padding: "28px 32px" }}>
        {paginas[pagina] || <Dashboard onNavigate={setPagina} />}
      </div>
    </div>
  );
}

export default function App() {
  return (
    <AppProviders>
      <AppContent />
    </AppProviders>
  );
}
