from src.db.database import init_db
from src.db.healthcheck import verify_db_connection
import logging
from src.utils.logging import setup_logging, get_logger
# DB Tests
from src.repositories import db_repository
from src.db import database
from src.db.models.product import Product
from src.services import csv_reader
from pathlib import Path
from src.config.app_config import settings

logger = get_logger("app.main")

def temp_test_db_operations():
    # Inicializar la base de datos
    verify_db_connection()
    init_db()   
    db = database.create_session()
    new_product = Product(product_id=1,store_id=3,
                    title="Camiseta Azul",price=19.99)
    logger = get_logger("app.main")
    logger.info(f"Creando nuevo producto: {new_product}")
    db_repository.create_product(db, new_product)
    products = db_repository.get_all_products(db)
    logger.info(f"Productos en la base de datos: {products}")
    database.commit_session(db)
    database.close_session(db)

def temp_test_csv_reading():
    file_path: Path = Path(settings.catalog_data_path)
    products = csv_reader.read_products_from_csv(file_path)


def main():
    # Configurar logging
    setup_logging()
    logger: logging.Logger = get_logger(f"app.{__name__}")
    logger.info("Iniciando la aplicación...")

    #temp_test_db_operations()
    temp_test_csv_reading()



if __name__ == "__main__":
    main()