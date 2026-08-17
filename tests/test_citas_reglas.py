"""Reglas de negocio: el trabajo de la noche, en TDD.

Cada prueba esta marcada como `skip` a proposito. El flujo es, una regla a la vez:

  1. Quitar el decorador `@pytest.mark.skip` de la prueba.
  2. Escribir el cuerpo de la prueba y verla FALLAR (rojo).
  3. Implementar la regla en `validar_reglas_de_negocio` (app/routers/citas.py).
  4. Ver la prueba PASAR (verde) y seguir con la siguiente.

Cada una de estas reglas es tambien una fila de la plantilla de casos de prueba
del documento, y la fuente de los criterios de aceptacion y rechazo.
"""

from datetime import timedelta

import pytest

MOTIVO = "Pendiente: se implementa en pareja siguiendo TDD"


def _crear_cliente(client, email):
    return client.post(
        "/clientes",
        json={"nombre": "Cliente de prueba", "email": email, "telefono": "809-555-0000"},
    ).json()


def test_rechaza_solapamiento_del_profesional(
    client, cliente_creado, profesional_creado, proximo_dia_laborable
):
    """REGLA 1 - El profesional no puede tener dos citas que se cruzen.

    Dado un profesional con una cita activa de 9:00 a 9:30,
    cuando se intenta agendar otra de 9:15 a 9:45 con el mismo profesional,
    entonces la respuesta es 409 y la segunda cita no se crea.
    """
    client.post(
        "/citas",
        json={
            "cliente_id": cliente_creado["id"],
            "profesional_id": profesional_creado["id"],
            "inicio": proximo_dia_laborable.isoformat(),
            "duracion_min": 30,
        },
    )
    otro_cliente = _crear_cliente(client, "solapa1@example.com")

    inicio_solapado = proximo_dia_laborable + timedelta(minutes=15)
    respuesta = client.post(
        "/citas",
        json={
            "cliente_id": otro_cliente["id"],
            "profesional_id": profesional_creado["id"],
            "inicio": inicio_solapado.isoformat(),
            "duracion_min": 30,
        },
    )

    assert respuesta.status_code == 409
    assert len(client.get("/citas").json()) == 1


def test_permite_cita_pegada_sin_solapar(
    client, cliente_creado, profesional_creado, proximo_dia_laborable
):
    """REGLA 1 (borde) - Una cita que empieza justo cuando termina otra si vale.

    Dado un profesional con una cita de 9:00 a 9:30,
    cuando se agenda otra de 9:30 a 10:00,
    entonces la respuesta es 201.
    """
    client.post(
        "/citas",
        json={
            "cliente_id": cliente_creado["id"],
            "profesional_id": profesional_creado["id"],
            "inicio": proximo_dia_laborable.isoformat(),
            "duracion_min": 30,
        },
    )
    otro_cliente = _crear_cliente(client, "pegada1@example.com")

    inicio_pegado = proximo_dia_laborable + timedelta(minutes=30)
    respuesta = client.post(
        "/citas",
        json={
            "cliente_id": otro_cliente["id"],
            "profesional_id": profesional_creado["id"],
            "inicio": inicio_pegado.isoformat(),
            "duracion_min": 30,
        },
    )

    assert respuesta.status_code == 201


def test_rechaza_cita_fuera_del_horario_laboral(
    client, cliente_creado, profesional_creado, proximo_dia_laborable
):
    """REGLA 2 - La cita debe caber completa en el horario del profesional.

    Dado un profesional que atiende de 08:00 a 17:00,
    cuando se intenta agendar a las 07:00,
    entonces la respuesta es 409.
    """
    antes_de_abrir = proximo_dia_laborable.replace(hour=7, minute=0)
    respuesta = client.post(
        "/citas",
        json={
            "cliente_id": cliente_creado["id"],
            "profesional_id": profesional_creado["id"],
            "inicio": antes_de_abrir.isoformat(),
            "duracion_min": 30,
        },
    )

    assert respuesta.status_code == 409


def test_rechaza_cita_que_termina_despues_del_cierre(
    client, cliente_creado, profesional_creado, proximo_dia_laborable
):
    """REGLA 2 (borde) - No basta con que empiece dentro del horario.

    Dado un profesional que cierra a las 17:00,
    cuando se agenda una cita de 16:45 con 30 minutos de duracion,
    entonces la respuesta es 409 porque terminaria a las 17:15.
    """
    casi_al_cierre = proximo_dia_laborable.replace(hour=16, minute=45)
    respuesta = client.post(
        "/citas",
        json={
            "cliente_id": cliente_creado["id"],
            "profesional_id": profesional_creado["id"],
            "inicio": casi_al_cierre.isoformat(),
            "duracion_min": 30,
        },
    )

    assert respuesta.status_code == 409


def test_rechaza_cita_en_el_pasado(
    client, cliente_creado, profesional_creado, proximo_dia_laborable
):
    """REGLA 3 - No se reserva en el pasado.

    Cuando se intenta agendar una cita con fecha de ayer,
    entonces la respuesta es 409.
    """
    ayer = proximo_dia_laborable - timedelta(days=2)
    respuesta = client.post(
        "/citas",
        json={
            "cliente_id": cliente_creado["id"],
            "profesional_id": profesional_creado["id"],
            "inicio": ayer.isoformat(),
            "duracion_min": 30,
        },
    )

    assert respuesta.status_code == 409


def test_rechaza_duracion_no_multiplo_de_treinta(
    client, cliente_creado, profesional_creado, proximo_dia_laborable
):
    """REGLA 4 - La duracion debe ser multiplo de 30 minutos.

    Cuando se agenda una cita de 45 minutos,
    entonces la respuesta es 409.
    """
    respuesta = client.post(
        "/citas",
        json={
            "cliente_id": cliente_creado["id"],
            "profesional_id": profesional_creado["id"],
            "inicio": proximo_dia_laborable.isoformat(),
            "duracion_min": 45,
        },
    )

    assert respuesta.status_code == 409


@pytest.mark.skip(reason=MOTIVO)
def test_rechaza_cliente_con_dos_citas_simultaneas():
    """REGLA 5 - El cliente no puede estar en dos lugares a la vez.

    Dado un cliente con una cita activa de 9:00 a 9:30 con el profesional A,
    cuando intenta agendar de 9:15 a 9:45 con el profesional B,
    entonces la respuesta es 409.
    """


def test_una_cita_cancelada_libera_el_espacio(
    client, cliente_creado, profesional_creado, proximo_dia_laborable
):
    """REGLA 1 + estados - Las citas canceladas no bloquean el horario.

    Dado un profesional con una cita de 9:00 a 9:30 que luego se cancela,
    cuando se agenda otra cita de 9:00 a 9:30,
    entonces la respuesta es 201.
    """
    primera = client.post(
        "/citas",
        json={
            "cliente_id": cliente_creado["id"],
            "profesional_id": profesional_creado["id"],
            "inicio": proximo_dia_laborable.isoformat(),
            "duracion_min": 30,
        },
    ).json()
    client.patch(f"/citas/{primera['id']}/cancelar")
    otro_cliente = _crear_cliente(client, "libera1@example.com")

    respuesta = client.post(
        "/citas",
        json={
            "cliente_id": otro_cliente["id"],
            "profesional_id": profesional_creado["id"],
            "inicio": proximo_dia_laborable.isoformat(),
            "duracion_min": 30,
        },
    )

    assert respuesta.status_code == 201


@pytest.mark.skip(reason=MOTIVO)
def test_rechaza_cancelacion_sin_anticipacion_minima():
    """REGLA 6 - Cancelar exige 24 horas de anticipacion.

    Dada una cita que empieza dentro de 2 horas,
    cuando se intenta cancelar,
    entonces la respuesta es 409.
    """


@pytest.mark.skip(reason=MOTIVO)
def test_permite_cancelacion_con_anticipacion_suficiente():
    """REGLA 6 (borde) - Con mas de 24 horas si se puede cancelar.

    Dada una cita que empieza dentro de 3 dias,
    cuando se cancela,
    entonces la respuesta es 200 y el estado queda CANCELADA.
    """
