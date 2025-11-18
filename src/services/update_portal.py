import sys
from typing import List
from sqlalchemy.orm import Session
from src.utils.logging import get_logger
from src.services.csv_reader import read_products_from_csv
from src.config.app_config import settings
from src.schemas.product_input import ProductInput
from src.db import database
from src.services.product_service import process_one_product
from src.repositories import product_repository

logger = get_logger(f"app.{__name__}")
db_logger = get_logger(f"app.db.{__name__}")

def update_portal() -> None:
    logger.info("Actualizando el portal de productos...")
    products_from_csv: List[ProductInput] = read_products_from_csv(settings.portal_data_path)
    db: Session = database.create_session()

    if not products_from_csv:
        logger.warning("No se encontraron productos para actualizar.")
        return
    try:
        _delete_products_not_in_csv(db, products_from_csv)
        for product in products_from_csv:
            process_one_product(db, product)
            ...
        database.commit_session(db)
        db_logger.info("COMMIT portal aplicado correctamente")
    except Exception as e:
        logger.error(f"Error al actualizar el portal. Realizando rollback.", exc_info=True)
        db_logger.warning("ROLLBACK portal: se han revertido los cambios de la transacción")
        db.rollback()
        sys.exit(1)
    finally:
        database.close_session(db)
        logger.info("Sesión de base de datos cerrada.")

    logger.info("Portal actualizado con éxito.")

def _delete_products_not_in_csv(db: Session, products_in_csv: List[ProductInput]) -> None:
    csv_product_ids = {product.product_id for product in products_in_csv}
    all_products_db = product_repository.get_all_products(db)
    all_product_ids_db = {product.product_id for product in all_products_db}
    products_to_delete_ids = all_product_ids_db - csv_product_ids
    for product_id in products_to_delete_ids:
        product_db = product_repository.get_product(db, product_id)
        if product_db:
            db_logger.info(f"DELETE product {product_db.product_id} ({product_db.title})")
            product_repository.delete_product(db, product_db)
            logger.info(f"Producto eliminado: {product_db}")
