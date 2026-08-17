from fastapi import FastAPI

from app.database import Base, motor
from app.routers import citas, clientes, profesionales

Base.metadata.create_all(bind=motor)

app = FastAPI(
    title="Sistema de Reservas de Citas",
    description=(
        "Primer Release del sistema de reservas de citas. "
        "Permite registrar clientes y profesionales, y agendar citas "
        "respetando las reglas de disponibilidad del negocio."
    ),
    version="1.0.0",
)

app.include_router(clientes.router)
app.include_router(profesionales.router)
app.include_router(citas.router)


@app.get("/health", tags=["Sistema"])
def health():
    return {"estado": "ok"}
