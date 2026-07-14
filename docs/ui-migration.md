# Migración de la Interfaz Visual

## Tabla de Equivalencias de Pantallas

| Pantalla anterior (MVP) | Componente nuevo (TypeScript) | Estado | Diferencias |
|-------------------|------------------|--------|-------------|
| Dashboard | `features/dashboard/Dashboard.tsx` | Migrada | Separado en módulo independiente, usa Tailwind CSS y tipado estricto |
| Propietarios | `features/owners/Propietarios.tsx` | Migrada | Implementada con formulario de creación |
| Inmuebles | `features/properties/Inmuebles.tsx` | Migrada | Listado con tarjetas e imagen responsive |
| Alquiler | `features/rentals/Alquiler.tsx` | Migrada | Preparada para conexión con endpoints de contratos |
| Venta | `features/sales/Venta.tsx` | Migrada | Visualización del estado del inmueble |
| Arreglos | `features/repairs/Arreglos.tsx` | Migrada | Preparado flujo de novedades |
| Reportes | `features/reports/Reportes.tsx` | Migrada | Selección dinámica de reporte y exportación |
| Configuración | `features/settings/Configuracion.tsx` | Migrada | Parámetros administrables de afianzadoras |
