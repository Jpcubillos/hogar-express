# Hogar Express

Hogar Express es una plataforma web interna para la gestión inmobiliaria en Colombia. El repositorio contiene una arquitectura modular y contenerizada migrada desde el MVP original.

## Stack tecnológico

- Backend: Python 3.13, Django 5.2.16 LTS y Django REST Framework 3.17.1.
- Frontend: React 19, TypeScript, Vite 8.1.0 y React Router v7.
- Base de datos: PostgreSQL 17.
- Contenedores: Docker y Docker Compose.

## Requisitos

- Docker 20.10 o superior.
- Docker Compose 2.0 o superior.
- Git.

## Inicio rápido

En Windows, desde la raíz del repositorio:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap.ps1
```

En Linux o macOS:

```bash
chmod +x scripts/*.sh
./scripts/bootstrap.sh
```

El bootstrap:

1. Crea `.env` desde `.env.example` si no existe.
2. Construye e inicia los contenedores.
3. Espera a PostgreSQL.
4. Aplica todas las migraciones.
5. Carga catálogos, organización, consecutivos y requisitos documentales (`seed_catalogs`).
6. Carga roles y permisos (`seed_roles`).
7. Crea el superusuario configurado en `.env`.

## Actualización desde el esquema anterior

El modelo de dominio fue consolidado antes de existir datos productivos. Si ya habías iniciado una versión anterior, el volumen local conserva un historial incompatible. Guarda cualquier dato que necesites y recrea una sola vez la base local:

```powershell
docker compose -f compose.yaml -f compose.dev.yaml down -v
powershell -ExecutionPolicy Bypass -File .\scripts\bootstrap.ps1
```

`down -v` elimina la base local y los archivos cargados. No debe ejecutarse en un ambiente con información que necesite conservarse.

## Acceso local

- Frontend: [http://localhost:5173](http://localhost:5173)
- API: [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/)
- Administración Django: [http://localhost:8000/admin/](http://localhost:8000/admin/)
- Documentación OpenAPI: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- Esquema OpenAPI: [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

## Usuarios y permisos

El primer administrador se toma de `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL` y
`DJANGO_SUPERUSER_PASSWORD` en `.env`. Después del arranque puedes crear usuarios de dos formas:

- Desde Django Admin, en `http://localhost:8000/admin/`, asignando uno de los grupos creados por `seed_roles`.
- Desde `POST /api/v1/auth/users/`, enviando como mínimo `username` y `password`; el endpoint requiere permisos de administración de usuarios.

El frontend puede consultar los roles y sus permisos en `GET /api/v1/auth/roles/`.

La contraseña se almacena mediante el algoritmo seguro de Django y nunca se devuelve en la API. Los roles iniciales son
`Administrador`, `Asesor Interno`, `Asesor Externo` y `Consulta`. La configuración empresarial y sus políticas se administran
desde `/api/v1/configuration/` o desde Django Admin.

## Datos de demostración

Para desarrollo únicamente:

```powershell
docker compose exec backend python manage.py seed_demo
```

| Rol | Usuario | Contraseña |
|---|---|---|
| Administrador | `admin` | `change_me` |
| Asesor Interno | `intern` | `change_me` |
| Asesor Externo | `extern` | `change_me` |
| Consulta | `visitor` | `change_me` |

Estas contraseñas son públicas y nunca deben utilizarse en producción.

## Comandos útiles

Iniciar desarrollo:

```powershell
.\scripts\dev.ps1
```

Ejecutar pruebas y validaciones:

```powershell
.\scripts\test.ps1
```

Linux o macOS dispone de los equivalentes `dev.sh`, `test.sh` y `backup.sh`.

## Modelo de dominio

La estructura completa, las aplicaciones y los servicios transaccionales están descritos en [docs/domain-model.md](docs/domain-model.md). Los endpoints disponibles para integrar el frontend se publican automáticamente en OpenAPI.
