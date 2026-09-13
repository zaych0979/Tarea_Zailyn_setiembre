---
id: 001
titulo: Control de Contratos
estado: Implementada
fecha: 2026-09-13
autor: zaych0979
---

# Especificación 001 — Control de Contratos

## 1. Objetivo

Construir una aplicación que permita registrar y dar seguimiento a los contratos de la
organización, indicando el **área** a la que pertenece cada contrato y su **fecha de
vencimiento**, de modo que el sistema advierta automáticamente cuando un contrato está
próximo a vencer (**3 meses antes** de la fecha de vencimiento) para gestionar su renovación
a tiempo.

## 2. Alcance

**Incluye:**
- Registro, edición, consulta y eliminación de contratos (CRUD).
- Asignación de un área/departamento a cada contrato.
- Cálculo automático del estado del contrato según la fecha de vencimiento.
- Listado de contratos con indicador visual de advertencia de renovación.
- Filtro/orden por área y por estado (Vigente / Por vencer / Vencido).

**No incluye (fuera de alcance de esta versión):**
- Envío de notificaciones por correo/SMS (queda como especificación futura).
- Gestión documental (adjuntar el PDF del contrato).
- Flujos de aprobación o firma electrónica.
- Autenticación/roles de usuario (se asume un solo usuario administrador por ahora).

## 3. Actores

- **Administrador de contratos**: única persona usuaria en esta versión. Crea, edita,
  consulta y elimina contratos, y visualiza las advertencias de vencimiento.

## 4. Requisitos funcionales

| ID | Requisito |
|----|-----------|
| RF-01 | El sistema debe permitir crear un contrato indicando: nombre del contrato, área, contraparte/proveedor, fecha de inicio, fecha de vencimiento y (opcional) monto y responsable. |
| RF-02 | El sistema debe permitir editar y eliminar un contrato existente. |
| RF-03 | El sistema debe listar todos los contratos mostrando: nombre, área, fecha de vencimiento y estado calculado. |
| RF-04 | El sistema debe permitir filtrar el listado por área y por estado. |
| RF-05 | El sistema debe calcular automáticamente el estado del contrato (ver Reglas de negocio) cada vez que se consulta el listado, sin requerir un campo editable manualmente. |
| RF-06 | El sistema debe destacar visualmente (p. ej. color/etiqueta de advertencia) los contratos en estado "Por vencer" y "Vencido". |
| RF-07 | El sistema debe permitir consultar el detalle de un contrato individual. |

## 5. Reglas de negocio

- **RN-01 (Advertencia de renovación):** un contrato pasa a estado **"Por vencer"** cuando
  la fecha actual está a **3 meses o menos** (90 días, usando meses calendario) de su fecha
  de vencimiento, y aún no ha vencido.
- **RN-02 (Vencido):** un contrato pasa a estado **"Vencido"** cuando la fecha actual es
  posterior a su fecha de vencimiento.
- **RN-03 (Vigente):** un contrato está en estado **"Vigente"** cuando faltan más de 3 meses
  para su vencimiento.
- **RN-04:** el estado no se almacena como un valor fijo editable por la persona usuaria;
  se **deriva** siempre a partir de la fecha de vencimiento y la fecha actual, para evitar
  inconsistencias.
- **RN-05:** el área de un contrato es obligatoria y debe pertenecer a un catálogo cerrado
  de áreas (ver Modelo de datos), para permitir filtrado y reportes consistentes.

## 6. Modelo de datos

### Entidad `Contrato`

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|--------------|
| id | entero | sí (autogenerado) | Identificador único. |
| nombre | texto | sí | Nombre/título descriptivo del contrato. |
| area_id | referencia a `Area` | sí | Área a la que pertenece el contrato. |
| contraparte | texto | no | Proveedor o contraparte del contrato. |
| fecha_inicio | fecha | no | Fecha de inicio de vigencia. |
| fecha_vencimiento | fecha | sí | Fecha de vencimiento del contrato. |
| monto | decimal | no | Monto asociado al contrato. |
| responsable | texto | no | Persona responsable de dar seguimiento. |
| notas | texto | no | Observaciones libres. |

**Estado** (`Vigente` / `Por vencer` / `Vencido`) es un campo **calculado**, no persistido,
derivado según RN-01 a RN-03.

### Entidad `Area`

| Campo | Tipo | Obligatorio | Descripción |
|-------|------|-------------|--------------|
| id | entero | sí (autogenerado) | Identificador único. |
| nombre | texto | sí, único | Nombre del área (p. ej. Legal, Recursos Humanos, TI, Finanzas, Operaciones, Compras). |

## 7. Requisitos no funcionales

- **RNF-01:** la aplicación debe seguir el patrón de arquitectura **MVC** (Modelo–Vista–Controlador).
- **RNF-02:** la gestión de librerías y del entorno del proyecto debe hacerse con **uv**.
- **RNF-03:** el cálculo de estado debe ejecutarse en el servidor (capa de modelo/controlador),
  no confiarse a lógica del cliente.
- **RNF-04:** la aplicación debe ser utilizable desde un navegador de escritorio estándar.

## 8. Criterios de aceptación

1. Al crear un contrato con fecha de vencimiento a 2 meses de la fecha actual, el listado
   lo muestra con estado **"Por vencer"** y una advertencia visible.
2. Al crear un contrato con fecha de vencimiento a 6 meses de la fecha actual, el listado
   lo muestra con estado **"Vigente"**, sin advertencia.
3. Al crear un contrato con fecha de vencimiento anterior a hoy, el listado lo muestra con
   estado **"Vencido"**.
4. Es posible filtrar el listado para ver únicamente los contratos de un área específica.
5. Es posible editar la fecha de vencimiento de un contrato y el estado se recalcula
   automáticamente sin pasos adicionales.

## 9. Preguntas abiertas / futuras especificaciones

- ¿El umbral de advertencia (3 meses) debe ser configurable por área o por tipo de contrato?
- ¿Se requiere notificación por correo además de la advertencia visual? (posible especificación 002)
- ¿Se requiere historial de renovaciones (contrato renovado → nueva fecha de vencimiento
  conservando el histórico)?

## 10. Cierre

Implementada en `src/control_contratos/` (MVC, Flask, gestión de dependencias con `uv`).
Los criterios de aceptación de la sección 8 se verificaron manualmente por HTTP: cálculo
correcto de estado (`Vigente` / `Por vencer` / `Vencido`), filtros por área y por estado,
y advertencia de renovación visible en el detalle del contrato.
