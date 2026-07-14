# Legacy Audit: Hogar Express

This document records the state, structure, and configurations of the legacy codebase prior to the architectural migration.

- **Legacy Commit Identifier:** `1db39d4` ("Initial Hogar Expres MVP")
- **Date of Audit:** 2026-07-13

## 1. Technical Stack (Legacy)

- **Language:** JavaScript (ES6+)
- **Frontend Framework:** React 19.2.7 (Client-side single-page app)
- **Bundler:** Vite 8.1.0
- **Router:** Client-side state variable (`pagina`) in `App.jsx`
- **Styling:** Inline CSS and Global CSS (`App.css`, `index.css`)
- **State Management:** React local state (`useState`, `useMemo`)
- **Backend:** None. All data is mock/static in client code.

## 2. File Structure (Legacy)

```
hogar-express/
├── docs/
│   └── ARCHITECTURE.md
├── src/
│   ├── app/
│   │   ├── providers/
│   │   └── routing/
│   ├── features/ (dashboard, leasing, owners, payments, etc.)
│   ├── domain/
│   ├── infrastructure/
│   ├── shared/
│   ├── App.css
│   ├── App.jsx (Primary implementation containing all mock data & UI)
│   ├── index.css
│   └── main.jsx
├── eslint.config.js
├── index.html
├── package.json
├── package-lock.json
└── vite.config.js
```

## 3. Detected Modules & Routes

Rutas simuladas por el estado `pagina`:
1. `dashboard` (Resumen general, KPIs, alertas, accesos rápidos)
2. `propietarios` (Listado y vista a detalle de propietarios)
3. `inmuebles` (Listado, filtros por estado, fotos y detalles)
4. `alquiler` (Contratos, simulador de prorrateo/recargos, liquidaciones)
5. `venta` (Fichas de venta y comisiones)
6. `arreglos` (Órdenes de trabajo de reparación y mantenimiento)
7. `reportes` (Visualización e indicadores operativos)
8. `configuracion` (Ajustes de tasas financieras y afianzadoras)

## 4. Components & Layouts

- **Sidebar:** Left navigation pane (width 232px) in `App.jsx`.
- **UI Primitives:** Cards, Buttons, Badges, Modals, Forms written as inline components in `App.jsx` without generic abstractions.
- **Logo:** Embedded SVG `LogoMark` and `LogoFull` inline.

## 5. Migration Risks & Issues

- **Risk of Regression:** The legacy codebase has all modules in a single file `src/App.jsx`. Splitting them requires careful routing setup and type safety without breaking visual continuity.
- **Access to Files:** File upload is simulated. The new system must handle real multipart uploads to a protected REST endpoint.
- **Prorate & Recargo Calculations:** Pinned inline formulas (`1.76%` daily penalty) must be mapped to configurable backend properties.
