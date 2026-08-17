# Esqueleto del documento — mapa de la rúbrica

Los títulos están en el orden y con la numeración que pide la consigna. Debajo de cada
uno hay **qué se evalúa** y **las preguntas que tienes que responder**. La redacción es
tuya: escribe en tus palabras, porque el video te va a poner a explicar esto en voz.

Peso total: **20 puntos**. El orden en que conviene escribir está marcado con 🔥
(hazlo primero, vale más y cuesta menos).

---

## Hoja de presentación · 0.5 pts

Nombre completo, matrícula, título del proyecto, fecha. Nada más.

## Índice enumerado

Si usas Word, insértalo automático (Referencias → Tabla de contenido) después de haber
aplicado estilos de título. Hacerlo a mano al final es perder 15 minutos.

---

# 1. Estrategia de Trabajo (Planificación) · 4 pts

## 1.1 Nombre del proyecto de software · 0.5 pts
Un título claro y representativo. Ya tienes uno: *Sistema de Reservas de Citas*.
Puedes ajustarlo a un rubro concreto (clínica, barbería, taller) — hace todo lo demás
más fácil de justificar.

## 1.2 Tecnología para aplicar
Las herramientas y lenguajes. Ya están en el `README.md`.
**Lo que agrega valor aquí no es la lista, es el porqué:** ¿por qué FastAPI y no otro
framework? ¿Por qué SQLite y no un motor con servidor?

## 1.3 Objetivo del proyecto · 0.5 pts
¿Qué problema real resuelve el sistema? Un párrafo.
Pregunta guía: *¿qué hace hoy el negocio sin este sistema, y qué le cuesta?*

## 1.4 Alcance del proyecto · 0.5 pts
Los límites. **Tan importante como lo que incluye es lo que deja fuera.**
- ¿Qué SÍ hace el sistema?
- ¿Qué NO hace? (¿cobros? ¿notificaciones por correo? ¿app móvil? ¿multi-sucursal?)
Declarar exclusiones explícitas es lo que distingue un alcance real de una lista de
deseos.

## 1.5 Cronograma del proyecto · 1 pt
Tabla con **actividades, plazos y responsables**. Usa `plantilla-cronograma.md`.

## 1.6 Definición del primer Release · 1 pt
Qué podrá hacer el sistema en su primera versión. Debe coincidir con lo que el video
muestra funcionando — si el documento promete algo que el video no enseña, se nota.

### 1.6.1 Requerimientos funcionales
Lo que el sistema hace. Los endpoints del `README.md` son tu materia prima.
Numéralos (RF-01, RF-02...) porque el plan de pruebas los va a referenciar.

### 1.6.2 Requerimientos no funcionales
Lo que el sistema debe cumplir sin ser una función: tiempo de respuesta,
validación de datos, documentación del API, cobertura de pruebas, portabilidad.
Numéralos (RNF-01, RNF-02...).

---

# 2. Metodología Scrum · 5 pts

## 2.1 Definición de tareas a ejecutar · 1 pt
Desglosa el trabajo en tareas concretas. Cada historia se rompe en tareas técnicas
(modelo, endpoint, validación, prueba).

## 2.2 Definición del equipo de trabajo · 1 pt
Roles, habilidades requeridas y responsabilidades. Los roles de Scrum son
Product Owner, Scrum Master y Development Team.
Pregunta guía: *¿qué habilidad concreta necesita cada rol en este proyecto?*

## 2.3 Herramientas y definición de épicas · 1 pt
La herramienta de gestión (Jira o Azure DevOps) y las **épicas**, que agrupan historias
relacionadas. Con este dominio, las épicas salen casi solas: gestión de clientes,
gestión de profesionales, agendamiento, ciclo de vida de la cita.

## 2.4 Ceremonias de Scrum · 0.5 pts
Fechas concretas de sprint planning, daily stand-ups y sprint review.
**Que las fechas sean coherentes con el cronograma de 1.5.** Si el cronograma dice que
el sprint arranca el 4 y el planning aparece el 9, eso se lee.

## 2.5 Historias de usuario · 1.5 pts 🔥
**Al menos 10**, cada una con criterios de aceptación y puntos de historia.
Usa `plantilla-historia-de-usuario.md`.

Las 6 reglas de negocio del sistema te dan historias directas y defendibles, más las
de CRUD de clientes y profesionales. Van también cargadas en el tablero.

Sobre los story points: son **esfuerzo relativo, no horas**. Usa Fibonacci
(1, 2, 3, 5, 8) y prepárate para justificar por qué una es 5 y otra 2 — eso es lo que
te pueden preguntar.

---

# 3. Plan de Pruebas · 7 pts 🔥 (el bloque de mayor peso)

## 3.1 Lista de requerimientos funcionales y no funcionales · 1 pt
Los mismos de 1.6, ahora **relacionados con las historias de usuario**. Una tabla de
trazabilidad (RF-01 → HU-03 → CP-010) vale mucho y cuesta poco.

## 3.2 Criterios de aceptación y rechazo · 1 pt
Cómo se evalúa que una prueba pasa o falla. Sé concreto: para este sistema, aceptación
es un código HTTP esperado más el estado correcto en la base de datos; rechazo es
cualquier otro código o un efecto secundario no deseado.

## 3.3 Herramientas de pruebas justificadas · 1 pt
pytest, pytest-html, y el TestClient de FastAPI.
**La palabra clave de la rúbrica es "justificadas":** no basta nombrarlas, hay que decir
por qué esa y no otra. ¿Por qué pytest y no unittest?

## 3.4 Cronograma de ejecución de pruebas · 1 pt
Plazos separando **pruebas manuales** y **automatizadas**.

## 3.5 Plantillas para casos de prueba y equipos de pruebas · 2 pts 🔥
Dos puntos, y es el más mecánico de todo el documento.
- Plantilla: `plantilla-caso-de-prueba.md`
- Los casos ya existen y están numerados (CP-001 a CP-018 en `tests/`, más los 10 de
  reglas). Llenar la tabla es transcribir.
- Equipos de prueba: quién ejecuta qué y con qué responsabilidad.

## 3.6 Plan de automatización de pruebas · 1 pt
Herramientas y estrategia. Puntos a cubrir: qué se automatiza y qué no, la estrategia de
base de datos limpia por prueba (está en `tests/conftest.py`), y cómo se genera la
evidencia.

## 3.7 Ejecución y demostración
Adjuntar evidencia. Ya la tienes: `reports/reporte-pruebas.html`. Captura de pantalla del
reporte con las pruebas en verde.

---

# 4. Demostración y Entregables · 4 pts

## 4.1 Video · 1 pt
Muestra el **incremento del sistema** y las funcionalidades del primer Release.
Grábalo sobre `/docs` (Swagger UI): creas un cliente, un profesional, agendas una cita,
intentas agendar una que se solapa y se rechaza. Ese rechazo es el momento más fuerte
del video, porque demuestra que hay lógica de negocio y no solo un CRUD.

Cierra corriendo `pytest` en la terminal para que se vea la suite en verde.

## 4.2 Links funcionales · 3 pts
Repositorio, tablero de gestión, y código de pruebas automatizadas.
**Van en "Texto en línea", no dentro del PDF.** Ver `ENTREGA-checklist.md`.

---

# Conclusiones

Qué aprendiste, qué salió distinto a lo planificado, qué harías diferente.
Es la sección donde se ve si entendiste el proyecto o solo lo ejecutaste. Escribe en
primera persona y sé concreto: una dificultad real vale más que tres generalidades.

# Bibliografía

Documentación oficial de FastAPI, pytest, SQLAlchemy, y la fuente que uses para Scrum
(la Scrum Guide de Schwaber y Sutherland es la referencia estándar). Formato consistente.
