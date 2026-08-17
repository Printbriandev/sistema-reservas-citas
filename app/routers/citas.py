from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.models import Cita, Cliente, EstadoCita, Profesional

router = APIRouter(prefix="/citas", tags=["Citas"])

ESTADOS_ACTIVOS = (EstadoCita.PENDIENTE, EstadoCita.CONFIRMADA)

# Anticipación mínima para poder cancelar una cita, en horas.
HORAS_MINIMAS_CANCELACION = 24


def _se_solapan(inicio_a, fin_a, inicio_b, fin_b) -> bool:
    """Dos rangos [inicio, fin) se solapan si cada uno empieza antes de que
    el otro termine. Con '<' estricto, una cita que empieza justo cuando
    otra termina NO se considera solapamiento (quedan pegadas, no cruzadas).
    """
    return inicio_a < fin_b and inicio_b < fin_a


def validar_reglas_de_negocio(datos: schemas.CitaCrear, db: Session) -> None:
    """Valida las reglas del dominio antes de crear una cita.

    Cada regla lanza HTTPException(409) con un mensaje explicativo.

    TODO 4 - Duracion: debe ser multiplo de 30 minutos.
    TODO 5 - Cliente ocupado: el cliente no puede tener dos citas activas
             que se solapen entre si.
    """
    if datos.inicio < datetime.now():
        raise HTTPException(
            status.HTTP_409_CONFLICT, "No se puede agendar una cita en el pasado"
        )

    fin_nueva = datos.inicio + timedelta(minutes=datos.duracion_min)

    citas_del_profesional = db.scalars(
        select(Cita).where(
            Cita.profesional_id == datos.profesional_id,
            Cita.estado.in_(ESTADOS_ACTIVOS),
        )
    )
    for cita in citas_del_profesional:
        if _se_solapan(datos.inicio, fin_nueva, cita.inicio, cita.fin):
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f"El profesional ya tiene una cita entre {cita.inicio} y {cita.fin}",
            )

    # Regla 2: la cita debe caber completa dentro del horario laboral.
    # Se valida tanto el inicio como el fin: empezar dentro del horario
    # no basta si la cita se extiende mas alla de la hora de cierre.
    profesional = db.get(Profesional, datos.profesional_id)
    if datos.inicio.time() < profesional.hora_inicio or fin_nueva.time() > profesional.hora_fin:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"La cita debe estar dentro del horario laboral "
            f"({profesional.hora_inicio} - {profesional.hora_fin})",
        )


@router.post("", response_model=schemas.CitaLeer, status_code=status.HTTP_201_CREATED)
def crear_cita(datos: schemas.CitaCrear, db: Session = Depends(get_db)):
    if db.get(Cliente, datos.cliente_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Cliente no encontrado")
    if db.get(Profesional, datos.profesional_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Profesional no encontrado")

    validar_reglas_de_negocio(datos, db)

    cita = Cita(**datos.model_dump(), estado=EstadoCita.PENDIENTE)
    db.add(cita)
    db.commit()
    db.refresh(cita)
    return cita


@router.get("", response_model=list[schemas.CitaLeer])
def listar_citas(
    profesional_id: int | None = None,
    cliente_id: int | None = None,
    estado: EstadoCita | None = None,
    db: Session = Depends(get_db),
):
    consulta = select(Cita).order_by(Cita.inicio)
    if profesional_id is not None:
        consulta = consulta.where(Cita.profesional_id == profesional_id)
    if cliente_id is not None:
        consulta = consulta.where(Cita.cliente_id == cliente_id)
    if estado is not None:
        consulta = consulta.where(Cita.estado == estado)
    return list(db.scalars(consulta))


def _obtener_cita(cita_id: int, db: Session) -> Cita:
    cita = db.get(Cita, cita_id)
    if cita is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Cita no encontrada")
    return cita


@router.patch("/{cita_id}/confirmar", response_model=schemas.CitaLeer)
def confirmar_cita(cita_id: int, db: Session = Depends(get_db)):
    cita = _obtener_cita(cita_id, db)
    if cita.estado is not EstadoCita.PENDIENTE:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"Solo se confirman citas PENDIENTE; esta esta {cita.estado.value}",
        )
    cita.estado = EstadoCita.CONFIRMADA
    db.commit()
    db.refresh(cita)
    return cita


@router.patch("/{cita_id}/cancelar", response_model=schemas.CitaLeer)
def cancelar_cita(cita_id: int, db: Session = Depends(get_db)):
    cita = _obtener_cita(cita_id, db)
    if cita.estado not in ESTADOS_ACTIVOS:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"No se puede cancelar una cita {cita.estado.value}",
        )
    # TODO 6 - Anticipacion minima: rechazar si faltan menos de
    #          HORAS_MINIMAS_CANCELACION horas para el inicio.
    cita.estado = EstadoCita.CANCELADA
    db.commit()
    db.refresh(cita)
    return cita
