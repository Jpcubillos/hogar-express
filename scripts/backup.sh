#!/bin/bash
# ======================================================================
# BACKUP SCRIPT — HOGAR EXPRESS
# ======================================================================

set -e

BACKUP_DIR="${BACKUP_DIR:-./infrastructure/backups}"
mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
DB_BACKUP_FILE="$BACKUP_DIR/db_backup_$TIMESTAMP.sql.gz"
MEDIA_BACKUP_FILE="$BACKUP_DIR/media_backup_$TIMESTAMP.tar.gz"

echo "Iniciando respaldo de base de datos..."
# Run pg_dump inside db container and compress locally
docker compose exec -T db pg_dump -U hogar_express hogar_express | gzip > "$DB_BACKUP_FILE"
echo "Respaldo de base de datos guardado en: $DB_BACKUP_FILE"

echo "Iniciando respaldo de archivos media..."
# Tar the media directory of backend service using a temporary tar command in backend
docker compose exec -T backend tar -czf - -C /app media > "$MEDIA_BACKUP_FILE"
echo "Respaldo de archivos media guardado en: $MEDIA_BACKUP_FILE"

echo "¡Proceso de copia de seguridad completado con éxito!"
