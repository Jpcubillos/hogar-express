# Sistema visual de Hogar Express

Este documento define la identidad visual aplicada al frontend administrativo. Toda pantalla nueva debe reutilizar estos tokens y componentes para conservar una experiencia coherente.

## Identidad

El logo oficial está almacenado en `frontend/public/hogar-express-logo.png`. Debe mostrarse sobre superficies blancas, sin redibujarlo, deformarlo ni cambiar sus colores.

La interfaz combina el azul profundo de la marca, que comunica confianza y orden, con el mostaza del logo como acento para estados activos y llamados de atención. El color mostaza no debe usarse en grandes superficies de contenido.

## Paleta

| Token | Valor | Uso |
|---|---|---|
| `mostaza` | `#E4AA18` | Navegación activa y acentos de marca |
| `mostazaOscuro` | `#A87308` | Texto de advertencia |
| `mostazaClaro` | `#FFF6DA` | Fondos de advertencia |
| `azul` | `#2D6FAF` | Acciones primarias, enlaces y foco |
| `azulOscuro` | `#102F49` | Navegación y superficies institucionales |
| `azulProfundo` | `#0B2236` | Fondos de alto contraste |
| `azulClaro` | `#EAF3FB` | Estados informativos |
| `carbon` | `#1D2935` | Texto principal |
| `carbonSuave` | `#687887` | Texto secundario |
| `verde` | `#3E7B55` | Estados correctos o vigentes |
| `verdeClaro` | `#EAF6EE` | Fondo de éxito |
| `rojo` | `#B9473B` | Error, mora y prioridad alta |
| `rojoClaro` | `#FCEDEA` | Fondo de error |
| `fondo` | `#F4F7F9` | Área de trabajo |
| `superficie` | `#FFFFFF` | Tarjetas, tablas y modales |
| `borde` | `#DDE5EA` | Separadores y contornos |

Los valores fuente están en `frontend/src/styles/colors.ts` y las variables CSS en `frontend/src/index.css`.

## Tipografía

- Fuente principal: `Segoe UI Variable`, `Aptos`, `Segoe UI`, `Inter` o la fuente sans-serif del sistema.
- Títulos: peso entre 750 y 800, espaciado ligeramente cerrado.
- Texto de interfaz: entre 12 y 14 px según jerarquía.
- Etiquetas de sección: mayúsculas, peso 800 y espaciado amplio.
- Cifras importantes: peso 800 y espaciado cerrado.

No se depende de fuentes remotas, de modo que la interfaz conserva su apariencia en instalaciones sin acceso a internet.

## Superficies y dimensiones

- Sidebar de escritorio: `264px`.
- Barra superior: `74px`; en móvil `66px`.
- Contenido principal: máximo `1600px` y padding de `36px` en escritorio.
- Tarjetas: radio de `17px`, borde sutil y sombra de baja elevación.
- Botones: radio de `11px`, altura de `42px` en tamaño normal.
- Campos: altura mínima de `42px` y anillo de foco azul.
- Modales: radio de `21px`, fondo desenfocado y altura máxima del `88vh`.

## Movimiento

- Botones: elevación de 2 px al pasar el cursor y compresión breve al presionar.
- Tarjetas interactivas: elevación de 3 px y aumento suave de sombra.
- Navegación: desplazamiento horizontal de 2 px en hover.
- Modales: entrada corta con opacidad y desplazamiento vertical.
- Duración habitual: entre 150 y 300 ms con curva `cubic-bezier(.22, 1, .36, 1)`.
- `prefers-reduced-motion` desactiva las animaciones no esenciales.

## Componentes

Los componentes reutilizables están en `frontend/src/components/ui/index.tsx`:

- `Button`: variantes primaria, secundaria, acento, fantasma y peligro.
- `Card`: superficie estándar y variante interactiva accesible por teclado.
- `Badge`: estado compacto con indicador visual.
- `PageHeader`: título, contexto, descripción y acciones.
- `SearchBar`: búsqueda con foco y limpieza rápida.
- `Modal`: diálogo accesible, cierre con Escape y fondo desenfocado.
- `Field`, `Input` y `Select`: controles de formulario consistentes.
- `SectionTitle`: encabezado interno de tarjetas y módulos.

## Responsive y accesibilidad

- A partir de `900px`, el sidebar se convierte en menú lateral desplegable.
- A partir de `640px`, tarjetas y formularios pasan a una columna.
- Tablas y grupos de filtros tienen desplazamiento horizontal controlado.
- Los elementos interactivos tienen foco visible y nombres accesibles.
- Las tarjetas clicables responden a Enter y barra espaciadora.
- El contraste de texto y estados debe conservarse al crear componentes nuevos.
- Ninguna pantalla debe producir desplazamiento horizontal del documento.

## Criterio para pantallas nuevas

Cada módulo nuevo debe utilizar el shell principal, `PageHeader`, la barra de herramientas, los componentes de formulario y las tablas existentes. No se deben introducir colores, radios, sombras ni patrones de interacción aislados sin actualizar primero este sistema visual.
