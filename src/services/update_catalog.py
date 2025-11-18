import logging
from pathlib import Path
from src.utils.logging import get_logger
from src.services.csv_reader import read_products_from_csv
from src.config.app_config import settings
from src.schemas.product_input import ProductInput
from typing import List
from src.db import database

logger = get_logger(f"app.{__name__}")
db = database.create_session()

def update_catalog():
    logger.info("Actualizando el catálogo de productos...")
    products_from_csv: List[ProductInput] = read_products_from_csv(settings.catalog_data_path)
    
    if not products_from_csv:
        logger.warning("No se encontraron productos para actualizar.")
        return
    
    try:
        # TODO: Implementar la lógica de actualización del catálogo en la base de datos
        for product in products_from_csv:
            _process_one_product(product)
        database.commit_session(db)
    except Exception as e:
        logger.error(f"Error al actualizar el catálogo. Realizando rollback.", exc_info=True)
        db.rollback()
    finally:
        database.close_session(db)
        logger.info("Sesión de base de datos cerrada.")


    logger.info("Catálogo actualizado con éxito.")

def _process_one_product(product: ProductInput):
    """
    Procesa un solo producto leído desde el CSV.
    """
    logger.debug(f"Procesando producto: {product}")
    
    # CASOS:
    # 1. Si un producto ya existe, se debe actualizar la información.
    # 2. Si es nuevo, se inserta en la base de datos.
    # 3. Si el producto cambia de store/cuenta, realizar la reasignación.
    # NOTAS: Si la tienda no existe, se debe crear.