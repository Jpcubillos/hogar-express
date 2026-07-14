# ======================================================================
# BOOTSTRAP SCRIPT (WINDOWS POWERSHELL) — HOGAR EXPRESS
# ======================================================================

Write-Host "Iniciando proceso de configuración de Hogar Express..." -ForegroundColor Cyan

# 1. Check Docker
Write-Host "Verificando instalación de Docker..." -ForegroundColor Gray
$dockerCheck = Get-Command docker -ErrorAction SilentlyContinue
if (-not $dockerCheck) {
    Write-Error "Docker no está instalado o no se encuentra en el PATH. Por favor instálalo antes de continuar."
    Exit 1
}

# 2. Check Docker Compose
Write-Host "Verificando instalación de Docker Compose..." -ForegroundColor Gray
$composeCheck = Get-Command "docker-compose" -ErrorAction SilentlyContinue
if (-not $composeCheck) {
    $composeCmdCheck = docker compose version 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Docker Compose no está instalado. Por favor instálalo antes de continuar."
        Exit 1
    }
}

# 3. Create .env if not exists
Write-Host "Verificando variables de entorno (.env)..." -ForegroundColor Gray
$envPath = Join-Path $PSScriptRoot "..\.env"
$examplePath = Join-Path $PSScriptRoot "..\.env.example"

if (-not (Test-Path $envPath)) {
    if (Test-Path $examplePath) {
        Copy-Item $examplePath $envPath
        Write-Host "Archivo .env creado exitosamente desde .env.example." -ForegroundColor Green
    } else {
        Write-Error "No se encontró el archivo .env.example para inicializar las variables de entorno."
        Exit 1
    }
} else {
    Write-Host "El archivo .env ya existe. No se sobrescribió." -ForegroundColor Yellow
}

# 4. Build and start services (db first to ensure healthcheck is ready)
Write-Host "Construyendo y levantando contenedores con Docker Compose..." -ForegroundColor Gray
docker compose -f compose.yaml -f compose.dev.yaml up -d --build

if ($LASTEXITCODE -ne 0) {
    Write-Error "Error al levantar los contenedores mediante Docker Compose."
    Exit 1
}

# 5. Wait for DB Healthcheck
Write-Host "Esperando a que la base de datos de PostgreSQL esté lista..." -ForegroundColor Gray
$retries = 10
$dbHealthy = $false
while ($retries -gt 0 -and -not $dbHealthy) {
    $status = docker inspect --format='{{json .State.Health.Status}}' hogar_express_db 2>$null
    if ($status -eq '"healthy"') {
        $dbHealthy = $true
        Write-Host "¡Base de datos saludable y conectada!" -ForegroundColor Green
    } else {
        Write-Host "Base de datos iniciando... reintentando en 3s ($retries intentos restantes)" -ForegroundColor Yellow
        Start-Sleep -Seconds 3
        $retries--
    }
}

if (-not $dbHealthy) {
    Write-Error "La base de datos no pudo iniciar correctamente en el tiempo esperado."
    Exit 1
}

# 6. Run Migrations
Write-Host "Ejecutando migraciones de base de datos..." -ForegroundColor Gray
docker compose exec backend python manage.py migrate

# 7. Seed Roles
Write-Host "Cargando roles y permisos en la base de datos..." -ForegroundColor Gray
docker compose exec backend python manage.py seed_roles

# 8. Create Superuser (Idempotent try)
Write-Host "Creando superusuario de administración..." -ForegroundColor Gray
docker compose exec backend python manage.py createsuperuser --noinput 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "Superusuario creado exitosamente." -ForegroundColor Green
} else {
    Write-Host "El superusuario ya existe o fue configurado previamente." -ForegroundColor Yellow
}

# 9. Finished
Write-Host "`n======================================================================" -ForegroundColor Cyan
Write-Host "Hogar Express levantado con éxito. Accede a los siguientes enlaces:" -ForegroundColor Green
Write-Host "  - Frontend:   http://localhost:5173" -ForegroundColor Green
Write-Host "  - Backend API: http://localhost:8000/api/v1/" -ForegroundColor Green
Write-Host "  - Django Admin:http://localhost:8000/admin/" -ForegroundColor Green
Write-Host "  - API Docs:    http://localhost:8000/api/docs/" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
