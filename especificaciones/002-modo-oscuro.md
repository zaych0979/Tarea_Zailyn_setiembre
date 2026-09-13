---
id: 002
titulo: Modo oscuro (fondo oscuro)
estado: Borrador
fecha: 2026-09-13
autor: zaych0979
---

# Especificación 002 — Modo oscuro

## 1. Objetivo

Ofrecer un tema visual de **fondo oscuro** para la aplicación de Control de Contratos
([[001-control-contratos]]), de modo que toda la interfaz (listado, formulario, detalle
y administración de áreas) pueda visualizarse con una paleta oscura, manteniendo la
legibilidad de las advertencias de vencimiento.

## 2. Alcance

**Incluye:**
- Un tema oscuro que cubra todas las vistas existentes (listado de contratos, formulario
  de alta/edición, detalle de contrato, listado/alta de áreas) y los elementos comunes
  (cabecera, mensajes flash, tablas, formularios, botones).
- Una forma de alternar entre tema claro y tema oscuro desde la interfaz.
- Persistencia de la preferencia de tema entre visitas (en el mismo navegador).
- Ajuste de los colores de los estados (`Vigente` / `Por vencer` / `Vencido`) para que
  mantengan buen contraste y sigan siendo distinguibles sobre fondo oscuro.

**No incluye (fuera de alcance de esta versión):**
- Detección automática de la preferencia del sistema operativo (`prefers-color-scheme`)
  como único mecanismo; se contempla como mejora opcional, no como requisito obligatorio.
- Temas adicionales más allá de claro/oscuro (p. ej. alto contraste).
- Personalización de colores por parte de la persona usuaria.

## 3. Actores

- **Administrador de contratos**: mismo actor de la especificación 001, que ahora puede
  elegir el tema visual de la aplicación.

## 4. Requisitos funcionales

| ID | Requisito |
|----|-----------|
| RF-01 | La aplicación debe incluir un control visible (p. ej. un botón en la cabecera) para alternar entre tema claro y tema oscuro. |
| RF-02 | Al activar el tema oscuro, todas las páginas de la aplicación deben mostrarse con la paleta oscura, sin páginas que queden con fondo claro por error. |
| RF-03 | La preferencia de tema elegida debe recordarse en visitas posteriores dentro del mismo navegador, sin requerir volver a seleccionarla en cada página. |
| RF-04 | El cambio de tema debe poder hacerse sin perder el estado de ningún formulario en curso (p. ej. no debe recargar perdiendo datos no guardados). |

## 5. Reglas de negocio / diseño

- **RN-01:** el tema por defecto para una persona que visita la aplicación por primera vez
  es el **tema claro** actual.
- **RN-02:** las etiquetas de estado deben mantener una asociación de color consistente
  entre temas (verde para `Vigente`, ámbar para `Por vencer`, rojo para `Vencido`), solo
  ajustando los tonos para asegurar contraste legible sobre fondo oscuro.
- **RN-03:** las filas de contratos con advertencia (`Por vencer` o `Vencido`) deben seguir
  destacándose visualmente en el tema oscuro, igual que lo hacen en el tema claro.

## 6. Modelo de datos

No se requieren cambios al modelo de datos de `Contrato` ni `Area` ([[001-control-contratos]]).
La preferencia de tema es un dato de presentación, no de negocio: se almacena en el
navegador de la persona usuaria (no en la base de datos), ya que la aplicación no maneja
todavía cuentas de usuario ni sesiones diferenciadas.

## 7. Requisitos no funcionales

- **RNF-01:** la implementación debe respetar el patrón **MVC** ya establecido: el cambio
  de tema es una preocupación de la capa de vista (plantillas/CSS/JS), sin introducir
  lógica de negocio en controladores o modelos.
- **RNF-02:** no debe agregarse ninguna dependencia nueva vía `pip`; si se necesita alguna
  librería, se añade con `uv add`.
- **RNF-03:** el contraste de texto sobre fondo oscuro debe ser suficiente para lectura
  cómoda (contraste mínimo razonable tipo WCAG AA para texto normal).

## 8. Criterios de aceptación

1. Al presionar el control de tema, toda la página cambia de fondo claro a fondo oscuro
   (y viceversa) sin recargar a un estado inconsistente.
2. Al navegar del listado a un formulario o al detalle de un contrato con el tema oscuro
   activo, la nueva página conserva el tema oscuro.
3. Al cerrar y volver a abrir la aplicación en el mismo navegador, se conserva el último
   tema elegido.
4. Con el tema oscuro activo, las etiquetas de estado (`Vigente`, `Por vencer`, `Vencido`)
   siguen siendo claramente distinguibles entre sí y legibles.

## 9. Preguntas abiertas / futuras especificaciones

- ¿Debe respetarse automáticamente `prefers-color-scheme` del sistema operativo como
  valor inicial, además del control manual?
- Cuando la aplicación tenga autenticación, ¿la preferencia de tema debería guardarse
  por usuario en el servidor en vez de solo en el navegador?
