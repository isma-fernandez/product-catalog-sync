import sys
from typing import List
from sqlalchemy.orm import Session
from product_catalog_sync.utils.logging import get_logger
from product_catalog_sync.services.csv_reader import read_products_from_csv
from product_catalog_sync.config.app_config import settings
from product_catalog_sync.schemas.product_input import ProductInput
from product_catalog_sync.db import database
from product_catalog_sync.services.product_service import process_one_product

logger = get_logger(__name__)
db_logger = get_logger(f"{__name__}.db")

def update_catalog() -> None:
    logger.info("Actualizando el catálogo de productos...")
    products_from_csv: List[ProductInput] = read_products_from_csv(settings.catalog_data_path)
    
    if not products_from_csv:
        logger.warning("No se encontraron productos para actualizar.")
        return
    
    db: Session = database.create_session()
    try:
        for product in products_from_csv:
            process_one_product(db, product)
        database.commit_session(db)
        db_logger.info("COMMIT catálogo aplicado correctamente")

    except Exception as e:
        logger.error(f"Error al actualizar el catálogo. Realizando rollback.", exc_info=True)
        logger.error(f"Ver detalles en los logs.")
        db_logger.warning("ROLLBACK catálogo: se han revertido los cambios de la transacción")
        db.rollback()
        sys.exit(1)

    finally:
        database.close_session(db)
        logger.info("Sesión de base de datos cerrada.")

    logger.info("Catálogo actualizado con éxito.")
