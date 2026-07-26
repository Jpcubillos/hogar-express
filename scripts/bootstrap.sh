#!/bin/bash
# ======================================================================
# BOOTSTRAP SCRIPT (LINUX BASH) — HOGAR EXPRESS
# ======================================================================

set -e

echo -e "\e[36mIniciando proceso de configuración de Hogar Express...\e[0m"

# 1. Check Docker
if ! [ -x "$(command -v docker)" ]; then
  echo -e "\e[31mError: Docker no está instalado o no se encuentra en el PATH.\e[0m" >&2
  exit 1
fi

# 2. Check Docker Compose
if ! docker compose version &> /dev/null; then
  echo -e "\e[31mError: Docker Compose no está instalado.\e[0m" >&2
  exit 1
fi

# 3. Create .env if not exists
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
ENV_PATH="$SCRIPT_DIR/../.env"
EXAMPLE_PATH="$SCRIPT_DIR/../.env.example"

if [ ! -f "$ENV_PATH" ]; then
  if [ -f "$EXAMPLE_PATH" ]; then
    cp "$EXAMPLE_PATH" "$ENV_PATH"
    echo -e "\e[32mArchivo .env creado exitosamente desde .env.example.\e[0m"
  else
    echo -e "\e[31mError: No se encontró .env.example.\e[0m" >&2
    exit 1
  fi
else
  echo -e "\e[33mEl archivo .env ya existe. No se sobrescribió.\e[0m"
fi

# 4. Build and start services
echo -e "\e[90mConstruyendo y levantando contenedores con Docker Compose...\e[0m"
docker compose -f compose.yaml -f compose.dev.yaml up -d --build

# 5. Wait for DB Healthcheck
echo -e "\e[90mEsperando a que la base de datos de PostgreSQL esté lista...\e[0m"
retries=10
db_healthy=false
while [ $retries -gt 0 ] && [ "$db_healthy" = false ]; do
  status=$(docker inspect --format='{{json .State.Health.Status}}' hogar_express_db 2>/dev/null || true)
  if [ "$status" = '"healthy"' ]; then
    db_healthy=true
    echo -e "\e[32m¡Base de datos saludable y conectada!\e[0m"
  else
    echo -e "\e[33mBase de datos iniciando... reintentando en 3s ($retries intentos restantes)\e[0m"
    sleep 3
    retries=$((retries-1))
  fi
done

if [ "$db_healthy" = false ]; then
  echo -e "\e[31mError: La base de datos no pudo iniciar correctamente.\e[0m" >&2
  exit 1
fi

# 6. Run Migrations
echo -e "\e[90mEjecutando migraciones de base de datos...\e[0m"
docker compose exec backend python manage.py migrate

# 7. Seed Catalogs
echo -e "\e[90mCargando catálogos y configuración inicial...\e[0m"
docker compose exec backend python manage.py seed_catalogs

# 8. Seed Roles
echo -e "\e[90mCargando roles y permisos en la base de datos...\e[0m"
docker compose exec backend python manage.py seed_roles

# 8.5 Seed Demo Data
echo -e "\e[90mCargando datos de prueba de inmuebles y propietarios...\e[0m"
docker compose exec backend python manage.py seed_demo

# 9. Create Superuser (Idempotent try)
echo -e "\e[90mCreando superusuario de administración...\e[0m"
docker compose exec backend python manage.py createsuperuser --noinput || true

# 9. Finished
echo -e "\n\e[36m======================================================================\e[0m"
echo -e "\e[32mHogar Express levantado con éxito. Accede a los siguientes enlaces:\e[0m"
echo -e "\e[32m  - Frontend:   http://localhost:5173\e[0m"
echo -e "\e[32m  - Backend API: http://localhost:8000/api/v1/\e[0m"
echo -e "\e[32m  - Django Admin:http://localhost:8000/admin/\e[0m"
echo -e "\e[32m  - API Docs:    http://localhost:8000/api/docs/\e[0m"
echo -e "\e[36m======================================================================\e[0m"
