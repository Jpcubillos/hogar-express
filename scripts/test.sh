#!/bin/bash
set -e

echo "Ejecutando verificaciones y pruebas en el backend..."
docker compose exec backend python manage.py check
docker compose exec backend pytest

echo "Ejecutando verificaciones y pruebas en el frontend..."
docker compose exec frontend npm run lint
docker compose exec frontend npm run typecheck
docker compose exec frontend npm run test -- --run

echo "¡Todas las pruebas y verificaciones pasaron exitosamente!"
