"""Pruebas del flujo de citas que ya cubre el andamiaje actual."""

import pytest


@pytest.fixture
def cita_creada(client, cliente_creado, profesional_creado, proximo_dia_laborable):
    respuesta = client.post(
        "/citas",
        json={
            "cliente_id": cliente_creado["id"],
            "profesional_id": profesional_creado["id"],
            "inicio": proximo_dia_laborable.isoformat(),
            "duracion_min": 30,
        },
    )
    assert respuesta.status_code == 201
    return respuesta.json()


def test_crear_cita_camino_feliz(cita_creada):
    """CP-010: una cita valida queda registrada en estado PENDIENTE."""
    assert cita_creada["id"] > 0
    assert cita_creada["estado"] == "PENDIENTE"


def test_rechaza_cita_con_cliente_inexistente(
    client, profesional_creado, proximo_dia_laborable
):
    """CP-011: agendar para un cliente que no existe devuelve 404."""
    respuesta = client.post(
        "/citas",
        json={
            "cliente_id": 9999,
            "profesional_id": profesional_creado["id"],
            "inicio": proximo_dia_laborable.isoformat(),
            "duracion_min": 30,
        },
    )

    assert respuesta.status_code == 404


def test_rechaza_cita_con_profesional_inexistente(
    client, cliente_creado, proximo_dia_laborable
):
    """CP-012: agendar con un profesional que no existe devuelve 404."""
    respuesta = client.post(
        "/citas",
        json={
            "cliente_id": cliente_creado["id"],
            "profesional_id": 9999,
            "inicio": proximo_dia_laborable.isoformat(),
            "duracion_min": 30,
        },
    )

    assert respuesta.status_code == 404


def test_rechaza_duracion_fuera_de_rango(
    client, cliente_creado, profesional_creado, proximo_dia_laborable
):
    """CP-013: una duracion menor al minimo permitido se rechaza."""
    respuesta = client.post(
        "/citas",
        json={
            "cliente_id": cliente_creado["id"],
            "profesional_id": profesional_creado["id"],
            "inicio": proximo_dia_laborable.isoformat(),
            "duracion_min": 10,
        },
    )

    assert respuesta.status_code == 422


def test_confirmar_cita_pendiente(client, cita_creada):
    """CP-014: una cita PENDIENTE pasa a CONFIRMADA."""
    respuesta = client.patch(f"/citas/{cita_creada['id']}/confirmar")

    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "CONFIRMADA"


def test_no_permite_confirmar_dos_veces(client, cita_creada):
    """CP-015: confirmar una cita ya CONFIRMADA devuelve 409."""
    client.patch(f"/citas/{cita_creada['id']}/confirmar")

    respuesta = client.patch(f"/citas/{cita_creada['id']}/confirmar")

    assert respuesta.status_code == 409


def test_cancelar_cita_activa(client, cita_creada):
    """CP-016: una cita activa pasa a CANCELADA."""
    respuesta = client.patch(f"/citas/{cita_creada['id']}/cancelar")

    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "CANCELADA"


def test_no_permite_cancelar_dos_veces(client, cita_creada):
    """CP-017: cancelar una cita ya CANCELADA devuelve 409."""
    client.patch(f"/citas/{cita_creada['id']}/cancelar")

    respuesta = client.patch(f"/citas/{cita_creada['id']}/cancelar")

    assert respuesta.status_code == 409


def test_listado_filtra_por_profesional(client, cita_creada, profesional_creado):
    """CP-018: el listado se puede filtrar por profesional."""
    respuesta = client.get(
        "/citas", params={"profesional_id": profesional_creado["id"]}
    )

    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 1
