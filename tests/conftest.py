from datetime import datetime, time, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture
def sesion():
    """Base de datos en memoria, nueva y vacia para cada prueba."""
    motor = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=motor)
    Sesion = sessionmaker(bind=motor, autoflush=False, autocommit=False)
    sesion = Sesion()
    try:
        yield sesion
    finally:
        sesion.close()
        Base.metadata.drop_all(bind=motor)
        motor.dispose()


@pytest.fixture
def client(sesion):
    def get_db_de_prueba():
        yield sesion

    app.dependency_overrides[get_db] = get_db_de_prueba
    with TestClient(app) as cliente_http:
        yield cliente_http
    app.dependency_overrides.clear()


@pytest.fixture
def cliente_creado(client):
    respuesta = client.post(
        "/clientes",
        json={
            "nombre": "Ana Perez",
            "email": "ana.perez@example.com",
            "telefono": "809-555-0101",
        },
    )
    assert respuesta.status_code == 201
    return respuesta.json()


@pytest.fixture
def profesional_creado(client):
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
    return respuesta.json()


@pytest.fixture
def proximo_dia_laborable():
    """Manana a las 9:00, dentro del horario laboral por defecto."""
    manana = datetime.now() + timedelta(days=1)
    return datetime.combine(manana.date(), time(9, 0))
