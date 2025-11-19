import sys
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine, Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session
from src.config.app_config import settings
from src.utils.logging import get_logger
from src.db.base import Base


logger = get_logger("app.db")

engine: Engine = create_engine(
    f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)
SessionLocal: Session = sessionmaker(autocommit=False, bind=engine)


def get_db() -> Generator:
    """
    Proporciona una sesión de base de datos a FastAPI
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        logger.debug("Sesión de base de datos cerrada.")

def create_session() -> Session:
    """
    Crea y devuelve una nueva sesión de base de datos
    """
    return SessionLocal()

def close_session(db: Session) -> None:
    """
    Cierra la sesión de base de datos dada
    """
    db.close()
    logger.debug("Sesión de base de datos cerrada.")

def commit_session(db: Session) -> None:
    """
    Confirma los cambios en la sesión de base de datos dada
    """
    try:
        db.commit()
        logger.debug("Commit de la sesión de base de datos realizado con éxito.")
    except:
        db.rollback()
        logger.error("Error al confirmar la sesión de base de datos. Rollback realizado.", exc_info=True)
    finally:
        db.close()

def init_db() -> None:
    """
    Crea todas las tablas en la base de datos
    """
    logger.info("Inicializando tablas en la base de datos...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Todas las tablas fueron creadas correctamente.")
    except SQLAlchemyError:
        logger.error("Error creando las tablas en la base de datos.")
        sys.exit(1)
