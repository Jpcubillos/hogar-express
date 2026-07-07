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
5. Migrar `Recaudo Arrendatario`, `Historial de pagos`, `Interes por mora` y `Recaudo propietario` con reglas de dominio.
6. Agregar API real, autenticacion, roles, auditoria y documentos.

## Correcciones del cliente para el MVP

Estas reglas reemplazan decisiones anteriores del documento inicial.

### Navegacion y lenguaje

- `Contratos` debe mostrarse como `Recaudo Arrendatario`.
- `Nuevo contrato` debe mostrarse como `Nuevo alquiler`.
- `Recibos y pagos` debe mostrarse como `Historial de pagos`.
- `Liquidacion` debe mostrarse como `Recaudo propietario`.
- `Recargo diario` debe mostrarse como `Interes por mora`.

### Inmuebles

Un inmueble puede estar simultaneamente disponible para alquiler, disponible
para venta y en reparacion. No debe modelarse con un destino unico excluyente.
Usar flags o estados independientes:

- `available_for_rent`
- `available_for_sale`
- `under_repair`
- `sold`

El preaviso pertenece al alquiler, no al inmueble. Los tipos de inmueble,
ubicaciones, bancos, proveedores de servicios, etiquetas de fotos y porcentajes
de administracion deben ser catalogos administrables, no listas quemadas.

### Venta

La ficha de venta debe usar rango de precios:

- `min_sale_price`
- `max_sale_price`
- `suggested_sale_price`
- `final_sale_price`

La comision esperada se calcula como rango:

- `expected_commission_min = min_sale_price * commission_percentage / 100`
- `expected_commission_max = max_sale_price * commission_percentage / 100`
- `final_commission_value = final_sale_price * commission_percentage / 100`

Antes de crear una venta, el inmueble debe existir, tener propietario, estar
disponible para venta, tener precio minimo y maximo validos, comision y
responsable. Antes de completar una venta deben existir los documentos
obligatorios: contrato de mandato, certificado de tradicion, megaobras y
facturas de servicios publicos al dia.

### Recaudo arrendatario

La mora ahora funciona asi:

- Dia 1 al 5: pago sin interes por mora.
- Dia 6 al 30: pago con interes por mora.
- Despues del dia 30: reportado o con afianzadora.

Si un alquiler inicia despues del dia 15, el sistema debe permitir elegir entre
generar solo recibo por dias o recibo por dias mas mes siguiente. No debe
generarlo automaticamente sin decision del usuario.

### Recibos e historial de pagos

Un recibo de arrendatario solo se puede generar despues de registrar el pago.
Debe permitir ajustes multiples con concepto, valor, tipo, nota, soporte y una
marca para indicar si debe tenerse presente para el propietario. Los cambios
posteriores del recibo deben guardarse con historial de modificaciones.

### Recaudo propietario

La liquidacion al propietario debe considerar canon pagado, administracion,
afianzadora, arreglos, descuentos y ajustes marcados para el propietario. Debe
permitir recibos de caja para propietarios asociados a propietario, inmueble,
recibo principal o liquidacion.

## Servicios de backend objetivo

La logica critica debe vivir en backend. El frontend solo debe mostrar datos,
formularios, filtros, estados y PDFs generados.

- `SalesService`
- `SaleDocumentService`
- `SaleStatusService`
- `CommissionService`
- `RentCollectionService`
- `PaymentHistoryService`
- `TenantReceiptService`
- `OwnerCollectionService`
- `OwnerCashReceiptService`
- `SettlementService`
- `LateInterestService`
- `PdfService`
- `AuditService`
- `CatalogService`
- `PropertyDocumentService`
