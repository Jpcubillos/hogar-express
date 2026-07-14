ACTÚA COMO ARQUITECTO DE SOFTWARE SENIOR, DESARROLLADOR FULL STACK SENIOR,
ESPECIALISTA EN DJANGO, REACT, POSTGRESQL, DOCKER, SEGURIDAD WEB,
MIGRACIONES DE SISTEMAS LEGADOS Y DISEÑO DE SISTEMAS ADMINISTRATIVOS.

Estás trabajando directamente dentro de un repositorio existente de un proyecto
llamado HOGAR EXPRESS, correspondiente a un software interno para una inmobiliaria
colombiana.

NO quiero únicamente recomendaciones, explicaciones ni un plan teórico.

QUIERO QUE:

1. Analices por completo el repositorio actual.
2. Protejas lo que ya existe antes de modificarlo.
3. Identifiques y documentes la interfaz, colores, logo, tipografías, rutas,
   componentes, acciones y comportamiento actual.
4. Reconstruyas la arquitectura técnica desde cero.
5. Mantengas visualmente la misma interfaz existente.
6. Migres la aplicación a una arquitectura profesional:
   - Backend Django.
   - API con Django REST Framework.
   - Frontend React + TypeScript + Vite.
   - PostgreSQL.
   - Docker y Docker Compose.
7. Dejes el repositorio completamente ejecutable por cualquier integrante del equipo
   con pocos comandos.
8. Ejecutes realmente las instalaciones, migraciones, pruebas y compilaciones.
9. No finalices hasta comprobar que el sistema arranca desde cero sin errores.
10. Documentes claramente qué hiciste, cómo se ejecuta y qué queda preparado para
    desarrollar posteriormente.

NO RESPONDAS SOLO CON UN PLAN.
PRIMERO PUEDES MOSTRAR UN RESUMEN DEL PLAN, PERO DESPUÉS DEBES EJECUTARLO.

======================================================================
1. CONTEXTO DEL PROYECTO
======================================================================

Hogar Express es una inmobiliaria que actualmente utiliza una base de datos antigua
en Microsoft Access. Se está construyendo un sistema web interno para reemplazarla.

El sistema será utilizado por empleados y colaboradores autorizados de la inmobiliaria.

Los siguientes actores NO iniciarán sesión:

- Propietarios.
- Arrendatarios.
- Codeudores.
- Apoderados.
- Proveedores.
- Compradores.

Estas personas son registros del negocio, no usuarios del sistema.

Los usuarios del sistema corresponden inicialmente a estos roles:

1. Administrador.
2. Asesor Interno.
3. Asesor Externo.
4. Consulta / Solo lectura.

El diseño actual contiene un selector llamado “Simular rol (demo)”.
Ese selector debe conservarse solamente en desarrollo como herramienta de demostración,
pero no debe sustituir la autenticación ni los permisos reales.

Debe controlarse mediante una variable:

VITE_ENABLE_ROLE_SIMULATOR=true

En producción debe estar desactivado y oculto.

Los módulos generales previstos para la aplicación son:

- Dashboard.
- Propietarios.
- Inmuebles.
- Personas:
  - Arrendatarios.
  - Codeudores.
  - Apoderados.
- Alquileres.
- Contratos.
- Pagos.
- Historial de pagos.
- Recaudo arrendatario.
- Recaudo propietario.
- Afianzadoras.
- Ventas.
- Arreglos y reparaciones.
- Novedades del inmueble.
- Inventario.
- Documentos y fotografías.
- Reportes.
- Usuarios, roles y permisos.
- Auditoría.
- Catálogos y configuración.

No desarrolles todavía de forma definitiva todas las reglas del negocio que están
pendientes de aprobación del cliente.

La prioridad de esta tarea es construir una BASE TÉCNICA PROFESIONAL, SEGURA,
MODULAR, DOCUMENTADA Y REPRODUCIBLE, conservando la interfaz existente.

Debe quedar preparada para que distintos integrantes trabajen paralelamente en:

- Propietarios e inmuebles.
- Alquileres y contratos.
- Pagos y recaudos.
- Ventas.
- Arreglos.
- Reportes.
- Autenticación y configuración.

======================================================================
2. REGLAS DE SEGURIDAD ANTES DE MODIFICAR EL REPOSITORIO
======================================================================

Antes de cambiar cualquier archivo:

1. Ejecuta:
   - git status
   - git branch
   - git log --oneline -n 10

2. No ejecutes:
   - git reset --hard
   - git clean -fd
   - rm -rf sobre el proyecto completo
   - eliminación del directorio .git
   - eliminación de cambios no confirmados

3. Si existen cambios sin commit:
   - No los descartes.
   - Documenta cuáles son.
   - Haz una copia de seguridad segura dentro de:
     docs/legacy-backup-info.md
   - Conserva los archivos originales.

4. Crea una rama nueva, siempre que el entorno Git lo permita:

   chore/django-docker-foundation

5. Si no puedes crear la rama:
   - Continúa sin destruir cambios.
   - Informa la razón al final.

6. Antes de reemplazar la arquitectura:
   - Identifica el commit actual.
   - Regístralo en:
     docs/legacy-audit.md

7. No borres inmediatamente el código anterior.
   Si debe retirarse de la aplicación principal, muévelo temporalmente a una ubicación
   claramente identificada, por ejemplo:

   legacy/

   Pero solo hazlo si no genera duplicación innecesaria o problemas de Git.
   Es preferible conservar la historia mediante la rama y los commits.

======================================================================
3. FASE OBLIGATORIA DE ANÁLISIS DEL PROYECTO EXISTENTE
======================================================================

Inspecciona recursivamente el repositorio antes de construir la nueva arquitectura.

Debes identificar:

- Tecnologías actuales.
- Framework frontend actual.
- Framework backend actual, si existe.
- Gestor de paquetes.
- Estructura de carpetas.
- Rutas y páginas.
- Componentes compartidos.
- Estilos globales.
- Archivos CSS, SCSS, Tailwind u otros.
- Variables CSS.
- Colores exactos.
- Tipografías.
- Tamaños de texto.
- Iconografía.
- Logo.
- Imágenes.
- Menú lateral.
- Barra superior.
- Tarjetas.
- Tablas.
- Formularios.
- Modales.
- Filtros.
- Botones.
- Estados de carga.
- Estados vacíos.
- Mensajes de error.
- Diseño responsivo.
- Acciones actualmente simuladas.
- Datos hardcodeados.
- Selector de roles demo.
- Rutas incompletas.
- Código duplicado.
- Dependencias innecesarias.
- Secretos expuestos.
- Archivos que no deben estar en Git.

Intenta ejecutar la aplicación actual antes de modificarla.

Si puede ejecutarse:

1. Iníciala.
2. Recorre todas las rutas.
3. Registra cada pantalla.
4. Toma capturas locales si el entorno permite hacerlo.
5. Identifica estados alternativos:
   - Listado.
   - Detalle.
   - Creación.
   - Edición.
   - Modal.
   - Menú desplegado.
   - Filtros.
   - Roles simulados.
6. Usa estas capturas como referencia de regresión visual.

Si la aplicación actual no puede ejecutarse:

1. No inventes su diseño.
2. Analiza el código y los recursos existentes.
3. Documenta por qué no inicia.
4. Recupera la mayor cantidad posible de información visual desde los archivos.

Crea obligatoriamente:

docs/legacy-audit.md

Debe contener:

- Stack anterior.
- Comandos que utilizaba.
- Estructura anterior.
- Rutas detectadas.
- Componentes detectados.
- Dependencias.
- Problemas encontrados.
- Activos visuales.
- Logo.
- Paleta.
- Elementos reutilizables.
- Elementos descartados y motivo.
- Riesgos de migración.

Crea también:

docs/design-system.md

Debe documentar:

- Colores exactos en hexadecimal, RGB o HSL.
- Colores de fondo.
- Colores del menú.
- Colores de tarjetas.
- Colores de botones.
- Estados hover.
- Estados activos.
- Bordes.
- Sombras.
- Radios.
- Espaciado.
- Tipografía.
- Tamaños.
- Pesos.
- Iconos.
- Anchura del sidebar.
- Altura del header.
- Estilo de tablas.
- Estilo de formularios.
- Breakpoints.
- Componentes visuales reutilizables.

REGLA CRÍTICA:

NO rediseñes la aplicación por gusto.
NO cambies la identidad visual.
NO cambies los colores porque consideres otros “más modernos”.
NO generes un logo nuevo.
NO reemplaces el logo con uno aproximado.
NO reconstruyas el logo con inteligencia artificial.

Debes reutilizar exactamente el archivo original del logo existente.

Si existen varias versiones del logo:

- Identifica cuál usa actualmente la interfaz.
- Conserva las otras dentro de assets.
- Documenta sus usos.

======================================================================
4. OBJETIVO VISUAL
======================================================================

La nueva aplicación debe conservar:

- Mismo logo.
- Misma paleta de colores.
- Mismo menú lateral.
- Mismos nombres visibles.
- Misma estructura general.
- Mismos botones.
- Mismos iconos cuando sea posible.
- Misma distribución.
- Mismas tarjetas.
- Mismas tablas.
- Mismos formularios.
- Mismos modales.
- Mismas acciones existentes.
- Mismo comportamiento responsive.
- Mismo selector de roles demo en desarrollo.

Puedes mejorar internamente:

- Accesibilidad.
- Semántica HTML.
- Organización de componentes.
- Tipado.
- Rendimiento.
- Estados de carga.
- Gestión de errores.
- Reutilización.
- Navegación por teclado.
- Contraste, únicamente si el cambio es imperceptible y necesario para accesibilidad.

No debes alterar visualmente la interfaz sin documentarlo.

Si un elemento anterior está roto:

1. Repáralo.
2. Conserva su intención visual.
3. Registra el cambio en:
   docs/ui-migration.md

Crea una tabla de equivalencias:

| Pantalla anterior | Ruta nueva | Estado | Diferencias |
|-------------------|------------|--------|-------------|

======================================================================
5. STACK TÉCNICO OBLIGATORIO
======================================================================

Utiliza la siguiente base:

BACKEND

- Python 3.13.
- Django 5.2.16 LTS.
- Django REST Framework 3.17.1.
- PostgreSQL 17.
- psycopg versión 3.
- django-filter.
- drf-spectacular para OpenAPI.
- django-cors-headers solo donde sea necesario.
- Pillow para imágenes.
- Gunicorn para producción.
- WhiteNoise solo si resulta necesario para archivos estáticos administrativos.
- pytest.
- pytest-django.
- coverage.
- Ruff.

FRONTEND

- Node.js 24 LTS.
- React 19.2.7.
- TypeScript.
- Vite 8.1.x estable.
- React Router.
- TanStack Query.
- React Hook Form.
- Zod.
- Un cliente HTTP centralizado.
- Vitest.
- React Testing Library.
- ESLint.
- Prettier.

BASE DE DATOS

- PostgreSQL 17.
- UTF-8.
- Zona horaria de negocio:
  America/Bogota.

CONTENEDORES

- Docker.
- Docker Compose usando la especificación actual.
- No agregues la propiedad obsoleta “version” en los archivos Compose.
- Contenedores separados para:
  - database
  - backend
  - frontend
  - nginx en producción

No agregues Redis, Celery, RabbitMQ ni otros servicios todavía, salvo que encuentres una
funcionalidad existente que realmente dependa de ellos.

Deja documentado cómo podrían incorporarse más adelante para:

- Alertas.
- Correos.
- Reportes pesados.
- Generación masiva de PDF.
- Tareas programadas.
- Backups.
- Procesamiento de imágenes.

DEPENDENCIAS

No uses rangos abiertos sin control.

Backend:

- Crea archivos fuente de dependencias y archivos bloqueados.
- Puedes utilizar pip-tools.
- Genera:
  requirements/base.in
  requirements/base.txt
  requirements/dev.in
  requirements/dev.txt
  requirements/prod.in
  requirements/prod.txt
- Los archivos .txt finales deben contener versiones exactas.
- Docker debe instalar desde los archivos bloqueados.

Frontend:

- Usa npm.
- Genera y conserva package-lock.json.
- El Dockerfile debe usar npm ci.
- No uses npm install durante el build de producción.
- Fija versiones compatibles.
- Registra las versiones finales en:
  docs/dependency-versions.md

IMÁGENES DOCKER

Intenta utilizar imágenes oficiales equivalentes a:

- python:3.13-slim
- node:24-alpine
- postgres:17-alpine
- nginx:alpine

Antes de fijar un tag exacto:

1. Verifica que exista.
2. Si puedes, fija el patch exacto.
3. Si no existe el tag exacto, utiliza la rama mayor estable.
4. Registra el tag finalmente usado.
5. No uses imágenes “latest”.

======================================================================
6. ARQUITECTURA DEL REPOSITORIO
======================================================================

La estructura final debe ser clara y similar a esta:

hogar-express/
├── backend/
│   ├── config/
│   │   ├── settings/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   ├── test.py
│   │   │   └── production.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── apps/
│   │   ├── core/
│   │   ├── accounts/
│   │   ├── audit/
│   │   ├── catalogs/
│   │   ├── documents/
│   │   ├── owners/
│   │   ├── properties/
│   │   ├── people/
│   │   ├── rentals/
│   │   ├── payments/
│   │   ├── guarantors/
│   │   ├── sales/
│   │   ├── repairs/
│   │   └── reports/
│   │
│   ├── requirements/
│   ├── scripts/
│   ├── tests/
│   ├── manage.py
│   ├── Dockerfile
│   └── .dockerignore
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── app/
│   │   ├── assets/
│   │   ├── components/
│   │   ├── features/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── hooks/
│   │   ├── lib/
│   │   ├── mocks/
│   │   ├── styles/
│   │   ├── types/
│   │   └── tests/
│   ├── Dockerfile
│   ├── Dockerfile.prod
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── .dockerignore
│
├── infrastructure/
│   ├── nginx/
│   │   ├── nginx.conf
│   │   └── default.conf
│   ├── postgres/
│   ├── backups/
│   └── scripts/
│
├── scripts/
│   ├── bootstrap.sh
│   ├── bootstrap.ps1
│   ├── dev.sh
│   ├── dev.ps1
│   ├── test.sh
│   ├── test.ps1
│   ├── backup.sh
│   └── restore.sh
│
├── docs/
├── compose.yaml
├── compose.dev.yaml
├── compose.prod.yaml
├── .env.example
├── .gitignore
├── README.md
└── CONTRIBUTING.md

Puedes adaptar ligeramente la estructura si existe una razón técnica real, pero debes:

- Mantener backend y frontend separados.
- Mantener aplicaciones Django por dominio.
- Evitar una aplicación Django monolítica llamada simplemente “api”.
- Evitar meter toda la lógica en views.py.
- Evitar componentes React gigantes.
- Documentar cualquier cambio respecto a la estructura propuesta.

======================================================================
7. CONFIGURACIÓN DE DJANGO
======================================================================

Crea el proyecto Django de forma profesional.

Configura settings separados:

- base
- development
- test
- production

No dupliques configuraciones innecesariamente.

Variables obligatorias mediante entorno:

DJANGO_SETTINGS_MODULE
DJANGO_SECRET_KEY
DJANGO_DEBUG
DJANGO_ALLOWED_HOSTS
DJANGO_CSRF_TRUSTED_ORIGINS
DJANGO_SECURE_SSL_REDIRECT
DJANGO_SESSION_COOKIE_SECURE
DJANGO_CSRF_COOKIE_SECURE
DJANGO_LOG_LEVEL

POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
POSTGRES_HOST
POSTGRES_PORT

DATABASE_URL, si decides soportarla adicionalmente.

CORS_ALLOWED_ORIGINS
FRONTEND_URL

MEDIA_ROOT
MEDIA_URL
MAX_UPLOAD_SIZE_MB

DJANGO_SUPERUSER_EMAIL
DJANGO_SUPERUSER_PASSWORD
DJANGO_SUPERUSER_USERNAME

ENABLE_DEMO_DATA
ENABLE_ROLE_SIMULATOR

No incluyas secretos reales en Git.

Crea:

.env.example

con valores descriptivos, pero no peligrosos.

El archivo real .env debe estar en .gitignore.

Configuración regional:

LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

Configura PostgreSQL como única base de datos real.

NO uses SQLite ni siquiera como configuración principal de desarrollo.
Las pruebas pueden utilizar PostgreSQL de prueba dentro de Docker.

Usa Decimal para dinero.
Nunca uses float para:

- Canon.
- Costos.
- Comisiones.
- Descuentos.
- Recaudos.
- Avalúos.
- Intereses.
- Porcentajes.

======================================================================
8. MODELO DE USUARIOS, ROLES Y PERMISOS
======================================================================

Crea un modelo de usuario personalizado desde el comienzo.

Debe extender AbstractUser o una alternativa apropiada.

Nombre recomendado:

accounts.User

Debe contemplar:

- UUID como identificador primario.
- username o email según la decisión mejor soportada.
- email.
- nombre visible.
- estado activo.
- fecha de creación.
- fecha de actualización.
- último acceso.
- posibilidad de asociarse a uno o varios grupos.
- campos futuros sin romper el modelo estándar.

Define:

AUTH_USER_MODEL = "accounts.User"

NO esperes a cambiar el modelo de usuario más adelante.

Usa:

- Django Groups.
- Django Permissions.
- Permisos personalizados.
- Permisos a nivel de endpoint.
- Permisos a nivel de acciones importantes.

Crea un comando idempotente:

python manage.py seed_roles

Este comando debe crear o actualizar estos grupos iniciales:

1. Administrador.
2. Asesor Interno.
3. Asesor Externo.
4. Consulta.

No dupliques grupos cuando el comando se ejecuta varias veces.

MATRIZ INICIAL DE PERMISOS

ADMINISTRADOR

- Acceso completo.
- Gestión de usuarios.
- Gestión de grupos.
- Gestión de permisos.
- Configuración.
- Catálogos.
- Auditoría.
- Todos los módulos.
- Todos los reportes.
- Acceso a datos financieros.
- Correcciones administrativas.

ASESOR INTERNO

- Consultar y gestionar propietarios.
- Consultar y gestionar inmuebles.
- Gestionar personas.
- Gestionar alquileres.
- Gestionar contratos.
- Registrar pagos.
- Generar recibos.
- Gestionar arreglos.
- Gestionar documentos.
- Consultar reportes operativos.
- Exportar reportes permitidos.
- No administrar usuarios.
- No cambiar parámetros globales sensibles.
- No eliminar auditoría.
- No eliminar operaciones financieras cerradas.

ASESOR EXTERNO

- Acceso limitado al módulo de ventas.
- Consulta de inmuebles disponibles para venta.
- Gestión de registros de venta asignados, cuando se implemente.
- Sin acceso a datos bancarios.
- Sin acceso a recaudos.
- Sin acceso a pagos de arrendatarios.
- Sin acceso a liquidaciones.
- Sin acceso a información financiera de alquiler.
- Sin acceso a arreglos ajenos a su proceso de venta.

CONSULTA

- Solo lectura sobre módulos permitidos.
- Puede consultar reportes autorizados.
- No crea.
- No modifica.
- No elimina.
- No registra pagos.
- No genera movimientos financieros.

IMPORTANTE:

Los nombres de los roles iniciales no deben ser la única fuente de autorización.

El frontend NO debe hacer solamente:

if (role === "Administrador")

La API debe entregar al frontend:

- Usuario autenticado.
- Grupos.
- Permisos efectivos.

El backend es la fuente definitiva de autorización.

El frontend puede ocultar botones por permisos, pero el backend siempre debe rechazar
la acción si el usuario no tiene autorización.

Crea permisos personalizados preparados para acciones futuras, por ejemplo:

repairs.view_repair
repairs.add_repair
repairs.change_repair
repairs.approve_repair
repairs.close_repair
repairs.apply_financial_charge

reports.view_operational_reports
reports.view_financial_reports
reports.export_reports

documents.view_private_document
documents.upload_document
documents.change_document
documents.archive_document

accounts.manage_users
accounts.manage_roles

Los nombres exactos pueden ajustarse a las convenciones de Django.

======================================================================
9. AUTENTICACIÓN
======================================================================

Este es un sistema web interno.

Implementa autenticación basada en sesiones de Django y cookies seguras.

No almacenes JWT ni tokens sensibles en localStorage.

Configura:

- SessionAuthentication.
- Protección CSRF.
- Cookies HttpOnly cuando corresponda.
- SameSite apropiado.
- Secure en producción.
- Expiración de sesión configurable.
- Cierre de sesión.
- Validadores de contraseña de Django.
- Bloqueo razonable o throttling para intentos repetidos de login.

Endpoints mínimos:

POST /api/v1/auth/login/
POST /api/v1/auth/logout/
GET  /api/v1/auth/me/
GET  /api/v1/auth/csrf/
GET  /api/v1/auth/permissions/

La respuesta de /me debe incluir:

- id
- username
- email
- display_name
- groups
- permissions
- is_staff
- is_superuser

No expongas información innecesaria.

En desarrollo, utiliza el proxy de Vite para:

- /api
- /admin
- rutas necesarias del backend

Así se reduce la complejidad de CORS.

Aun así, configura correctamente CSRF_TRUSTED_ORIGINS y CORS para los casos necesarios.

======================================================================
10. APLICACIONES DJANGO
======================================================================

Crea aplicaciones por dominio.

Cada aplicación debe tener una estructura consistente, por ejemplo:

apps/repairs/
├── migrations/
├── api/
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── filters.py
├── services.py
├── selectors.py
├── permissions.py
├── models.py
├── admin.py
├── apps.py
└── tests/

No es obligatorio crear archivos vacíos sin utilidad, pero mantén una separación clara.

Responsabilidades:

core
- Modelos abstractos.
- Utilidades comunes.
- Respuestas y errores.
- Health checks.
- Paginación.
- Funciones de fechas.
- Validadores comunes.

accounts
- Usuario.
- Roles.
- Permisos.
- Autenticación.
- Administración de usuarios.

audit
- Eventos de auditoría.
- Middleware o servicios de registro.
- Consulta autorizada.

catalogs
- Bancos.
- Tipos de inmueble.
- Países.
- Departamentos.
- Ciudades.
- Barrios.
- Tipos de documentos.
- Etiquetas.
- Categorías.
- Estados configurables cuando aplique.

documents
- Archivos.
- Fotografías.
- Metadatos.
- Acceso protegido.
- Previsualización.
- Descarga.
- Etiquetas.
- Validaciones.

owners
- Propietarios.
- Apoderados.
- Información bancaria.
- Debe quedar como aplicación preparada, sin inventar reglas no aprobadas.

properties
- Inmuebles.
- Inventario.
- Servicios públicos.
- Fotografías.
- Debe quedar preparada.

people
- Arrendatarios.
- Codeudores.
- Personas relacionadas.

rentals
- Alquileres.
- Contratos.
- Renovaciones.
- Estados contractuales.

payments
- Pagos.
- Recibos.
- Recaudo arrendatario.
- Recaudo propietario.

guarantors
- Afianzadoras.
- Tipos de fianza.
- Novedades de casos trasladados.

sales
- Venta de inmuebles.
- Responsables.
- Comisión.
- Documentos de venta.

repairs
- Novedades.
- Órdenes de trabajo.
- Costos.
- Evidencias.
- Responsables financieros.
- Estados de reparación.

reports
- Consultas agregadas.
- Filtros.
- Exportaciones.
- Dashboard.
- No debe duplicar información transaccional.

REGLA DE MODELADO:

No implementes de manera definitiva las reglas del negocio que todavía son contradictorias
o están pendientes de reunión.

Ejemplos pendientes:

- Día exacto de traslado a afianzadora.
- Cálculo final de mora.
- Duraciones contractuales personalizadas.
- Reglas de pagos parciales.
- Distribución de costos de arreglos.
- Flujo de aprobación de reparaciones.
- Algunos documentos obligatorios.
- Definición exacta de “pendiente por arrendar”.

Para esas reglas:

1. Crea el módulo y estructura.
2. Documenta la decisión pendiente.
3. Agrega TODO claramente rastreable.
4. No codifiques una regla falsa.
5. No bloquees la base técnica.

Crea:

docs/pending-business-decisions.md

======================================================================
11. MODELOS FUNDACIONALES SEGUROS
======================================================================

Puedes implementar completamente desde ahora los modelos fundacionales cuyo diseño no depende
de reglas de negocio dudosas.

Crea modelos abstractos como:

TimeStampedModel
- created_at
- updated_at

UserStampedModel
- created_by
- updated_by

SoftDeleteModel
- is_active o archived_at
- archived_by

Considera UUID como clave primaria para nuevas entidades.

Para facilitar una futura migración desde Access, prepara un campo opcional como:

legacy_id
legacy_source

No lo agregues indiscriminadamente a todas las tablas si no es necesario.
Puedes utilizar una mezcla mediante un modelo abstracto destinado a entidades migrables.

No realices eliminaciones físicas de:

- Documentos.
- Operaciones financieras.
- Recibos.
- Recaudos.
- Órdenes de arreglos.
- Inmuebles.
- Ventas.
- Registros con valor de auditoría.

Utiliza:

- Archivado.
- Cancelación.
- Inactivación.
- Versionado.
- Anulación.

======================================================================
12. AUDITORÍA
======================================================================

Crea un sistema base de auditoría.

Debe poder registrar como mínimo:

- Usuario.
- Acción.
- Fecha y hora.
- IP.
- User-Agent.
- Tipo de entidad.
- Identificador del registro.
- Datos anteriores, cuando sea seguro.
- Datos posteriores, cuando sea seguro.
- Ruta.
- Método HTTP.
- Resultado.

Acciones:

- CREATE
- UPDATE
- ARCHIVE
- RESTORE
- LOGIN
- LOGOUT
- DOWNLOAD
- EXPORT
- PERMISSION_CHANGE
- ROLE_CHANGE

No almacenes:

- Contraseñas.
- Tokens.
- Cookies.
- Contenido binario.
- Secretos.
- Información innecesariamente sensible.

Los eventos de auditoría no deben poder eliminarse desde la interfaz normal.

Solo el administrador puede consultarlos inicialmente.

No registres automáticamente cuerpos completos que puedan contener documentos o archivos.

======================================================================
13. DOCUMENTOS, IMÁGENES Y ARCHIVOS
======================================================================

Los archivos NO deben guardarse como binarios dentro de PostgreSQL.

PostgreSQL almacena:

- Metadatos.
- Relaciones.
- Ruta o clave del archivo.
- Nombre.
- Tipo.
- Tamaño.
- Hash.
- Usuario.
- Fechas.

El archivo físico se almacena en un almacenamiento persistente.

PRIMERA IMPLEMENTACIÓN

Utiliza la abstracción STORAGES de Django.

En desarrollo:

- Almacenamiento local.
- Carpeta persistente montada por Docker.
- Datos de prueba.

En producción inicial sobre la máquina virtual:

- Directorio persistente del host.
- Ejemplo conceptual:

  /srv/hogar-express/media

- Nunca dentro de la capa efímera del contenedor.

Usa un volumen o bind mount apropiado.

La aplicación debe quedar preparada para migrar posteriormente a:

- S3.
- Almacenamiento compatible con S3.
- Otro proveedor.

Sin reescribir la lógica de los módulos.

MODELO DOCUMENTO

Implementa un modelo reusable que contemple:

- id UUID.
- nombre visible.
- nombre original.
- archivo.
- tipo de documento.
- etiqueta.
- descripción.
- MIME type.
- extensión.
- tamaño.
- checksum SHA-256.
- fecha del documento.
- fecha de vencimiento opcional.
- obligatorio.
- usuario que lo cargó.
- fecha de carga.
- estado.
- archivado.
- relación con una entidad.

Evalúa cuidadosamente si usar ContentType / GenericForeignKey.

Si lo utilizas:

- Encapsula su uso.
- Valida tipos permitidos.
- Evita relaciones imposibles de consultar.
- Documenta las ventajas y desventajas.

Si una relación explícita es mejor, utiliza relaciones explícitas.

RUTAS DE ARCHIVOS

No uses directamente el nombre original como nombre físico.

Genera rutas seguras con UUID.

Ejemplo conceptual:

documents/{entity_type}/{year}/{month}/{uuid}.{extension}

Evita:

- Path traversal.
- Nombres duplicados.
- Caracteres inseguros.
- Sobrescrituras.

VALIDACIONES

Por defecto admite:

- application/pdf
- image/jpeg
- image/png
- image/webp, solo si ya se usa o resulta conveniente

Límite inicial configurable:

MAX_UPLOAD_SIZE_MB=10

Valida:

- Tamaño.
- Extensión.
- MIME type.
- Archivo vacío.
- Nombre.
- Relación autorizada.

No confíes solamente en la extensión.

ACCESO PRIVADO

Los documentos no deben quedar públicamente accesibles por una URL directa sin autorización.

Implementa un endpoint protegido:

GET /api/v1/documents/{id}/content/

El endpoint debe:

1. Verificar autenticación.
2. Verificar permiso.
3. Verificar que el archivo existe.
4. Registrar auditoría de acceso.
5. Entregar el archivo correctamente.

Para vista previa:

Content-Disposition: inline

Para descarga:

Content-Disposition: attachment

En desarrollo puedes utilizar FileResponse.

En producción prepara integración eficiente con Nginx mediante X-Accel-Redirect,
sin exponer el directorio de archivos públicamente.

FOTOGRAFÍAS

Cada fotografía debe poder tener:

- Etiqueta.
- Descripción.
- Orden.
- Es portada.
- Fecha.
- Usuario que cargó.
- Relación con inmueble o arreglo.

Ejemplos de etiquetas:

- Fachada.
- Sala.
- Cocina.
- Habitación.
- Baño.
- Contador.
- Daño.
- Antes.
- Durante.
- Después.

Las etiquetas deben provenir de catálogo o permitir expansión administrativa,
no de un enum imposible de modificar.

======================================================================
14. CATÁLOGOS
======================================================================

Crea una base reutilizable para catálogos administrables.

Catálogos previstos:

- Bancos.
- Países.
- Departamentos.
- Ciudades.
- Barrios.
- Tipos de inmueble.
- Tipos de documentos.
- Etiquetas de fotografías.
- Categorías de arreglos.
- Métodos de pago.
- Afianzadoras.
- Tipos de fianza.
- Tipos de servicios públicos.
- Proveedores de servicios públicos.

Cada elemento de catálogo debe contemplar:

- UUID.
- Código.
- Nombre.
- Descripción.
- Orden.
- Activo.
- Creado por.
- Actualizado por.
- Fechas.

Evita poner todo en una tabla genérica si eso elimina integridad referencial.

Puedes usar:

- Modelos específicos para catálogos estructurales.
- Un catálogo genérico solamente para opciones simples.

Documenta la decisión.

Crea datos iniciales de demostración:

- Colombia.
- Valle del Cauca.
- Cali.

Pero no cargues datos reales del cliente.

======================================================================
15. API
======================================================================

Versiona la API:

/api/v1/

Crea:

GET /api/v1/health/
GET /api/v1/ready/

health:
- Indica que el proceso responde.

ready:
- Verifica conexión con PostgreSQL.
- Verifica configuración mínima.
- No expone secretos.

Configura OpenAPI mediante drf-spectacular:

/api/schema/
/api/docs/
/api/redoc/

En producción, permite restringir la documentación a usuarios autorizados.

Configura:

- Paginación estándar.
- Filtros.
- Ordenamiento.
- Búsqueda.
- Respuestas de error consistentes.
- Validación de serializers.
- Permisos.
- Throttling básico donde aplique.

Formato de error recomendado:

{
  "code": "validation_error",
  "message": "Los datos enviados no son válidos.",
  "errors": {
    "campo": ["Mensaje de error."]
  },
  "request_id": "..."
}

Agrega un request ID por petición para facilitar diagnóstico.

No coloques lógica de negocio compleja en:

- Serializers.
- ViewSets.
- Signals.

Usa servicios y selectores:

services.py
- Cambios de estado.
- Operaciones transaccionales.
- Escritura.

selectors.py
- Consultas complejas.
- Lecturas.
- Agregaciones.

Usa transaction.atomic en operaciones que afecten varios registros.

======================================================================
16. FRONTEND
======================================================================

Construye el frontend con:

- React.
- TypeScript estricto.
- Vite.
- React Router.
- TanStack Query.
- React Hook Form.
- Zod.

No uses Create React App.

Conserva el estilo actual.

ESTRUCTURA POR FUNCIONALIDAD

Ejemplo:

src/features/repairs/
├── api/
├── components/
├── hooks/
├── pages/
├── schemas/
├── types/
└── utils/

No concentres todo en components/.

Crea layouts:

- AuthLayout.
- AppLayout.
- Sidebar.
- Header.
- MainContent.

Crea rutas protegidas.

Crea componentes reutilizables:

- Button.
- Input.
- Select.
- Textarea.
- Checkbox.
- Radio.
- DateInput.
- CurrencyInput.
- PercentageInput.
- Modal.
- Drawer.
- Table.
- Pagination.
- EmptyState.
- LoadingState.
- ErrorState.
- Badge.
- StatusBadge.
- FileUploader.
- FilePreview.
- ConfirmDialog.
- PermissionGuard.

No agregues una librería visual nueva si el proyecto ya tiene una que permite conservar
exactamente la interfaz.

Si el proyecto usa Tailwind y funciona:

- Puedes conservarlo.
- Extrae tokens.
- Evita clases repetitivas.

Si usa CSS Modules:

- Puedes conservarlos.

Si usa CSS global:

- Organízalo sin cambiar la apariencia.

La elección debe basarse en la fidelidad visual y mantenibilidad.

ESTADO DEL SERVIDOR

Usa TanStack Query para:

- Consultas.
- Cache.
- Invalidaciones.
- Estados de carga.
- Errores.
- Mutaciones.

No uses un estado global pesado sin necesidad.

AUTENTICACIÓN

Crea:

- AuthProvider o solución equivalente.
- useAuth.
- usePermissions.
- ProtectedRoute.
- PermissionGuard.

No confíes en el frontend para seguridad real.

CLIENTE HTTP

Debe:

- Usar credentials: "include".
- Gestionar CSRF.
- Centralizar errores.
- No guardar tokens en localStorage.
- Permitir cancelar solicitudes.
- Manejar 401 y 403 correctamente.

FORMULARIOS

Usa:

- React Hook Form.
- Zod.
- Mensajes en español.
- Validación de cliente y servidor.
- Errores por campo.
- Prevención de doble envío.

======================================================================
17. MIGRACIÓN DE LA INTERFAZ ACTUAL
======================================================================

Migra todas las pantallas actualmente visibles.

Para cada pantalla:

1. Identifica ruta anterior.
2. Identifica componentes.
3. Identifica acciones.
4. Identifica datos mock.
5. Crea equivalente nuevo.
6. Mantén la apariencia.
7. Migra la navegación.
8. Añade pruebas mínimas.
9. Documenta el estado.

Las acciones que todavía no tengan backend deben:

- Permanecer visualmente.
- Tener comportamiento coherente.
- Usar un servicio mock aislado solamente en desarrollo.
- No fingir persistencia real en producción.
- Mostrar claramente un estado “módulo en construcción” cuando corresponda.
- No mezclar datos mock dentro de componentes.

Ubica mocks en:

frontend/src/mocks/

Contrólalos con:

VITE_USE_MOCKS=true

En producción:

VITE_USE_MOCKS=false

Cuando VITE_USE_MOCKS=false:

- No deben cargarse datos de demostración silenciosamente.
- La aplicación debe usar la API.
- Si un endpoint no existe, mostrar un mensaje controlado.

======================================================================
18. DASHBOARD
======================================================================

Conserva el dashboard actual.

Prepara su arquitectura para indicadores como:

- Total de inmuebles.
- Inmuebles disponibles para alquiler.
- Inmuebles disponibles para venta.
- Pendientes por arrendar.
- Arrendados.
- Arreglos pendientes.
- Arreglos en progreso.
- Arreglos vencidos.
- Costos de arreglos del período.
- Pendientes de pago.
- Canon al día.
- Mora.
- Casos trasladados a afianzadora.
- Recaudo pendiente para propietarios.
- Contratos próximos a vencer.

No inventes cifras de producción.

En desarrollo puedes suministrar datos demo identificados claramente.

Crea una interfaz tipada para los indicadores.

No implementes WebSockets.
La actualización al consultar o refrescar es suficiente para la base inicial.

======================================================================
19. MÓDULO DE ARREGLOS: PREPARACIÓN TÉCNICA
======================================================================

El módulo debe quedar especialmente bien preparado.

Distingue conceptualmente:

NOVEDAD
- Reporte inicial de una situación del inmueble.

ORDEN DE ARREGLO
- Trabajo aprobado o programado para solucionar la novedad.

Flujo previsto, pendiente de validación:

Novedad
→ Revisión
→ Cotización
→ Aprobación
→ Programación
→ Ejecución
→ Evidencias
→ Aplicación financiera
→ Cierre

Estados preliminares:

- REPORTADO
- PENDIENTE_REVISION
- PENDIENTE_APROBACION
- APROBADO
- PROGRAMADO
- EN_PROGRESO
- TERMINADO
- CERRADO
- CANCELADO

No cierres estos estados como decisión inmodificable.
Documenta que requieren aprobación del cliente.

Prepara la estructura para:

- Inmueble.
- Contrato relacionado opcional.
- Título.
- Descripción.
- Categoría.
- Prioridad.
- Fecha de reporte.
- Fecha programada.
- Fecha de inicio.
- Fecha de terminación.
- Responsable interno.
- Proveedor.
- Estado.
- Observaciones.
- Ítems de costo.
- Materiales.
- Mano de obra.
- Transporte.
- Otros.
- Evidencias.
- Cotizaciones.
- Facturas.
- Cuentas de cobro.
- Soportes de pago.
- Responsable financiero.
- Estado financiero.

No implementes todavía el descuento automático final en recibos o recaudos sin validar
las reglas del cliente.

Sí puedes dejar interfaces, servicios y contratos de API preparados.

Un inmueble puede estar:

- Arrendado.
- Disponible para venta.
- Con arreglos activos.

Todo al mismo tiempo.

Por tanto, NO modeles un único campo:

destino = ALQUILER | VENTA | ARREGLO

como estado excluyente.

Los estados de:

- Alquiler.
- Venta.
- Arreglo.

deben vivir en sus procesos respectivos.

======================================================================
20. MÓDULO DE REPORTES: PREPARACIÓN TÉCNICA
======================================================================

El módulo reports no debe almacenar copias de datos transaccionales.

Debe consumir:

- Selectores.
- Consultas agregadas.
- Vistas SQL solamente si son justificadas.
- Endpoints filtrables.

Prepara contratos para reportes como:

- Propietarios.
- Inmuebles.
- Estado general de inmuebles.
- Alquileres.
- Pagos.
- Pendientes.
- Mora.
- Afianzadora.
- Contratos próximos a vencer.
- Recaudo propietario.
- Ventas.
- Arreglos por inmueble.
- Costos de arreglos.
- Insumos.
- Materiales.
- Mano de obra.
- Arreglos pendientes de aplicación financiera.

Cada reporte debe poder definir:

- Nombre.
- Descripción.
- Permiso requerido.
- Filtros.
- Columnas.
- Orden.
- Totales.
- Exportación.

No implementes exportadores enormes todavía si no hay requisitos finales.

Deja preparada una interfaz de exportación para:

- CSV.
- Excel.
- PDF.

La generación real puede implementarse por fases.

Crea filtros reutilizables para:

- Rango de fechas.
- Propietario.
- Inmueble.
- Barrio.
- Estado.
- Responsable.
- Proveedor.
- Categoría.

======================================================================
21. DOCKER PARA DESARROLLO
======================================================================

Crea:

compose.yaml
compose.dev.yaml
compose.prod.yaml

compose.yaml debe contener la base común.

DESARROLLO

Servicios mínimos:

db
backend
frontend

DB

- PostgreSQL 17.
- Volumen persistente.
- Healthcheck con pg_isready.
- Usuario, contraseña y base desde variables.
- Puerto configurable.
- No incluir datos reales.

BACKEND

- Dockerfile para desarrollo.
- Montaje del código.
- Espera saludable de PostgreSQL.
- Ejecuta migraciones de manera controlada.
- Inicia servidor Django en:
  0.0.0.0:8000
- Healthcheck HTTP.

FRONTEND

- Node 24.
- Montaje del código.
- Volumen separado para node_modules si es necesario.
- Vite en:
  0.0.0.0:5173
- HMR funcional dentro de Docker.
- Proxy hacia backend.

DEPENDENCIAS ENTRE SERVICIOS

Usa healthchecks reales.
No dependas únicamente de sleeps fijos.

Evita ciclos de reinicio infinitos.

PERSISTENCIA

Crea volúmenes separados para:

- postgres_data
- media_data
- static_data, si aplica

No almacenes datos persistentes únicamente dentro del contenedor.

COMANDO OBJETIVO

El equipo debe poder ejecutar:

docker compose -f compose.yaml -f compose.dev.yaml up --build

o un comando aún más sencillo documentado.

Después de iniciar:

Frontend:
http://localhost:5173

Backend:
http://localhost:8000

Admin:
http://localhost:8000/admin/

API docs:
http://localhost:8000/api/docs/

======================================================================
22. DOCKER PARA PRODUCCIÓN
======================================================================

Crea una configuración de producción funcional, aunque todavía no se despliegue.

Servicios:

- db, permitiendo posteriormente sustituirlo por PostgreSQL externo.
- backend con Gunicorn.
- frontend compilado.
- nginx.

Usa builds multi-stage.

BACKEND DE PRODUCCIÓN

- No usar runserver.
- Gunicorn.
- Usuario no root.
- collectstatic.
- Migraciones mediante comando explícito o entrypoint controlado.
- Configuración production.py.
- DEBUG=false.
- Cookies seguras.
- Hosts permitidos por entorno.
- Logs a stdout/stderr.
- Healthcheck.

FRONTEND DE PRODUCCIÓN

- Build con npm ci.
- npm run build.
- Servido por Nginx.
- No incluir dependencias de desarrollo en imagen final.

NGINX

Debe:

- Servir frontend.
- Redirigir rutas SPA a index.html.
- Enviar /api/ al backend.
- Enviar /admin/ al backend.
- Servir /static/ adecuadamente.
- Gestionar archivos privados mediante ruta interna, no pública.
- Configurar límites de carga coherentes.
- Incluir headers de seguridad razonables.
- Permitir configuración posterior de HTTPS.

No incluyas certificados falsos.

Documenta despliegue detrás de:

- Nginx con Let's Encrypt.
- Proxy existente de la VM.
- Balanceador, si posteriormente se utiliza.

======================================================================
23. SCRIPTS
======================================================================

Crea scripts para Linux/macOS y Windows PowerShell.

bootstrap

Debe:

1. Verificar Docker.
2. Verificar Docker Compose.
3. Crear .env desde .env.example si no existe.
4. No sobrescribir un .env existente.
5. Construir servicios.
6. Levantar PostgreSQL.
7. Ejecutar migraciones.
8. Crear roles.
9. Crear usuario demo o administrador solo si variables lo permiten.
10. Cargar datos demo si está habilitado.
11. Levantar frontend y backend.
12. Mostrar URLs.

Comandos:

scripts/bootstrap.sh
scripts/bootstrap.ps1

dev

- Levanta entorno.
- Muestra logs útiles.

test

- Ejecuta backend.
- Ejecuta frontend.
- Ejecuta lint.
- Ejecuta comprobaciones.

backup

Debe permitir:

- pg_dump comprimido.
- Copia o archivo comprimido de media.
- Timestamp.
- Directorio configurable.
- No almacenar contraseña en el script.

restore

Debe:

- Requerir confirmación explícita.
- Restaurar dump.
- Documentar riesgos.
- No ejecutarse accidentalmente.

======================================================================
24. BACKUPS
======================================================================

Prepara scripts y documentación para respaldar:

1. PostgreSQL.
2. Archivos media.
3. Configuraciones no secretas.

No basta con respaldar PostgreSQL.

Estructura conceptual de producción:

/srv/hogar-express/
├── postgres/
├── media/
├── backups/
└── logs/

No asumas que esta ruta existe durante desarrollo.
Hazla configurable.

Documenta estrategia sugerida:

- Backup diario.
- Retención.
- Copia externa a la VM.
- Verificación de restauración.
- Cifrado del respaldo externo.

No implementes un cron destructivo automáticamente.
Incluye ejemplos para configurar cron o systemd timers.

======================================================================
25. DATOS DE DEMOSTRACIÓN
======================================================================

No utilices la base real del cliente.

Crea un comando:

python manage.py seed_demo

Debe ser idempotente o permitir limpiar únicamente sus propios datos demo.

Crea:

- Usuarios demo.
- Roles.
- Catálogos mínimos.
- Datos completamente ficticios.
- Cero cédulas reales.
- Cero cuentas reales.
- Cero documentos reales.

Credenciales demo:

- Deben provenir de variables.
- No deben quedar con contraseñas públicas en producción.
- ENABLE_DEMO_DATA=false por defecto en producción.

======================================================================
26. DJANGO ADMIN
======================================================================

Configura Django Admin como herramienta de soporte interno, no como interfaz principal.

Registra:

- Usuarios.
- Grupos.
- Catálogos.
- Documentos.
- Auditoría, solo lectura.
- Modelos fundacionales.

Personaliza:

- Nombre del sitio.
- Títulos.
- Búsquedas.
- Filtros.
- Campos readonly.
- Permisos.

No expongas archivos privados sin control.

No permitas eliminar eventos de auditoría desde admin.

======================================================================
27. CALIDAD DE CÓDIGO
======================================================================

BACKEND

Configura Ruff para:

- Formato.
- Imports.
- Reglas razonables.
- Exclusión de migraciones generadas cuando corresponda.

Configura pytest.

Pruebas mínimas:

- Health endpoint.
- Ready endpoint.
- Login correcto.
- Login incorrecto.
- Logout.
- /me.
- Usuario no autenticado.
- Permisos por rol.
- Seed de roles idempotente.
- Acceso protegido a documento.
- Rechazo de tipo de archivo inválido.
- Rechazo de archivo demasiado grande.
- Auditoría básica.

FRONTEND

Configura:

- ESLint.
- Prettier.
- TypeScript strict.
- Vitest.
- React Testing Library.

Pruebas mínimas:

- Render de login.
- Protección de ruta.
- Render de layout.
- Menú según permisos.
- Selector demo oculto cuando está deshabilitado.
- Manejo de 401.
- Estado de carga.
- Estado de error.
- Componente de subida de archivos.

No busques 100% de cobertura artificial.

Define un umbral razonable para el código fundacional.

======================================================================
28. INTEGRACIÓN CONTINUA
======================================================================

Si el repositorio usa GitHub, crea:

.github/workflows/ci.yml

Debe:

1. Ejecutarse en pull requests.
2. Instalar dependencias.
3. Levantar PostgreSQL de prueba.
4. Ejecutar migraciones.
5. Ejecutar:
   - Django checks.
   - Ruff.
   - Pytest.
   - TypeScript check.
   - ESLint.
   - Vitest.
   - Build del frontend.
6. No requerir secretos reales.
7. Usar datos de prueba.

Si el repositorio no está en GitHub, conserva el workflow y documenta que es opcional.

======================================================================
29. DOCUMENTACIÓN OBLIGATORIA
======================================================================

Crea o actualiza:

README.md

Debe incluir:

- Qué es Hogar Express.
- Stack.
- Requisitos.
- Inicio rápido.
- Docker.
- Desarrollo.
- Producción.
- Variables de entorno.
- Migraciones.
- Usuarios demo.
- Pruebas.
- Lint.
- Backups.
- Restauración.
- Estructura.
- Solución de problemas frecuentes.

CONTRIBUTING.md

Debe incluir:

- Flujo Git.
- Nombres de ramas.
- Commits.
- Migraciones.
- Pruebas.
- Pull requests.
- No modificar migraciones ya compartidas.
- Cómo agregar una app.
- Cómo agregar un endpoint.
- Cómo agregar una pantalla.
- Cómo agregar permisos.
- Cómo agregar catálogos.

docs/architecture.md

- Diagrama textual.
- Backend.
- Frontend.
- PostgreSQL.
- Docker.
- Archivos.
- Seguridad.
- Flujo de solicitudes.

docs/legacy-audit.md

- Análisis del proyecto anterior.

docs/design-system.md

- Diseño visual detectado.

docs/ui-migration.md

- Mapeo de pantallas.

docs/permissions.md

- Matriz de roles y permisos.

docs/file-storage.md

- Almacenamiento.
- Acceso.
- Backups.
- Migración futura a S3.

docs/pending-business-decisions.md

- Reglas pendientes.

docs/dependency-versions.md

- Todas las versiones efectivamente instaladas.

docs/development-workflow.md

- Cómo trabaja cada integrante.

docs/deployment-vm.md

- Despliegue en VM.
- Directorios persistentes.
- Nginx.
- Variables.
- Backups.
- Actualizaciones.
- Rollback.

======================================================================
30. VARIABLES DE ENTORNO
======================================================================

Crea un .env.example completo.

Ejemplo conceptual, ajustando nombres según implementación:

COMPOSE_PROJECT_NAME=hogar_express

POSTGRES_DB=hogar_express
POSTGRES_USER=hogar_express
POSTGRES_PASSWORD=change_me
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_EXPOSED_PORT=5432

DJANGO_SETTINGS_MODULE=config.settings.development
DJANGO_SECRET_KEY=change_me
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,backend
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://localhost:8000
DJANGO_LOG_LEVEL=INFO

DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.test
DJANGO_SUPERUSER_PASSWORD=change_me

FRONTEND_URL=http://localhost:5173
CORS_ALLOWED_ORIGINS=http://localhost:5173

MAX_UPLOAD_SIZE_MB=10
ENABLE_DEMO_DATA=true
ENABLE_ROLE_SIMULATOR=true

VITE_API_BASE_URL=/api/v1
VITE_USE_MOCKS=false
VITE_ENABLE_ROLE_SIMULATOR=true

No uses exactamente estos valores en producción.
Agrega comentarios claros.

Valida al arrancar que las variables críticas existan.

======================================================================
31. LOGS Y OBSERVABILIDAD
======================================================================

Configura logs estructurados o, como mínimo, consistentes.

Incluye:

- Timestamp.
- Nivel.
- Logger.
- Request ID.
- Mensaje.
- Usuario cuando sea seguro.

No registres:

- Contraseñas.
- Cookies.
- Tokens.
- Archivos.
- Información bancaria completa.
- Datos personales completos sin necesidad.

En producción, envía logs a stdout/stderr para que Docker pueda gestionarlos.

Agrega un manejo global de errores que:

- No muestre trazas al usuario en producción.
- Registre el error con request ID.
- Devuelva mensaje controlado.

======================================================================
32. SEGURIDAD
======================================================================

Aplica:

- CSRF.
- Sesiones seguras.
- Hash de contraseñas.
- Password validators.
- HTTPS preparado.
- Secure cookies en producción.
- HttpOnly donde corresponda.
- SameSite.
- X-Content-Type-Options.
- Referrer-Policy.
- X-Frame-Options.
- HSTS en producción cuando HTTPS esté confirmado.
- Límites de carga.
- Validación de archivos.
- Permisos backend.
- No exposición de media.
- No secretos en Git.
- No DEBUG en producción.

Ejecuta:

python manage.py check
python manage.py check --deploy --settings=config.settings.production

Documenta cualquier advertencia que solo pueda resolverse durante el despliegue,
por ejemplo dominio o certificado HTTPS.

No desactives CSRF para “hacer que funcione”.

No uses @csrf_exempt indiscriminadamente.

======================================================================
33. COMANDOS DE ACEPTACIÓN
======================================================================

Antes de considerar terminada la tarea, ejecuta realmente un flujo limpio.

PRUEBA DESDE CERO

1. Detén los contenedores.
2. Elimina únicamente los volúmenes de desarrollo creados para esta prueba, si es seguro.
3. Reconstruye.
4. Levanta servicios.
5. Ejecuta migraciones.
6. Ejecuta seed_roles.
7. Ejecuta seed_demo si está habilitado.
8. Comprueba backend.
9. Comprueba frontend.
10. Comprueba login.
11. Comprueba PostgreSQL.
12. Comprueba subida de un archivo ficticio.
13. Comprueba acceso protegido.
14. Comprueba selector demo.
15. Ejecuta pruebas.
16. Ejecuta build de producción.

Comandos esperados, adaptados si es necesario:

docker compose -f compose.yaml -f compose.dev.yaml config

docker compose -f compose.yaml -f compose.dev.yaml build

docker compose -f compose.yaml -f compose.dev.yaml up -d

docker compose exec backend python manage.py migrate

docker compose exec backend python manage.py seed_roles

docker compose exec backend python manage.py check

docker compose exec backend pytest

docker compose exec frontend npm run lint

docker compose exec frontend npm run typecheck

docker compose exec frontend npm run test -- --run

docker compose exec frontend npm run build

docker compose -f compose.yaml -f compose.prod.yaml config

No declares éxito si alguno falla.

Si un comando falla:

1. Lee el error.
2. Corrígelo.
3. Repite el comando.
4. Continúa hasta que pase.

======================================================================
34. CRITERIOS DE ACEPTACIÓN
======================================================================

La tarea solamente está completa si:

[ ] El repositorio anterior fue analizado.
[ ] Los cambios anteriores no fueron destruidos.
[ ] El logo original se conserva exactamente.
[ ] La interfaz mantiene los colores y diseño.
[ ] Las rutas actuales siguen visibles o están mapeadas.
[ ] Django arranca.
[ ] PostgreSQL conecta.
[ ] React arranca.
[ ] Docker Compose arranca todo.
[ ] Las migraciones funcionan desde una base vacía.
[ ] Existe usuario personalizado.
[ ] Existen cuatro roles iniciales.
[ ] seed_roles es idempotente.
[ ] Login funciona.
[ ] Logout funciona.
[ ] /me funciona.
[ ] Permisos funcionan.
[ ] El selector demo solo aparece en desarrollo.
[ ] Existe API versionada.
[ ] Existe documentación OpenAPI.
[ ] Los archivos se almacenan fuera de PostgreSQL.
[ ] Los archivos persisten al recrear contenedores.
[ ] Los archivos privados requieren permiso.
[ ] Existe auditoría base.
[ ] Existen apps por dominio.
[ ] Arreglos está preparado.
[ ] Reportes está preparado.
[ ] No se inventaron reglas contradictorias.
[ ] Existe .env.example.
[ ] No hay secretos en Git.
[ ] Existen configuraciones development, test y production.
[ ] Existen Dockerfiles.
[ ] Existen archivos Compose.
[ ] Existe Nginx de producción.
[ ] Existen scripts de bootstrap.
[ ] Existen scripts de backup.
[ ] Existen pruebas.
[ ] El frontend compila.
[ ] El backend pasa checks.
[ ] README permite iniciar desde cero.
[ ] La documentación explica la arquitectura.
[ ] La configuración de producción pasa check --deploy o documenta únicamente
    advertencias dependientes del dominio/HTTPS.
[ ] No quedan errores conocidos ocultos.

======================================================================
35. FORMA DE TRABAJO DURANTE LA TAREA
======================================================================

Trabaja por fases:

FASE 1
- Auditoría.
- Protección.
- Documentación del legado.

FASE 2
- Estructura.
- Docker.
- PostgreSQL.
- Django.
- React.

FASE 3
- Diseño visual.
- Migración de interfaz.

FASE 4
- Autenticación.
- Roles.
- Permisos.
- Auditoría.

FASE 5
- Documentos.
- Catálogos.
- Apps de dominio.

FASE 6
- Pruebas.
- Producción.
- Documentación.

Después de cada fase:

1. Ejecuta validaciones relevantes.
2. Corrige errores.
3. Haz un commit claro si el entorno lo permite.

Commits sugeridos:

chore: audit legacy project
chore: add docker development environment
feat: initialize django backend
feat: initialize react frontend
feat: add authentication and role permissions
feat: add private document storage foundation
refactor: migrate legacy interface
test: add foundation test suites
docs: add architecture and development guides

No hagas un único commit gigante si puedes evitarlo.

======================================================================
36. RESTRICCIONES
======================================================================

NO:

- Borres el repositorio sin respaldo.
- Cambies el logo.
- Cambies la paleta.
- Inventes datos del cliente.
- Uses la base real.
- Expongas archivos públicamente.
- Guardes archivos binarios en PostgreSQL.
- Uses SQLite como solución principal.
- Guardes JWT en localStorage.
- Desactives CSRF.
- Uses “latest” en imágenes Docker.
- Uses float para dinero.
- Codifiques los cuatro roles como única lógica de permisos.
- Mezcles toda la aplicación en una sola app Django.
- Introduzcas microservicios.
- Introduzcas Kubernetes.
- Introduzcas Redis o Celery sin necesidad.
- Construyas una plataforma pública para propietarios o arrendatarios.
- Implementes reglas contradictorias como si estuvieran aprobadas.
- Simules éxito sin ejecutar los comandos.
- Dejes comentarios “TODO” genéricos sin explicar la decisión pendiente.
- Termines con archivos sin formatear.
- Dejes imports rotos.
- Dejes migraciones pendientes.
- Dejes dependencias sin bloquear.

======================================================================
37. ENTREGA FINAL
======================================================================

Al terminar, responde con un informe estructurado:

1. RESUMEN EJECUTIVO
   - Qué se cambió.
   - Estado final.

2. AUDITORÍA DEL PROYECTO ANTERIOR
   - Stack.
   - Elementos reutilizados.
   - Elementos reemplazados.

3. ARQUITECTURA NUEVA
   - Backend.
   - Frontend.
   - Base de datos.
   - Docker.
   - Archivos.

4. INTERFAZ
   - Pantallas migradas.
   - Fidelidad visual.
   - Diferencias justificadas.

5. SEGURIDAD
   - Autenticación.
   - Permisos.
   - Documentos.
   - Auditoría.

6. COMANDOS PARA EL EQUIPO
   - Inicio rápido.
   - Apagado.
   - Logs.
   - Migraciones.
   - Pruebas.
   - Crear usuario.
   - Backup.

7. VERSIONES EXACTAS
   - Python.
   - Django.
   - DRF.
   - PostgreSQL.
   - Node.
   - React.
   - Vite.
   - Dependencias relevantes.

8. PRUEBAS EJECUTADAS
   - Comando.
   - Resultado.
   - Número de pruebas.

9. URLS LOCALES
   - Frontend.
   - Backend.
   - Admin.
   - API Docs.

10. CREDENCIALES DEMO
    - Solo si fueron generadas mediante variables de desarrollo.
    - Advertencia para no usarlas en producción.

11. DECISIONES PENDIENTES
    - Reglas del negocio que deben confirmarse con el cliente.

12. ESTADO DE GIT
    - Rama.
    - Commits.
    - Archivos modificados.
    - Cambios no confirmados, si existen.

13. PROBLEMAS RESTANTES
    - No ocultes errores.
    - Distingue bloqueadores de tareas futuras.

14. CONFIRMACIÓN FINAL
    Confirma expresamente si una persona nueva puede:

    - Clonar el repositorio.
    - Copiar .env.example.
    - Ejecutar el bootstrap.
    - Levantar frontend, backend y PostgreSQL.
    - Iniciar sesión.
    - Ver la interfaz existente.
    - Comenzar a desarrollar su módulo.

COMIENZA AHORA CON LA AUDITORÍA DEL REPOSITORIO Y DESPUÉS EJECUTA TODAS LAS FASES.
NO TE LIMITES A PROPONER ARCHIVOS: CRÉALOS, CONFIGÚRALOS, EJECÚTALOS Y VERIFÍCALOS.