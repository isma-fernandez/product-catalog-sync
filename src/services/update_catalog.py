import logging
from pathlib import Path
from src.utils.logging import get_logger
from src.services.csv_reader import read_products_from_csv
from src.config.app_config import settings
from src.schemas.product_input import ProductInput
from typing import List
from src.db import database
from src.db.models.product import Product
from src.db.models.store import Store
from src.db.models.product_store import ProductStore
from src.repositories import product_repository, store_repository, product_store_repository

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
    # 1. Si es nuevo, se inserta en la base de datos.
    product_db: Product = product_repository.get_product(db, product.product_id)
    if not product_db:
        product_db = product_repository.create_product(db, Product(
            product_id=product.product_id,
            title=product.title,
            price=product.price
        ))
        _assign_stores_to_product(product_db, product.store_ids)
        logger.info(f"Producto creado: {product_db}")
    else:
        ...
        # TODO: Actualizar el producto si hay cambios en title o price
    # 2. Si un producto ya existe, se debe actualizar la información.
    
    # 3. Si el producto cambia de store/cuenta, realizar la reasignación.
    # NOTAS: Si la tienda no existe, se debe crear.

def _assign_stores_to_product(product: Product, store_ids: List[int]):
    """
    Asigna las tiendas a un producto, creando las relaciones necesarias.
    """
    for store_id in store_ids:
        store: Store = store_repository.get_store(db, store_id)
        if not store:
            store = store_repository.create_store(db, store_id)
        product_store_repository.add_product_store(db, product.product_id, store.store_id)
        logger.info(f"Tienda creada: {store}")
        logger.info(f"Asignada tienda {store.store_id} al producto {product.product_id}")
            
            