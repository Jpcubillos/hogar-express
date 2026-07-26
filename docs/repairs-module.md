# 🏛️ Documentación Técnica: Módulo de Reparaciones & Mantenimiento

El módulo de **Reparaciones y Mantenimiento** gestiona el ciclo de vida completo de reportes de novedades, cotizaciones de proveedores, autorizaciones, ejecución física, distribución financiera de costos y garantías para la inmobiliaria.

---

## 1. Arquitectura del Dominio (Domain-Driven Design)

El módulo se encuentra desacoplado y utiliza a **`RepairOrder` como Aggregate Root**. Ninguna entidad interna (cotizaciones, tareas, costos, aprobaciones o eventos) puede ser mutada o manipulada fuera del límite del agregado.

### Entidades Principales

*   **`RepairIncident`**: Novedad o reporte inicial del problema presentado en un inmueble (`REPORTED`, `IN_REVIEW`, `CONVERTED`, `DISMISSED`, `CLOSED`).
*   **`RepairOrder` (Aggregate Root)**: Representa la orden de trabajo. Mantiene el estado estricto, la prioridad (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`), severidad, tipo de reparación y el cálculo automático del reloj de SLA (`is_overdue`).
*   **`RepairTask`**: Sub-actividades desglosadas con secuencia ordenada (`sequence_order`), proveedor asignado, costo estimado y costo real.
*   **`RepairQuote` y `RepairQuoteItem`**: Propuestas presentadas por contratistas/proveedores con desglose de ítems (materiales, mano de obra, transporte).
*   **`RepairCost`**: Registro inmutable de costos clasificados como `ESTIMATED` (inicial), `QUOTED` (presupuestado) o `ACTUAL` (ejecutado real).
*   **`RepairApproval`**: Registro formal de decisiones de autorización por administración, propietario, gerencia o contabilidad.
*   **`RepairCostAllocation` y `RepairAllocationInstallment`**: Esquema de distribución del costo (Propietario / Arrendatario / Inmobiliaria) desglosado en cuotas mensuales.
*   **`RepairWarranty`**: Control de vencimientos y términos de garantía del trabajo realizado.
*   **`RepairComment`**: Registro de observaciones internas con adjuntos opcionales y soporte de `@menciones`.
*   **`RepairTimelineEvent`**: Event Stream cronológico inmutable (estilo GitHub) con codificación de colores para trazabilidad visual.

---

## 2. Máquina de Estados (`RepairStateMachine`)

Toda transición de estado es validada estrictamente por `RepairStateMachine` para garantizar las invariantes del negocio:

```
[REPORTED] ───> [IN_REVIEW] ───┬───> [PENDING_QUOTE] ───> [PENDING_APPROVAL]
                                │                                │
                                └───> [PENDING_APPROVAL] <───────┘
                                                │
                                                ▼
                                           [APPROVED]
                                                │
                                                ▼
                                           [SCHEDULED]
                                                │
                                                ▼
                                         [IN_PROGRESS]
                                                │
                                                ▼
                                           [COMPLETED]
                                                │
                                                ▼
                                            [CLOSED]

*(Cualquier estado previo a CLOSED puede cambiar a CANCELLED requiriendo motivo obligatorio)*
```

### Invariantes Destacadas
1. **Cancelación**: Exige parámetro de texto obligatorio con la justificación.
2. **Aprobación**: Requiere que la cotización seleccionada esté en estado `SELECTED` y que exista un registro de `RepairApproval`.
3. **Terminación**: Requiere que todas las `RepairTask` estén en estado `COMPLETED` o `CANCELLED`.
4. **Cierre**: Requiere estado previo `COMPLETED`, notas de verificación e imagen de soporte posterior (`PHOTO_AFTER`).

---

## 3. Capa de Servicio Atómica (`RepairService`)

Todas las operaciones que mutan el dominio se ejecutan de forma atómica con `@transaction.atomic` y registran automáticamente el historial de estados y el `RepairTimelineEvent`:

*   `RepairService.change_status(repair_order, new_status, user, reason)`
*   `RepairService.update_priority(repair_order, new_priority, user)`
*   `RepairService.select_quote(quote, user)`
*   `RepairService.add_comment(repair_order, text, document, user, is_internal)`

---

## 4. Contratos de Integración con el Ecosistema

El módulo de Reparaciones ofrece métodos desacoplados y endpoints REST específicos para ser consumidos libremente por los demás módulos cuando se desarrollen:

### 🏠 1. Módulo de Inmuebles (`Properties`)
*   **Método:** `RepairService.get_property_repairs_summary(property_id)`
*   **Endpoint:** `GET /api/v1/repairs/orders/by-property/?property_id=UUID`
*   **Retorna:** Resumen de reparaciones activas, pendientes, cerradas, fecha de última reparación, próxima visita programada, costos acumulados y garantías activas.

### 👤 2. Módulo de Propietarios (`Owners`)
*   **Método:** `RepairService.get_owner_repairs_summary(owner_id)`
*   **Endpoint:** `GET /api/v1/repairs/orders/by-owner/?owner_id=UUID`
*   **Retorna:** Historial de reparaciones por propietario, costos acumulados, cobros pendientes, valor descontado en liquidaciones y garantías vigentes.

### 📄 3. Módulo de Alquileres (`Rentals`)
*   **Método:** `RepairService.get_rental_repairs_summary(rental_id)`
*   **Endpoint:** `GET /api/v1/repairs/orders/by-rental/?rental_id=UUID`
*   **Retorna:** Reparaciones asociadas al contrato, cargos al arrendatario, descuentos al canon del propietario e indicador de reparaciones críticas bloqueantes.

### 🏷️ 4. Módulo de Ventas (`Sales`)
*   **Método:** `RepairService.get_sales_repairs_summary(property_id)`
*   **Endpoint:** `GET /api/v1/repairs/orders/by-sales-property/?property_id=UUID`
*   **Retorna:** Historial de reparaciones, trabajos de mantenimiento preventivo (mejoras realizas) y total acumulado invertido en el inmueble en comercialización.

### 📊 5. Dashboard General (`Dashboard`)
*   **Método:** `RepairService.get_dashboard_widgets_data()`
*   **Endpoint:** `GET /api/v1/repairs/orders/dashboard-widgets/`
*   **Retorna:** Agregación estadística por estado, prioridad, categoría, proveedor, porcentaje de cumplimiento de SLA y promedios de costos.

---

## 5. Endpoints REST API

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/v1/repairs/incidents/` | Listar y filtrar novedades iniciales. |
| `GET` | `/api/v1/repairs/orders/` | Listar órdenes de trabajo (con `select_related` y `prefetch_related`). |
| `POST` | `/api/v1/repairs/orders/` | Crear nueva orden de trabajo. |
| `POST` | `/api/v1/repairs/orders/{id}/change-status/` | Cambiar estado atómicamente vía State Machine. |
| `POST` | `/api/v1/repairs/orders/{id}/update-priority/` | Actualizar prioridad y recalcular reloj SLA. |
| `POST` | `/api/v1/repairs/quotes/{id}/select/` | Seleccionar cotización ganadora. |
| `GET` | `/api/v1/repairs/orders/dashboard-summary/` | Obtener KPIs financieros y de SLA. |
| `GET` | `/api/v1/repairs/orders/by-property/` | Contrato de integración para Inmuebles. |
| `GET` | `/api/v1/repairs/orders/by-owner/` | Contrato de integración para Propietarios. |
| `GET` | `/api/v1/repairs/orders/by-rental/` | Contrato de integración para Alquileres. |
| `GET` | `/api/v1/repairs/orders/by-sales-property/` | Contrato de integración para Ventas. |
| `GET` | `/api/v1/repairs/orders/dashboard-widgets/` | Contrato de integración para Dashboard General. |
