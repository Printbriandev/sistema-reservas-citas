# Plantilla de historia de usuario

Necesitas **al menos 10**, cada una con criterios de aceptación y puntos de historia.
Las mismas van cargadas en Jira / Azure DevOps.

## Formato

> **HU-00 — [Título corto]**
>
> **Como** [rol]
> **quiero** [capacidad]
> **para** [beneficio].
>
> **Épica:** [a qué épica pertenece]
> **Puntos de historia:** [1, 2, 3, 5, 8]
> **Prioridad:** Alta / Media / Baja
>
> **Criterios de aceptación:**
> - Dado [contexto], cuando [acción], entonces [resultado observable].
> - Dado [contexto], cuando [acción], entonces [resultado observable].
>
> **Tareas técnicas:**
> - [ ]
> - [ ]

---

## Ejemplo de referencia

> **HU-04 — Evitar citas solapadas**
>
> **Como** recepcionista
> **quiero** que el sistema rechace una cita que se cruce con otra del mismo profesional
> **para** no comprometer al profesional en dos lugares a la vez.
>
> **Épica:** Agendamiento
> **Puntos de historia:** 5
> **Prioridad:** Alta
>
> **Criterios de aceptación:**
> - Dado un profesional con una cita de 9:00 a 9:30, cuando intento agendar otra de
>   9:15 a 9:45 con ese profesional, entonces el sistema la rechaza con un mensaje
>   que explica el conflicto.
> - Dado un profesional con una cita de 9:00 a 9:30, cuando agendo otra de 9:30 a 10:00,
>   entonces se acepta, porque no hay cruce real.
> - Dada una cita cancelada de 9:00 a 9:30, cuando agendo otra en ese mismo horario,
>   entonces se acepta.
>
> **Tareas técnicas:**
> - [ ] Consultar citas activas del profesional en el rango solicitado
> - [ ] Implementar la comparación de rangos en `validar_reglas_de_negocio`
> - [ ] Escribir las pruebas automatizadas de los tres criterios

Nota sobre este ejemplo: fíjate que **el segundo y tercer criterio son casos borde**.
Una historia con un solo criterio de camino feliz se ve pobre; los bordes son los que
demuestran que pensaste el problema.

---

## Materia prima para tus 10 historias

Del sistema salen naturalmente. No las copies tal cual — decide tú el rol, la prioridad
y los puntos, porque eso es lo que tendrás que justificar:

**Épica: Gestión de clientes**
- Registrar un cliente
- Evitar clientes duplicados por correo
- Consultar y listar clientes

**Épica: Gestión de profesionales**
- Registrar un profesional con su horario de atención
- Consultar disponibilidad de un profesional

**Épica: Agendamiento**
- Agendar una cita
- Evitar citas solapadas del profesional (regla 1)
- Respetar el horario laboral (regla 2)
- Impedir reservas en el pasado (regla 3)
- Restringir la duración a bloques de 30 minutos (regla 4)
- Impedir que un cliente tenga dos citas a la vez (regla 5)

**Épica: Ciclo de vida de la cita**
- Confirmar una cita pendiente
- Cancelar una cita con anticipación mínima (regla 6)
- Consultar el historial de citas con filtros

---

## Sobre los puntos de historia

Son **esfuerzo relativo, no horas**. La escala habitual es Fibonacci: 1, 2, 3, 5, 8.

Método rápido: toma la historia más simple que tengas (probablemente "consultar
clientes"), asígnale 1, y estima el resto comparando contra ella. Una historia de 5
debería sentirse unas cinco veces más costosa que la de 1.

Prepárate para responder *por qué* una historia es 5 y otra 2. Esa es la pregunta que
delata a quien puso números al azar.
