# Arquitectura Base

El MVP visual existente se mantiene activo mientras se migra por partes hacia
una estructura modular. La regla principal es no mezclar UI, reglas de negocio
y persistencia en el mismo archivo.

## Capas

- `src/app`: composicion de la aplicacion, providers y registro de modulos.
- `src/features`: pantallas y flujos por modulo funcional.
- `src/domain`: conceptos del negocio, estados, invariantes y reglas puras.
- `src/infrastructure`: adaptadores para API, storage, documentos y mocks.
- `src/shared`: componentes, utilidades y configuracion reutilizable.

## Estado actual

`src/App.jsx` conserva el MVP entregado por el companero. `src/app/App.jsx`
lo envuelve para que la nueva entrada de la aplicacion ya exista sin romper la
demo. La migracion recomendada es mover un modulo a la vez desde el MVP hacia
`src/features`.

## Orden recomendado de migracion

1. Extraer datos mock a repositorios de `src/infrastructure`.
2. Extraer componentes genericos a `src/shared/ui`.
3. Migrar `Dashboard` como primer modulo real.
4. Migrar `Propietarios` e `Inmuebles`, porque son entidades base.
5. Migrar `Contratos`, `Pagos`, `Mora` y `Liquidaciones` con reglas de dominio.
6. Agregar API real, autenticacion, roles, auditoria y documentos.
