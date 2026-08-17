def test_health_responde_ok(client):
    """CP-001: el servicio responde y reporta estado operativo."""
    respuesta = client.get("/health")

    assert respuesta.status_code == 200
    assert respuesta.json() == {"estado": "ok"}
