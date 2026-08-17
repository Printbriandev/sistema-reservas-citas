from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.models import Cliente

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("", response_model=schemas.ClienteLeer, status_code=status.HTTP_201_CREATED)
def crear_cliente(datos: schemas.ClienteCrear, db: Session = Depends(get_db)):
    if db.scalar(select(Cliente).where(Cliente.email == datos.email)):
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Ya existe un cliente con ese correo"
        )
    cliente = Cliente(**datos.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


@router.get("", response_model=list[schemas.ClienteLeer])
def listar_clientes(db: Session = Depends(get_db)):
    return list(db.scalars(select(Cliente).order_by(Cliente.id)))


@router.get("/{cliente_id}", response_model=schemas.ClienteLeer)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.get(Cliente, cliente_id)
    if cliente is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Cliente no encontrado")
    return cliente
