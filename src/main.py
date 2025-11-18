from src.db.database import init_db
from src.db.healthcheck import verify_db_connection
import logging
from src.utils.logging import setup_logging, get_logger
# DB Tests
from src.db import database
from src.db.models.product import Product
from src.services import csv_reader
from pathlib import Path
from src.config.app_config import settings
from src.services.update_catalog import update_catalog
from src.services.update_portal import update_portal

logger = get_logger("app.main")

def temp_test_csv_reading():
    file_path: Path = Path(settings.catalog_data_path)
    products = csv_reader.read_products_from_csv(file_path)


def main():
    # Configurar logging
    setup_logging()
    logger: logging.Logger = get_logger(f"app.{__name__}")
    logger.info("Iniciando la aplicación...")
    verify_db_connection()
    init_db()
    update_portal()
    #temp_test_db_operations()
    #temp_test_csv_reading()
    



if __name__ == "__main__":
    main()