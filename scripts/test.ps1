Write-Host "Ejecutando verificaciones y pruebas en el backend..." -ForegroundColor Cyan
docker compose exec backend python manage.py check
if ($LASTEXITCODE -ne 0) { Write-Error "Checks de Django fallidos."; Exit 1 }

docker compose exec backend pytest
if ($LASTEXITCODE -ne 0) { Write-Error "Pruebas de Pytest fallidas."; Exit 1 }

Write-Host "Ejecutando verificaciones y pruebas en el frontend..." -ForegroundColor Cyan
docker compose exec frontend npm run lint
if ($LASTEXITCODE -ne 0) { Write-Error "Eslint del frontend fallido."; Exit 1 }

docker compose exec frontend npm run typecheck
if ($LASTEXITCODE -ne 0) { Write-Error "Typecheck de TypeScript fallido."; Exit 1 }

docker compose exec frontend npm run test -- --run
if ($LASTEXITCODE -ne 0) { Write-Error "Pruebas de Vitest fallidas."; Exit 1 }

Write-Host "¡Todas las pruebas y verificaciones pasaron exitosamente!" -ForegroundColor Green
