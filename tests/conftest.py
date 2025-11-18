"""
Configuración de fixtures para pytest
"""
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from src.db.base import Base


# Configurar variables de entorno para tests antes de importar el código de la aplicación
@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Configurar variables de entorno necesarias para los tests"""
    os.environ["DB_HOST"] = "localhost"
    os.environ["DB_PORT"] = "5432"
    os.environ["DB_USER"] = "test_user"
    os.environ["DB_PASSWORD"] = "test_password"
    os.environ["DB_NAME"] = "test_db"


@pytest.fixture(scope="function")
def db_session():
    """
    Crea una sesión de base de datos en memoria para tests
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def sample_product_data():
    """
    Datos de ejemplo para un producto
    """
    return {
        "product_id": 1,
        "store_id": "1|2|3",
        "title": "Test Product",
        "price": 19.99
    }


@pytest.fixture
def sample_csv_row():
    """
    Fila de ejemplo de CSV
    """
    return {
        "product_id": "123",
        "store_id": "1|2",
        "title": "Sample Product",
        "price": "29.99"
    }
