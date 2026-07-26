Como te comentamos, tuvimos la reunión con el cliente. Esta fue la parte de reparaciones y reportes que realizamos. Creo que me corresponde a mí y debo de hacer yo. Entonces quiero ahí, yo hice las anotaciones, o sea, yo primero le mostré un documento con un poco de preguntas y cosas así. Pero entonces yo iba anotando lo que él me iba diciendo, porque la verdad, al parecer ellos no tenían, por así decirlo, algo claro ya. Sí, que, o sea, por ejemplo, para la parte de reparaciones, ellos no implementado nada. Entonces, apenas estaban empezando la idea. Y, por ejemplo, tú me diste como un modelo recomendado. Yo les mostré ese y les gustó, lo resolvimos y por ahí dejamos plasmado, por ahí plasmado pues. Entonces eso, para que revises todo eso, los reportes que, que nos iban a mandar algún reporte de ejemplo. Y pues ellos quieren otros nuevos que pues ahí lo anoté. Entonces para tener en cuenta también. ¿Qué otra cosa así? Ya, revisa el documento, alguna duda o alguna cosa me dices, para hacer esta parte que me corresponde a mí nomás, que sería pues, te digo, reparaciones y reportes. Es lo que me interesa hacer por el momento. El doc se llama DOC reparaciones y reportes, Sí, ya revisé completo el documento. **La reunión sirvió bastante:** para Reparaciones ya existe un flujo suficientemente claro para empezar a diseñar e implementar el módulo. En Reportes también se identificaron las necesidades principales, pero todavía faltan definiciones sobre formatos, permisos, columnas exactas y conservación histórica. 

# 1. Reparaciones: cómo quedó entendido el proceso

El flujo aprobado conceptualmente sería:

```text
Novedad
→ Revisión
→ Cotización
→ Aprobación
→ Programación
→ Ejecución
→ Registro de costos y evidencias
→ Distribución financiera
→ Verificación
→ Cierre
```

La **secretaria** registra y administra el proceso operativo. Un usuario con permisos superiores aprueba la ejecución y posteriormente valida que el trabajo haya terminado correctamente.

## Estados definidos

```text
REPORTADA
EN_REVISION
PENDIENTE_COTIZACION
PENDIENTE_APROBACION
APROBADA
PROGRAMADA
EN_PROGRESO
TERMINADA
CERRADA
CANCELADA
```

La diferencia importante es:

* **Terminada:** el trabajo físico fue ejecutado.
* **Cerrada:** el trabajo fue verificado, se cargaron soportes, se distribuyeron los costos y no quedan movimientos pendientes.
* **Cancelada:** debe exigir una razón obligatoria.

Esto está bien diseñado y permite controlar el proceso completo.

# 2. Entidades que realmente necesita Reparaciones

Para evitar una tabla gigante, yo lo dividiría así.

## Novedad

Es el reporte inicial de un problema:

```text
- inmueble
- descripción
- fecha del reporte
- prioridad
- persona que informó
- usuario que registró
- estado
- observaciones
```

Ejemplo:

> Se reporta una filtración en el baño principal.

## Orden de reparación

Es el trabajo que se decide realizar:

```text
- novedad relacionada
- inmueble
- título
- descripción
- responsable interno
- fecha programada
- fecha de inicio
- fecha de terminación
- estado
- observaciones
```

Una novedad podría cerrarse sin reparación o podría generar una o varias órdenes. Esta separación sigue siendo recomendable.

## Proveedores o maestros

La reunión confirmó que deben registrar:

* Maestros.
* Ferreterías.
* Proveedores de materiales.
* Personas o empresas que cotizan.

Campos recomendados:

```text
- tipo: persona o empresa
- nombre o razón social
- identificación
- teléfono
- correo
- especialidad
- dirección
- información bancaria
- observaciones
- activo
```

Un proveedor no se elimina si deja de trabajar con la inmobiliaria; se marca como inactivo.

## Cotizaciones

Una reparación puede tener varias cotizaciones:

```text
Orden de reparación
├── Cotización del proveedor A
├── Cotización del proveedor B
└── Cotización del proveedor C
```

Cada cotización debería contener:

```text
- proveedor
- fecha
- vigencia
- valor de materiales
- valor de mano de obra
- otros costos
- garantía ofrecida
- documento adjunto
- estado
- seleccionada o no seleccionada
```

Los estados pueden ser:

```text
BORRADOR
PRESENTADA
SELECCIONADA
RECHAZADA
INACTIVA
```

Cuando el documento dice que una cotización se puede “deshabilitar”, **no debe eliminarse**. Se marca como inactiva o rechazada y permanece en el historial.

## Ítems de cotización

```text
- descripción
- tipo: material, mano de obra u otro
- cantidad
- valor unitario
- valor total
- activo
```

Esto permite añadir imprevistos o trabajos extras sin borrar el presupuesto inicial.

Ejemplo:

```text
Cotización original                   $500.000
Trabajo adicional autorizado          $120.000
Total actualizado                     $620.000
```

Debe conservarse quién agregó el extra, cuándo se agregó y quién lo aprobó.

# 3. Aprobaciones

La reunión confirmó dos aprobaciones importantes:

1. La reparación debe ser aprobada antes de ejecutarse.
2. Al marcarla como terminada, un usuario superior verifica el resultado.

Yo almacenaría cada aprobación como un registro independiente:

```text
- tipo de aprobación
- usuario que aprobó
- fecha y hora
- observación
- documento o evidencia opcional
```

Tipos:

```text
APROBACION_COTIZACION
APROBACION_EJECUCION
APROBACION_TRABAJO_TERMINADO
APROBACION_CIERRE
```

No conviene guardar solamente:

```text
aprobado = true
```

porque se perdería quién aprobó y bajo qué condiciones.

Tampoco fijaría en código el nombre “superusuario”. Lo correcto es utilizar un permiso:

```text
repairs.approve_repair
repairs.verify_repair
repairs.close_repair
```

Así el administrador puede asignar esos permisos a uno o varios roles.

# 4. Costos y pagos

La reunión confirmó que deben conservarse por separado:

* Valor cotizado.
* Valor finalmente ejecutado.
* Materiales.
* Mano de obra.
* Imprevistos.
* Pagos parciales al maestro o proveedor.
* Distribución del costo entre propietario y arrendatario. 

## Costos reales

Después de realizar el trabajo se registran los costos finales:

```text
- concepto
- tipo: material, mano de obra, transporte u otro
- cantidad
- valor unitario
- valor total
- proveedor
- factura o soporte
```

No se debe reemplazar el valor cotizado con el valor final. Deben conservarse ambos para poder generar el reporte:

```text
Valor cotizado:     $500.000
Valor final:        $565.000
Diferencia:          $65.000
```

## Pagos al proveedor

Como se aprobaron pagos parciales, se necesita:

```text
- proveedor
- reparación
- fecha
- valor
- método de pago
- soporte
- observación
```

Y un resumen:

```text
Total de reparación:     $800.000
Pagado al proveedor:     $500.000
Pendiente:                $300.000
```

La reparación no debería cerrarse financieramente mientras existan pagos pendientes, salvo que un usuario autorizado haga una excepción documentada.

# 5. Distribución del costo

Este es uno de los puntos más importantes.

La reunión confirmó que una reparación puede cobrarse a:

* Propietario.
* Arrendatario.
* Ambos.

Por tanto, no sirve un solo campo como:

```text
responsable = PROPIETARIO
```

Debe existir una distribución:

| Responsable  |    Valor |
| ------------ | -------: |
| Propietario  | $400.000 |
| Arrendatario | $150.000 |
| Total        | $550.000 |

Puede manejarse por valor o porcentaje, pero recomiendo guardar el **valor final en pesos**, aunque la interfaz permita calcularlo usando porcentajes.

## Cuando paga el propietario

El costo se descuenta del dinero proveniente del canon y puede dividirse en una o varias cuotas:

```text
Reparación: $600.000

Julio:       $200.000
Agosto:      $200.000
Septiembre:  $200.000
```

Se necesita una programación:

```text
- propietario
- reparación
- período
- valor
- estado
- recaudo donde se aplicó
```

Estados:

```text
PENDIENTE
APLICADA
PAGADA
CANCELADA
```

## Cuando paga el arrendatario

El documento indica que debe quedar en cartera y generarse un recibo. Entonces debe generarse una obligación:

```text
- arrendatario
- reparación
- concepto
- valor
- fecha límite
- saldo
- estado
```

Y posteriormente:

```text
PENDIENTE
PAGO_PARCIAL
PAGADO
ANULADO
```

## Cuando pagan ambos

Se crean dos distribuciones independientes:

```text
Propietario → descuento en uno o varios recaudos
Arrendatario → cuenta por cobrar y recibo
```

Eso evita mezclar sus movimientos.

# 6. Evidencias, garantía y cierre

Se confirmó que deben guardar:

* Fotografías de antes.
* Fotografías de después.
* Cotizaciones.
* Facturas.
* Cuentas de cobro.
* Soportes de pago.
* Documentos relacionados.
* Imágenes o videos de verificación.

También se indicó que la garantía debe aparecer en el documento entregado al maestro o trabajador. 

Yo guardaría:

```text
- duración de garantía
- unidad: días, meses o años
- fecha de inicio
- fecha de vencimiento
- condiciones
- proveedor responsable
```

La orden solo debería pasar a `CERRADA` cuando:

1. Está terminada.
2. Fue verificada por un usuario autorizado.
3. Tiene las evidencias requeridas.
4. La distribución financiera está definida.
5. Se registró la garantía, si aplica.
6. No quedan documentos obligatorios pendientes.
7. Se registró una observación final.

# 7. Comentarios e historial

El cliente pidió un apartado de comentarios y observaciones. Recomiendo que no sea solo un campo de texto que se sobrescribe.

Debe ser un historial:

```text
15/07 - Secretaria:
El propietario solicita una segunda cotización.

16/07 - Administrador:
Se aprueba la propuesta del proveedor B.

20/07 - Secretaria:
El proveedor informa un daño adicional en la tubería.
```

Cada comentario debe guardar:

* Usuario.
* Fecha.
* Texto.
* Archivo opcional.
* Visibilidad o tipo, si más adelante se necesita.

Además, todos los cambios de estado deben quedar en otro historial:

```text
REPORTADA → EN_REVISION
EN_REVISION → PENDIENTE_COTIZACION
PENDIENTE_COTIZACION → PENDIENTE_APROBACION
```

# 8. Dudas que todavía veo en Reparaciones

Aunque ya se puede desarrollar bastante, quedaron estos puntos ambiguos:

## 1. Documento para el maestro

En las notas aparece:

> “Genera recibo a la persona que va a ejecutar el trabajo”.

Hay que definir si se refieren a:

* Orden de trabajo.
* Comprobante de pago.
* Cuenta de cobro.
* Recibo de caja.
* Documento de aceptación de condiciones y garantía.

No son el mismo documento.

## 2. Porcentaje para la inmobiliaria

Aparece:

> “Recibo que se entrega a la persona que asume el costo — porcentaje para inmobiliaria”.

No quedó definido:

* Qué porcentaje es.
* Sobre qué valor se calcula.
* Quién lo paga.
* Si siempre aplica.
* Si es comisión, administración o utilidad.

**No implementes ese cálculo todavía** hasta aclararlo.

## 3. Reparaciones sin cotización

No quedó explícito si una reparación pequeña puede pasar directamente de revisión a aprobación.

Yo permitiría dos rutas:

```text
Con cotización:
EN_REVISION → PENDIENTE_COTIZACION

Sin cotización:
EN_REVISION → PENDIENTE_APROBACION
```

Pero debería confirmarse.

## 4. Revisiones periódicas

La respuesta sobre gas y contadores no resolvió si son:

* Reparaciones.
* Mantenimientos preventivos.
* Eventos programados.

Mi recomendación sigue siendo manejar una categoría:

```text
CORRECTIVO
PREVENTIVO
REVISION_PERIODICA
```

Y permitir una fecha futura o recurrencia.

# 9. Reportes: qué quedó confirmado

El cliente quiere reportes en seis grupos principales. 

## Propietarios

* Propietario y sus inmuebles.
* Estado de los inmuebles.
* Información financiera por inmueble.
* Información financiera consolidada.
* Reporte mensual, anual y por rango personalizado.

## Reparaciones

* Por reparación.
* Por estado.
* Por proveedor.
* Por propietario o “cliente”.
* Por fecha reportada.
* Por fecha terminada.
* Comparación de costos.
* Materiales y mano de obra.

Aquí debes confirmar qué significa exactamente “por cliente”: probablemente propietario, pero podría referirse al arrendatario.

## Ventas

* Por estado.
* En venta.
* Vendidos.
* Pendientes.
* En proceso.
* Por valor.
* Por propietario.
* Por vendedor.

## Inmuebles

* Por uno o varios inmuebles.
* Inventario.
* Arrendado.
* Disponible.
* En venta.
* En reparación.
* Pausado o pendiente.

## Alquileres

* Pendientes de arrendar.
* En mora.
* Reportados a afianzadora.
* Al día.
* Desocupados.
* En reparación.
* Retirados.
* Próximos a vencer.
* Con incumplimientos.
* No renovación.

## Reporte administrativo general

Para usuarios con permisos superiores:

* Inmuebles alquilados.
* Canon esperado.
* Dinero recaudado.
* Dinero pendiente.
* Fecha de pago.
* Observaciones.
* Inmuebles en mora.
* Totales mensuales.

# 10. Cómo construir el módulo de Reportes

Yo no crearía una tabla diferente por cada reporte. La aplicación `reports` debe ejecutar consultas sobre los módulos existentes.

Cada reporte debe definirse con esta ficha:

```text
Nombre:
Objetivo:
Usuarios autorizados:
Fuente de datos:
Filtros:
Columnas:
Agrupaciones:
Totales:
Campo de fecha:
Formato de exportación:
```

Ejemplo:

```text
Nombre:
Reparaciones por proveedor

Filtros:
- Proveedor
- Estado
- Fecha reportada
- Fecha terminada
- Inmueble
- Propietario

Columnas:
- Número de reparación
- Inmueble
- Proveedor
- Estado
- Valor cotizado
- Valor final
- Fecha reportada
- Fecha terminada

Totales:
- Número de reparaciones
- Total cotizado
- Total ejecutado
- Diferencia
```

## Fechas

La reunión confirmó que para reparaciones deben aparecer principalmente:

* Fecha en la que se reportó.
* Fecha en la que terminó.

Sin embargo, otros reportes sí pueden requerir:

* Fecha de creación.
* Fecha de pago.
* Período del canon.
* Fecha de cierre.
* Fecha de ejecución.
* Fecha de traslado a afianzadora.
* Fecha de terminación del contrato.

Por eso el filtro no debe ser simplemente “fecha”. Debe indicar qué fecha se está filtrando.

# 11. Dashboard mensual

El cliente pidió indicadores mensuales de:

```text
- Fechas próximas a vencer
- Inmuebles pendientes por arrendar
- Ventas
- Reparaciones
```

Y definió “pendiente por arrendar” como:

> Inmueble desocupado, pero listo para ser arrendado.

Eso debería convertirse en una regla clara:

```text
No tiene contrato de alquiler activo
AND está habilitado para alquiler
AND no tiene bloqueo que impida arrendarlo
```

Debería diferenciarse de:

* Desocupado en reparación.
* Desocupado pausado.
* Retirado.
* Disponible para venta únicamente.

# 12. Exportación: punto pendiente

La reunión dejó “PDF o Word”. Yo cuestionaría el uso de Word.

Para reportes tabulares recomiendo:

* **Excel o CSV:** análisis, filtros y manipulación.
* **PDF:** impresión y entrega formal.
* **Word:** documentos narrativos o plantillas editables.

Un reporte financiero grande en Word suele ser incómodo. Antes de desarrollarlo, confirma si realmente quieren Word o si querían decir Excel.

# 13. Históricos y permanencia de información

En el documento aparece:

> “Un año de permanencia de información”.

Esto es demasiado ambiguo y no recomiendo interpretarlo como eliminar los datos después de un año.

Podría significar:

1. Guardar el archivo PDF generado durante un año.
2. Permitir consultar reportes de un año.
3. Mantener datos detallados un año.
4. Mantener versiones anteriores por un año.

Mi recomendación:

* Los movimientos transaccionales no se eliminan.
* Los pagos, reparaciones, contratos y recaudos permanecen como historial.
* Los reportes se recalculan usando la información actual.
* Los archivos exportados pueden conservarse durante un período configurable.
* Si se necesita que un reporte conserve exactamente cómo se veía al generarse, se almacena una copia o snapshot.

Esto debe aclararse antes de implementar cualquier eliminación automática.

# 14. Permisos y auditoría

Quedó confirmado:

* El usuario de Consulta debe visualizar primero.
* Las descargas de reportes deben registrarse.

La parte “visualizar antes” todavía puede significar dos cosas:

* Consulta solo puede visualizar, pero nunca exportar.
* Consulta puede previsualizar y luego exportar.

Mientras se aclara, implementaría permisos separados:

```text
reports.view_report
reports.export_report
reports.view_financial_report
```

Y auditoría de:

```text
- usuario
- reporte
- filtros usados
- formato
- fecha y hora
- cantidad de registros
```

# 15. Qué puedes empezar a implementar desde ya

## Primera etapa de Reparaciones

1. Proveedores.
2. Novedades.
3. Órdenes de reparación.
4. Estados e historial.
5. Comentarios.
6. Cotizaciones.
7. Ítems de cotización.
8. Aprobaciones.
9. Evidencias.
10. Costos reales.
11. Pagos parciales al proveedor.
12. Garantías.
13. Distribución entre propietario y arrendatario.
14. Programación en cuotas.
15. Historial completo.

## Primera etapa de Reportes

Empieza con cuatro reportes que dependen principalmente de tu módulo:

1. Reparaciones por estado.
2. Reparaciones por inmueble.
3. Reparaciones por proveedor.
4. Comparativo cotizado contra ejecutado.

Después:

5. Costos por propietario.
6. Reparaciones pendientes de cobro.
7. Reparaciones pendientes de descontar al propietario.
8. Pagos pendientes a proveedores.
9. Garantías próximas a vencer.
10. Materiales y mano de obra.

Los reportes generales de alquileres, ventas y propietarios dependerán de que tus compañeros definan y desarrollen correctamente esos módulos.

# 16. Lo que debes coordinar con tus compañeros

Pídeles que te confirmen los nombres y relaciones definitivas de:

```text
Propietario
Inmueble
Arrendatario
Contrato
Canon o período de recaudo
Recibo
Pago
Recaudo del propietario
Venta
Usuario
```

Para Reportes, acuerden que los estados no se escriban como textos libres. Deben compartir catálogos o constantes claras:

```text
ACTIVO
PENDIENTE
PAGADO
EN_MORA
REPORTADO
FINALIZADO
```

También debes pedirles que no cambien modelos o nombres de campos sin comunicarlo, porque tus consultas dependerán de ellos.

# 17. Mi conclusión

**Reparaciones está lo suficientemente definido para comenzar.** Las únicas partes que no cerraría todavía son:

* Porcentaje o comisión de la inmobiliaria.
* Nombre y contenido de algunos recibos/documentos.
* Ruta para reparaciones sin cotización.
* Manejo final de revisiones periódicas.

**Reportes está definido a nivel de necesidades, pero no todavía a nivel de diseño final.** Para cada reporte todavía deben precisar:

* Columnas.
* Totales.
* Agrupaciones.
* Permisos.
* PDF, Excel o Word.
* Diseño de la plantilla.
* Comportamiento histórico.

La sección de infraestructura quedó sin respuestas en el documento, por lo que todavía no se puede cerrar la estrategia definitiva de almacenamiento, backups, acceso y despliegue. Conviene mantenerla formalmente como pendiente del proyecto. 


Ya tengo el IDE con el proyecto cargado, todo entendido, todo, está toda la base, con base de datos, Postgres, el Docker bien, todo bien, todo funcionando, está la base. Ahora debo hacer lo que te digo, que es básicamente todo esto, todo lo que te corresponde, que es, se llama reparaciones y reportes. Me gustaría ir primero con reparaciones, por ende, no sé, o sea, cómo le puedo decir a la gente de IEX está en el IDE para eso. Anteriormente tú me hiciste un mensaje larguísimo, que la verdad creo que estaba bueno, solo que como ya acabó el plan Plus, no creo que me pueda hacer un mensaje predefinido. O sea, no importa cuántas palabras, entre más completo, que mejor. Para yo pasarle al IDE que tenga el contexto bueno y ayudarme a hacer todo el tema de reparaciones bien hecho.
Sí. De hecho, en este punto no le pediría que "haga Reparaciones". Le pediría que primero diseñe la arquitectura del módulo y luego la implemente. Esa diferencia hace que el resultado sea muchísimo mejor.

Yo dividiría el trabajo en fases:

Analizar el proyecto actual.
Diseñar el módulo.
Crear los modelos.
Crear la API.
Crear el frontend.
Integrarlo con el resto.

Así la IA no empieza a generar código sin pensar.

Prompt para Antigravity IDE

Puedes copiar prácticamente esto (yo incluso le agregaría que no empiece a escribir código hasta terminar el análisis).

CONTEXTO

Actualmente estás trabajando sobre un proyecto que YA EXISTE.

No debes crear un proyecto nuevo.

Ya existe:

Backend Django
Django REST Framework
PostgreSQL
Docker
Docker Compose
Variables de entorno
Frontend React + TypeScript
Sistema de autenticación
Roles y permisos
Base de datos funcionando
Arquitectura modular

Antes de hacer cualquier modificación debes analizar completamente el proyecto.

Quiero que entiendas la arquitectura antes de escribir código.

No rompas la estructura existente.

No crees modelos duplicados.

No cambies la arquitectura.

No modifiques módulos existentes si no es estrictamente necesario.

Si necesitas modificar algo existente primero explícalo.

Siempre reutiliza el código existente.

TU OBJETIVO

Voy a desarrollar únicamente el módulo llamado

REPARACIONES

Este módulo será completamente interno.

No existen usuarios externos.

No existen propietarios entrando al sistema.

No existen arrendatarios entrando al sistema.

Todo será utilizado únicamente por empleados de la inmobiliaria.

Los permisos ya los maneja Django.

PRIMER PASO (NO ESCRIBIR CÓDIGO)

Primero analiza completamente el proyecto.

Necesito que revises:

estructura del backend
estructura del frontend
modelos existentes
autenticación
permisos
usuarios
arquitectura REST
convenciones del proyecto
serializers
routers
vistas
componentes React
estructura de carpetas
diseño existente

Después explícame:

Cómo está organizado el proyecto.

Dónde debería vivir el módulo Reparaciones.

Qué modelos existentes debo reutilizar.

Qué relaciones ya existen.

Qué debo crear.

Qué debo evitar duplicar.

NO escribas código todavía.

ARQUITECTURA DEL MÓDULO

Después del análisis quiero diseñar el módulo.

No quiero escribir modelos inmediatamente.

Quiero diseñarlo.

Ayúdame a construir una arquitectura limpia.

El módulo debe poder crecer durante muchos años.

Debe seguir principios SOLID.

Debe ser modular.

Debe ser desacoplado.

Debe ser fácilmente testeable.

Debe respetar la arquitectura existente.

CONCEPTO DEL NEGOCIO

Una reparación NO comienza directamente.

Primero existe una NOVEDAD.

Ejemplo

"El baño presenta una filtración."

Una novedad puede:

cerrarse sin reparación

generar una reparación

generar varias reparaciones

Después aparece una

ORDEN DE REPARACIÓN

La orden representa el trabajo que realmente se ejecutará.

Ejemplo

"Cambiar tubería del baño."

No quiero mezclar novedades con reparaciones.

Quiero entidades separadas.

FLUJO

El flujo aprobado por el cliente es

REPORTADA

↓

EN REVISIÓN

↓

PENDIENTE COTIZACIÓN

↓

PENDIENTE APROBACIÓN

↓

APROBADA

↓

PROGRAMADA

↓

EN PROGRESO

↓

TERMINADA

↓

CERRADA

o

CANCELADA

La IA debe respetar exactamente este flujo.

No inventar estados nuevos.

MODELOS ESPERADOS

Espero algo parecido a:

RepairIssue (Novedad)

RepairOrder

RepairQuotation

RepairQuotationItem

RepairCost

RepairSupplier

RepairPayment

RepairEvidence

RepairApproval

RepairComment

RepairHistory

NO significa que esos nombres sean definitivos.

Primero analiza si el proyecto ya tiene modelos parecidos.

PROVEEDORES

Debe existir un catálogo.

Pueden ser

Personas

Empresas

Ferreterías

Maestros

Contratistas

Plomeros

Electricistas

etc.

No deben eliminarse.

Solo activarse o desactivarse.

COTIZACIONES

Una reparación puede tener muchas cotizaciones.

Cada cotización puede tener muchos ítems.

Debe poder marcarse una como seleccionada.

Las demás permanecen históricamente.

Nunca eliminar.

COSTOS

No mezclar

valor cotizado

con

valor ejecutado.

Ambos deben existir.

También deben existir

materiales

mano de obra

transporte

otros

Todo debe poder auditarse.

PAGOS

Una reparación puede pagarse parcialmente.

Debe existir historial.

Debe quedar saldo pendiente.

RESPONSABLE FINANCIERO

Una reparación puede ser asumida por

propietario

arrendatario

ambos

La distribución debe ser flexible.

Nunca usar un único campo.

Debe existir una entidad de distribución.

EVIDENCIAS

Cada reparación puede almacenar

fotografías

videos

facturas

cuentas de cobro

PDF

cotizaciones

soportes

documentos

No guardar archivos dentro de PostgreSQL.

Solo la referencia.

GARANTÍA

La garantía debe quedar registrada.

Debe permitir

fecha

duración

unidad

observaciones

proveedor

COMENTARIOS

No quiero un simple TextField.

Quiero historial.

Cada comentario debe guardar

usuario

fecha

hora

texto

archivo opcional

HISTORIAL

Todo cambio importante debe quedar registrado.

Estados

Aprobaciones

Ediciones

Cambios importantes

Nunca perder historial.

APROBACIONES

Las aprobaciones NO deben guardarse como un boolean.

Debe existir historial.

Quién aprobó.

Cuándo.

Observaciones.

Tipo de aprobación.

AUDITORÍA

Quiero aprovechar el sistema de auditoría existente.

Si el proyecto ya posee auditoría reutilízala.

No crear otra.

ARCHIVOS

No almacenar binarios en PostgreSQL.

Solo almacenar rutas.

El almacenamiento físico será administrado por el cliente.

Nosotros solo administramos referencias.

API

Quiero una API REST limpia.

Debe seguir exactamente el estilo existente del proyecto.

No romper convenciones.

No cambiar nombres.

FRONTEND

No quiero un diseño nuevo.

Debe reutilizar:

colores

tipografía

cards

botones

componentes

layout

sidebar

header

formularios

tablas

modales

Todo debe verse como parte natural del sistema.

EXPERIENCIA DE USUARIO

No quiero formularios enormes.

Prefiero wizard.

Paso 1

Información básica

Paso 2

Cotizaciones

Paso 3

Programación

Paso 4

Costos

Paso 5

Documentos

Paso 6

Resumen

TABLAS

Todas las tablas deben permitir

buscar

filtrar

ordenar

paginación

estado

acciones

FILTROS

Estado

Proveedor

Inmueble

Propietario

Responsable

Fecha

Prioridad

DETALLE

Cada reparación debe tener una vista de detalle.

Con pestañas.

Resumen

Historial

Cotizaciones

Costos

Documentos

Comentarios

Pagos

Garantía

Auditoría

CÓDIGO

No quiero archivos gigantes.

No quiero clases enormes.

No quiero lógica duplicada.

No quiero funciones de 500 líneas.

Prefiero servicios pequeños.

Responsabilidad única.

Código limpio.

IMPORTANTE

No empieces a escribir código inmediatamente.

Primero analiza completamente el proyecto.

Después proponme la arquitectura.

Después discutimos si la arquitectura tiene sentido.

Una vez aprobada la arquitectura, recién comenzamos a implementar.

Cada decisión debe justificarse técnicamente.

Nunca supongas relaciones si puedes reutilizar modelos existentes.

Siempre prioriza mantenibilidad, escalabilidad y claridad del dominio.

Una recomendación adicional

Yo haría una pequeña mejora al plan. No le pidas que implemente todo el módulo de una vez. Pídele que lo haga por milestones (hitos). Por ejemplo:

Milestone 1: análisis de la arquitectura y diseño del dominio.
Milestone 2: modelos, migraciones y relaciones.
Milestone 3: API REST (serializers, views, permisos y rutas).
Milestone 4: interfaz React (listados, formularios y detalle).
Milestone 5: carga de documentos, historial, auditoría y pruebas.

Con ese enfoque, la IA puede revisar cada etapa antes de pasar a la siguiente, lo que reduce mucho la probabilidad de tener que rehacer partes importantes del módulo.