# Arquitectura Técnica: Hogar Express

## Componentes del Sistema

El sistema se compone de los siguientes contenedores aislados:

1. **db**: Base de datos relacional PostgreSQL 17.
2. **backend**: Capa transaccional Django 5.2.16 + Django REST Framework 3.17.1.
3. **frontend**: SPA React 19 + Vite 8.1.0 servido localmente con HMR en desarrollo.
4. **nginx**: Proxy inverso en producción que sirve estáticos y redirige `/api/` y `/admin/`.

```
[Cliente (Navegador)] ──(Puerto 80)──> [ Nginx (Prod) ]
                                            │
               ┌────────────────────────────┴──────────────────────────┐
               ▼                                                       ▼
      [ Frontend Dist ]                                        [ Backend (WSGI) ]
                                                                       │
                                                                       ▼
                                                              [ PostgreSQL (db) ]
```

## Seguridad de Solicitudes

- Autenticación mediante sesiones seguras con cookies HTTPOnly (`SameSite=Lax`).
- Protección CSRF activa mediante cabecera `X-CSRFToken` e interceptores de Axios.
- Almacenamiento de archivos binarios fuera de la base de datos con URLs cifradas por UUID y descarga protegida con autenticación.
