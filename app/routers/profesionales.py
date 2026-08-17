from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.models import Profesional

router = APIRouter(prefix="/profesionales", tags=["Profesionales"])


@router.post(
    "", response_model=schemas.ProfesionalLeer, status_code=status.HTTP_201_CREATED
)
def crear_profesional(datos: schemas.ProfesionalCrear, db: Session = Depends(get_db)):
    profesional = Profesional(**datos.model_dump())
    db.add(profesional)
    db.commit()
    db.refresh(profesional)
    return profesional


@router.get("", response_model=list[schemas.ProfesionalLeer])
def listar_profesionales(db: Session = Depends(get_db)):
    return list(db.scalars(select(Profesional).order_by(Profesional.id)))


@router.get("/{profesional_id}", response_model=schemas.ProfesionalLeer)
def obtener_profesional(profesional_id: int, db: Session = Depends(get_db)):
    profesional = db.get(Profesional, profesional_id)
    if profesional is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Profesional no encontrado")
    return profesional
