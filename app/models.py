from datetime import datetime, time
from enum import Enum as EnumPython

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class EstadoCita(str, EnumPython):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    COMPLETADA = "COMPLETADA"


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    telefono: Mapped[str] = mapped_column(String(30))

    citas: Mapped[list["Cita"]] = relationship(back_populates="cliente")


class Profesional(Base):
    __tablename__ = "profesionales"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120))
    especialidad: Mapped[str] = mapped_column(String(120))
    hora_inicio: Mapped[time] = mapped_column(Time)
    hora_fin: Mapped[time] = mapped_column(Time)

    citas: Mapped[list["Cita"]] = relationship(back_populates="profesional")


class Cita(Base):
    __tablename__ = "citas"

    id: Mapped[int] = mapped_column(primary_key=True)
    cliente_id: Mapped[int] = mapped_column(ForeignKey("clientes.id"))
    profesional_id: Mapped[int] = mapped_column(ForeignKey("profesionales.id"))
    inicio: Mapped[datetime] = mapped_column(DateTime)
    duracion_min: Mapped[int] = mapped_column(Integer)
    estado: Mapped[EstadoCita] = mapped_column(
        Enum(EstadoCita), default=EstadoCita.PENDIENTE
    )

    cliente: Mapped["Cliente"] = relationship(back_populates="citas")
    profesional: Mapped["Profesional"] = relationship(back_populates="citas")

    @property
    def fin(self) -> datetime:
        from datetime import timedelta

        return self.inicio + timedelta(minutes=self.duracion_min)
