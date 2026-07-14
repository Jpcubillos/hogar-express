#!/bin/bash
# ======================================================================
# RESTORE SCRIPT — HOGAR EXPRESS
# ======================================================================

set -e

if [ -z "$1" ]; then
  echo "Error: Debe especificar la ruta al archivo SQL comprimido (.sql.gz)."
  echo "Uso: $0 <ruta_al_respaldo.sql.gz>"
  exit 1
fi

BACKUP_FILE="$1"

if [ ! -f "$BACKUP_FILE" ]; then
  echo "Error: El archivo de respaldo no existe en la ruta especificada."
  exit 1
fi

echo -e "\e[31m⚠️  ADVERTENCIA DE SEGURIDAD ⚠️\e[0m"
echo "Esta operación restaurará la base de datos reemplazando toda la información actual."
read -p "¿Está seguro de continuar? (escriba 'SI' para confirmar): " CONFIRM

if [ "$CONFIRM" != "SI" ]; then
  echo "Operación cancelada."
  exit 0
fi

echo "Iniciando restauración..."
# Drop and recreate schema to ensure a clean slate, then load dump
docker compose exec -T db psql -U hogar_express -d hogar_express -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
gunzip -c "$BACKUP_FILE" | docker compose exec -T db psql -U hogar_express -d hogar_express

echo "¡Restauración de base de datos completada con éxito!"
