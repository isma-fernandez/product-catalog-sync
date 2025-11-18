from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config.app_config import settings


Base = declarative_base()
engine = create_engine(
    f"postgresql://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Proporciona una sesión de base de datos
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Crea todas las tablas en la base de datos
    """
    # Importar todos los modelos aquí para que estén registrados con el Base
    # no se mueven al inicio del archivo para evitar importaciones circulares
    from src.models.product import Product
    Base.metadata.create_all(bind=engine)

