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
from sqlalchemy.orm import Session
import sys

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
            _process_one_product(db, product)
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


def _process_one_product(db:Session, product: ProductInput)-> None:
    logger.debug(f"Procesando producto: {product}")

    product_db: Product = product_repository.get_product(db, product.product_id)
    if not product_db:
        db_logger.info(f"INSERT product {product.product_id} ({product.title}) price={product.price}")
        product_db = product_repository.create_product(
            db, product_id=product.product_id,
            title=product.title, price=product.price
        )
        _assign_stores_to_product(db, product_db, product.store_id)
        logger.info(f"Producto creado: {product_db}")
    else:
        if _is_product_changed(product_db, product):
            db_logger.info(f"UPDATE product {product.product_id} ({product.title}) price={product.price}")
            product_repository.update_product(
                product_db, title=product.title,
                price=product.price
            )
            logger.info(f"Producto actualizado: {product_db}")
        else:
            logger.debug(f"No hay cambios para el producto {product.product_id}")
    
    _sync_product_stores(db, product_db, product.store_id)

def _assign_stores_to_product(db: Session, product: Product, store_ids: set[int]) -> None:
    for store_id in store_ids:
        store: Store = store_repository.get_or_create_store(db, store_id)
        db_logger.info(f"INSERT product_store ({product.product_id}, {store.store_id})")
        product_store_repository.add_product_store(db, product.product_id, store.store_id)
        logger.info(f"Tienda creada: {store}")
        logger.info(f"Asignada tienda {store.store_id} al producto {product.product_id}")

def _is_product_changed(product_db: Product, product_input: ProductInput) -> bool:
    return (product_db.title != product_input.title) or (product_db.price != product_input.price)

def _sync_product_stores(db: Session, product: Product, store_ids: set[int]) -> None:
    db_stores = product_store_repository.get_product_stores(db, product.product_id)
    db_store_ids = {ps.store_id for ps in db_stores}

    stores_to_add = store_ids - db_store_ids
    stores_to_remove = db_store_ids - store_ids

    for store_id in stores_to_add:
        store: Store = store_repository.get_or_create_store(db, store_id)
        db_logger.info(f"INSERT product_store ({product.product_id}, {store.store_id})")
        product_store_repository.add_product_store(db, product.product_id, store.store_id)
        logger.info(f"Asignada tienda {store.store_id} al producto {product.product_id}")

    for store_id in stores_to_remove:
        db_logger.info(f"DELETE product_store ({product.product_id}, {store_id})")
        product_store_repository.delete_product_store_by_ids(db, product.product_id, store_id)
        logger.info(f"Eliminada tienda {store_id} del producto {product.product_id}")
