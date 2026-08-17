# Sistema de Reservas de Citas

Proyecto final de Programación III — ITLA.

API REST para agendar citas entre clientes y profesionales, respetando las reglas de
disponibilidad del negocio.

## Tecnologías

- **Python 3.12** — lenguaje base
- **FastAPI** — framework del API REST, genera documentación interactiva automática
- **SQLAlchemy 2.0 + SQLite** — persistencia sin servidor externo
- **Pydantic v2** — validación de datos de entrada y salida
- **pytest + pytest-html** — pruebas automatizadas y reporte de evidencia

## Instalación

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
```

## Ejecutar el sistema

```bash
.venv/Scripts/python.exe -m uvicorn app.main:app --reload
```

Luego abrir **http://127.0.0.1:8000/docs** para la interfaz interactiva (Swagger UI),
donde se pueden probar todos los endpoints desde el navegador.

## Ejecutar las pruebas automatizadas

```bash
.venv/Scripts/python.exe -m pytest
```

El reporte de evidencia queda en `reports/reporte-pruebas.html`.

## Estructura

```
app/
  main.py              punto de entrada y registro de routers
  database.py          motor, sesión y clase Base
  models.py            entidades: Cliente, Profesional, Cita
  schemas.py           validación de entrada/salida
  routers/
    clientes.py        CRUD de clientes
    profesionales.py   CRUD de profesionales
    citas.py           agendar, confirmar, cancelar y reglas de negocio
tests/
  conftest.py          base de datos limpia por prueba y datos de apoyo
  test_*.py            casos de prueba
docs/                  documentación del proyecto y plantillas
reports/               evidencia de ejecución de pruebas
```

## Reglas de negocio

1. Un profesional no puede tener dos citas que se solapen.
2. Una cita debe caber completa dentro del horario laboral del profesional.
3. No se puede reservar en el pasado.
4. La duración debe ser múltiplo de 30 minutos.
5. Un cliente no puede tener dos citas activas simultáneas.
6. Cancelar exige un mínimo de 24 horas de anticipación.

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/health` | Estado del servicio |
| POST | `/clientes` | Registrar cliente |
| GET | `/clientes` | Listar clientes |
| GET | `/clientes/{id}` | Consultar cliente |
| POST | `/profesionales` | Registrar profesional |
| GET | `/profesionales` | Listar profesionales |
| GET | `/profesionales/{id}` | Consultar profesional |
| POST | `/citas` | Agendar cita (aplica las reglas de negocio) |
| GET | `/citas` | Listar citas, con filtros |
| PATCH | `/citas/{id}/confirmar` | Confirmar una cita pendiente |
| PATCH | `/citas/{id}/cancelar` | Cancelar una cita activa |
