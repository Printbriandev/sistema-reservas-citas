from datetime import datetime, time

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator

from app.models import EstadoCita


class ClienteCrear(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    email: EmailStr
    telefono: str = Field(min_length=1, max_length=30)


class ClienteLeer(ClienteCrear):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ProfesionalCrear(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    especialidad: str = Field(min_length=1, max_length=120)
    hora_inicio: time
    hora_fin: time

    @model_validator(mode="after")
    def validar_rango_horario(self):
        if self.hora_inicio >= self.hora_fin:
            raise ValueError("hora_inicio debe ser anterior a hora_fin")
        return self


class ProfesionalLeer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    especialidad: str
    hora_inicio: time
    hora_fin: time


class CitaCrear(BaseModel):
    cliente_id: int
    profesional_id: int
    inicio: datetime
    duracion_min: int = Field(ge=30, le=240)


class CitaLeer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_id: int
    profesional_id: int
    inicio: datetime
    duracion_min: int
    estado: EstadoCita
