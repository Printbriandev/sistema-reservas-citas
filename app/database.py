from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

URL_BASE_DATOS = "sqlite:///./citas.db"

motor = create_engine(URL_BASE_DATOS, connect_args={"check_same_thread": False})
SesionLocal = sessionmaker(bind=motor, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    sesion: Session = SesionLocal()
    try:
        yield sesion
    finally:
        sesion.close()
