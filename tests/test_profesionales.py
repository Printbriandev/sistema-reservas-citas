def test_crear_profesional_camino_feliz(client):
    """CP-007: un profesional con horario coherente se registra."""
    respuesta = client.post(
        "/profesionales",
        json={
            "nombre": "Dr. Luis Gomez",
            "especialidad": "Odontologia",
            "hora_inicio": "08:00:00",
            "hora_fin": "17:00:00",
        },
    )

    assert respuesta.status_code == 201
    assert respuesta.json()["id"] > 0


def test_rechaza_horario_invertido(client):
    """CP-008: hora_inicio posterior a hora_fin se rechaza."""
    respuesta = client.post(
        "/profesionales",
        json={
            "nombre": "Dr. Luis Gomez",
            "especialidad": "Odontologia",
            "hora_inicio": "17:00:00",
            "hora_fin": "08:00:00",
        },
    )

    assert respuesta.status_code == 422


def test_obtener_profesional_inexistente_da_404(client):
    """CP-009: consultar un id que no existe devuelve 404."""
    respuesta = client.get("/profesionales/9999")

    assert respuesta.status_code == 404
