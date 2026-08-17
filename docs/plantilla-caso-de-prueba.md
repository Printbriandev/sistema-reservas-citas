# Plantilla de caso de prueba

## Formato detallado

Para los casos importantes (las reglas de negocio), usa la ficha completa:

| Campo | Contenido |
|---|---|
| **ID del caso** | CP-000 |
| **Requerimiento asociado** | RF-00 / RNF-00 |
| **Historia de usuario** | HU-00 |
| **Título** | |
| **Precondiciones** | Estado que debe existir antes de ejecutar |
| **Datos de entrada** | |
| **Pasos** | 1. <br> 2. <br> 3. |
| **Resultado esperado** | |
| **Criterio de aceptación** | Qué hace que la prueba se considere aprobada |
| **Criterio de rechazo** | Qué hace que se considere fallida |
| **Tipo** | Manual / Automatizada |
| **Prioridad** | Alta / Media / Baja |
| **Responsable** | |
| **Resultado obtenido** | |
| **Estado** | Aprobada / Fallida / Bloqueada |

### Ejemplo de referencia (ya implementado en `tests/test_clientes.py`)

| Campo | Contenido |
|---|---|
| **ID del caso** | CP-003 |
| **Título** | Rechazar registro de cliente con correo duplicado |
| **Precondiciones** | Existe un cliente registrado con el correo `ana.perez@example.com` |
| **Datos de entrada** | `{"nombre": "Otra Persona", "email": "ana.perez@example.com", "telefono": "809-555-0202"}` |
| **Pasos** | 1. Enviar POST a `/clientes` con el correo ya registrado |
| **Resultado esperado** | HTTP 409 y el cliente no se crea |
| **Criterio de aceptación** | Código 409 y la cantidad de clientes no aumenta |
| **Criterio de rechazo** | Cualquier código 2xx, o que se cree un segundo registro |
| **Tipo** | Automatizada |
| **Prioridad** | Alta |
| **Estado** | Aprobada |

---

## Formato de tabla resumen

Para el conjunto completo de casos, una tabla compacta:

| ID | Título | RF/RNF | HU | Tipo | Resultado esperado | Estado | Responsable |
|---|---|---|---|---|---|---|---|
| CP-001 | | | | | | | |
| CP-002 | | | | | | | |
| CP-003 | | | | | | | |

---

## Casos ya implementados en el repositorio

Los IDs están en los docstrings de cada prueba, así que la tabla se llena leyendo el
código. Para verlos todos en orden:

```bash
.venv/Scripts/python.exe -m pytest --collect-only -q
```

- `tests/test_health.py` — CP-001
- `tests/test_clientes.py` — CP-002 a CP-006
- `tests/test_profesionales.py` — CP-007 a CP-009
- `tests/test_citas.py` — CP-010 a CP-018
- `tests/test_citas_reglas.py` — las 10 reglas de negocio (numerar al implementarlas)

---

## Equipos de prueba y responsabilidades

La rúbrica evalúa plantillas **y** equipos juntos (2 puntos). Define también:

| Rol | Responsabilidad | Casos a su cargo |
|---|---|---|
| | | |
