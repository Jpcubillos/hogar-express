# Modelo de dominio de Hogar Express

Este documento resume el esquema fundacional implementado en Django. PostgreSQL es la fuente transaccional; los reportes y el dashboard consultan estos datos y no mantienen copias paralelas.

## Convenciones

- UUID para todas las entidades de negocio.
- Dinero y porcentajes con `Decimal`.
- Marcas de creación, actualización y usuario responsable.
- Archivado lógico para maestros y registros operativos.
- Estados, anulaciones y versiones para documentos financieros.
- `legacy_id` y `legacy_source` para la futura migración desde Microsoft Access.
- Relaciones financieras protegidas contra eliminación en cascada.

## Aplicaciones

- `accounts`: usuarios, grupos y permisos.
- `audit`: trazabilidad de acciones y cambios.
- `configuration`: organización, sedes, consecutivos y políticas versionadas.
- `catalogs`: geografía y catálogos administrables.
- `people`: personas naturales, jurídicas, contactos, direcciones y proveedores.
- `owners`: propietarios, cuentas bancarias, instrucciones de pago y apoderados.
- `properties`: inmuebles, copropiedad, oferta de arriendo, pisos, servicios e inventarios.
- `documents`: archivos privados, documentos, versiones, asociaciones, fotografías y requisitos.
- `rentals`: alquileres, contratos, participantes, renovaciones, ajustes, notas y terminaciones.
- `payments`: períodos, cartera, ajustes, pagos, aplicaciones, recibos, recaudo propietario y fondos.
- `guarantors`: coberturas, casos y novedades de afianzadora.
- `repairs`: novedades, órdenes, cotizaciones, aprobaciones, costos, distribución, pagos y garantías.
- `sales`: publicaciones, interesados, ofertas, transacciones, asesores y comisiones.
- `reports`: definiciones, ejecuciones exportables y alertas operativas.

## Reglas deliberadamente configurables

La tasa de mora, el prorrateo, el traslado a afianzadora, el porcentaje de administración y la retención documental tienen modelos con vigencia y versión. No se codificaron valores no aprobados como reglas definitivas.

## Servicios transaccionales

Los archivos `services.py` implementan las operaciones que requieren bloquear varias filas o validar agregados:

- Consecutivos sin colisiones.
- Distribución de propiedad al 100%.
- Activación de contratos sin solapamientos.
- Aplicación de pagos sin exceder saldos.
- Generación de recibos versionados.
- Recalculo de recaudo propietario.
- Distribución completa de costos de reparación y cuotas.

Estas operaciones deben invocarse desde serializers o casos de uso; no deben replicarse en React.

## Superficie API inicial

Los recursos CRUD protegidos por sesión y permisos Django están disponibles bajo `/api/v1/`. Esto incluye personas,
propietarios, inmuebles, inventarios, arriendos, cartera, garantías, reparaciones, ventas, reportes, catálogos y configuración.
La administración segura de usuarios está en `/api/v1/auth/users/`. Los recibos y las demás operaciones que requieren una
transacción de negocio deben emitirse mediante los servicios correspondientes, no mediante escrituras directas desde React.

## Reinicio de la base fundacional

El esquema inicial fue consolidado antes de tener datos productivos. Una base local creada con la migración anterior debe recrearse una sola vez. Los clones nuevos utilizan directamente las migraciones actuales mediante `scripts/bootstrap.ps1` o `scripts/bootstrap.sh`.
