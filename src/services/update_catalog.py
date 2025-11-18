import sys
from typing import List
from sqlalchemy.orm import Session
from src.utils.logging import get_logger
from src.services.csv_reader import read_products_from_csv
from src.config.app_config import settings
from src.schemas.product_input import ProductInput
from src.db import database
from src.services.product_service import process_one_product

logger = get_logger(f"app.{__name__}")
db_logger = get_logger(f"app.db.{__name__}")

def update_catalog() -> None:
    logger.info("Actualizando el catálogo de productos...")
    products_from_csv: List[ProductInput] = read_products_from_csv(settings.catalog_data_path)
    db: Session = database.create_session()

    if not products_from_csv:
        logger.warning("No se encontraron productos para actualizar.")
        return
    try:
        for product in products_from_csv:
            process_one_product(db, product)
        database.commit_session(db)
        db_logger.info("COMMIT catálogo aplicado correctamente")
    except Exception as e:
        logger.error(f"Error al actualizar el catálogo. Realizando rollback.", exc_info=True)
        db_logger.warning("ROLLBACK catálogo: se han revertido los cambios de la transacción")
        db.rollback()
        sys.exit(1)
    finally:
        database.close_session(db)
        logger.info("Sesión de base de datos cerrada.")

    logger.info("Catálogo actualizado con éxito.")
