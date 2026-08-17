"""Rebanada vertical de referencia.

Este archivo es el patron a seguir para las demas pruebas: un caso de camino
feliz, un caso de rechazo por regla de negocio, un caso de validacion de
entrada y un caso de recurso inexistente.
"""


def test_crear_cliente_camino_feliz(client):
    """CP-002: un cliente con datos validos se registra y recibe un id."""
    respuesta = client.post(
        "/clientes",
        json={
            "nombre": "Ana Perez",
            "email": "ana.perez@example.com",
            "telefono": "809-555-0101",
        },
    )

    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["id"] > 0
    assert cuerpo["nombre"] == "Ana Perez"


def test_rechaza_correo_duplicado(client, cliente_creado):
    """CP-003: el correo es unico; un segundo registro con el mismo es 409."""
    respuesta = client.post(
        "/clientes",
        json={
            "nombre": "Otra Persona",
            "email": cliente_creado["email"],
            "telefono": "809-555-0202",
        },
    )

    assert respuesta.status_code == 409


def test_rechaza_correo_con_formato_invalido(client):
    """CP-004: un correo mal formado se rechaza en la validacion de entrada."""
    respuesta = client.post(
        "/clientes",
        json={
            "nombre": "Ana Perez",
            "email": "no-es-un-correo",
            "telefono": "809-555-0101",
        },
    )

    assert respuesta.status_code == 422


def test_obtener_cliente_inexistente_da_404(client):
    """CP-005: consultar un id que no existe devuelve 404."""
    respuesta = client.get("/clientes/9999")

    assert respuesta.status_code == 404


def test_listar_clientes_incluye_el_creado(client, cliente_creado):
    """CP-006: el listado refleja los clientes registrados."""
    respuesta = client.get("/clientes")

    assert respuesta.status_code == 200
    correos = [c["email"] for c in respuesta.json()]
    assert cliente_creado["email"] in correos
