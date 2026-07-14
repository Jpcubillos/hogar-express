# Hogar Express

Hogar Express es una plataforma web interna para la gestión inmobiliaria en Colombia. Este repositorio contiene la base técnica profesional, modular y contenerizada del sistema, migrada desde el prototipo MVP original.

## Stack Tecnológico

- **Backend:** Python 3.13 + Django 5.2.16 LTS + Django REST Framework 3.17.1.
- **Frontend:** React 19 + TypeScript + Vite 8.1.0 + React Router v7.
- **Base de Datos:** PostgreSQL 17.
- **Contenedores:** Docker & Docker Compose.

---

## Requisitos Previos

- Docker (v20.10+)
- Docker Compose (v2.0+)
- Git

---

## Inicio Rápido (Bootstrap)

El sistema se puede levantar completamente desde cero con un solo comando gracias a los scripts de automatización:

### En Windows (PowerShell):
```powershell
./scripts/bootstrap.ps1
```

### En Linux / macOS:
```bash
chmod +x scripts/*.sh
./scripts/bootstrap.sh
```

Este script:
1. Creará tu archivo `.env` local a partir de `.env.example`.
2. Descargará las imágenes oficiales e iniciará los contenedores.
3. Esperará a que PostgreSQL esté saludable.
4. Aplicará las migraciones de Django.
5. Cargará los roles y permisos (`seed_roles`).
6. Creará el superusuario administrador por defecto.

---

## URLs de Acceso Local

- **Frontend:** [http://localhost:5173](http://localhost:5173)
- **Backend API:** [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/)
- **Django Admin:** [http://localhost:8000/admin/](http://localhost:8000/admin/)
- **API Docs (OpenAPI):** [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)

---

## Credenciales de Demostración

Si se habilita la semilla demo (`python manage.py seed_demo`), puedes usar:

| Rol | Usuario | Contraseña |
|---|---|---|
| **Administrador** | `admin` | `change_me` |
| **Asesor Interno** | `intern` | `change_me` |
| **Asesor Externo** | `extern` | `change_me` |
| **Consulta / Lectura** | `visitor` | `change_me` |

*Advertencia: Cambiar estas contraseñas por defecto antes de desplegar a producción.*

---

## Comandos Útiles

### Levantar en Desarrollo
```bash
./scripts/dev.ps1   # Windows
./scripts/dev.sh    # Linux/macOS
```

### Ejecutar Pruebas y Linting
```bash
./scripts/test.ps1  # Windows
./scripts/test.sh   # Linux/macOS
```

### Realizar Copias de Seguridad (Backup)
```bash
./scripts/backup.sh
```
