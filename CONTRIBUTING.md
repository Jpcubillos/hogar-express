# Guía de Contribución: Hogar Express

Esta guía explica el flujo de trabajo y las normas para contribuir al desarrollo del software Hogar Express.

## 1. Ramas y Commits

- Utilizar el prefijo de rama según la intención:
  - `feat/nombre-modulo` para nuevas características.
  - `fix/nombre-bug` para correcciones de errores.
  - `chore/tarea-mantenimiento` para cambios en dependencias o Docker.
- Commits atómicos y descriptivos. Ejemplo:
  `feat: add private document storage foundation`

## 2. Desarrollo Backend (Django)

- Todas las apps deben crearse bajo `backend/apps/`.
- No mezclar lógica de negocio directamente en los serializadores o vistas; usar servicios en `services.py` o selectores en `selectors.py` si son consultas complejas.
- Utilizar `Decimal` para dinero. Nunca float.
- Registrar eventos de auditoría mediante middleware o llamadas explícitas a `AuditEvent.objects.create`.

## 3. Desarrollo Frontend (React)

- Estructura basada en dominios (`features/repairs/`, etc.).
- Utilizar componentes de interfaz genéricos en `shared/ui` en vez de clases CSS ad-hoc.
- Manejar llamadas asíncronas con TanStack Query para el almacenamiento en caché e invalidación de estados.

## 4. Agregar Nuevos Permisos o Catálogos

1. Modificar el comando `seed_roles` en `backend/apps/accounts/management/commands/seed_roles.py`.
2. Agregar el código o nombre del permiso/grupo.
3. Ejecutar:
   ```bash
   docker compose exec backend python manage.py seed_roles
   ```
