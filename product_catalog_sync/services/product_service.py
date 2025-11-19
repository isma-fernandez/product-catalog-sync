from sqlalchemy.orm import Session
from product_catalog_sync.utils.logging import get_logger
from product_catalog_sync.db.models.product import Product
from product_catalog_sync.schemas.product_input import ProductInput
from product_catalog_sync.repositories import product_repository, store_repository, product_store_repository


logger = get_logger(__name__)
db_logger = get_logger(f"{__name__}.db")


def process_one_product(db: Session, product: ProductInput) -> None:
    logger.debug(f"Procesando producto: {product}")

    product_db: Product = product_repository.get_product(db, product.product_id)

    if not product_db:
        db_logger.info(f"INSERT product {product.product_id} ({product.title}) price={product.price}")
        product_db = product_repository.create_product(
            db, product_id=product.product_id,
            title=product.title, price=product.price
        )
        _assign_stores_to_product(db, product_db, product.store_id)
        
    else:
        if _is_product_changed(product_db, product):
            db_logger.info(f"UPDATE product {product.product_id} ({product.title}) price={product.price}")
            product_repository.update_product(
                product_db, title=product.title, price=product.price
            )
    
    _sync_product_stores(db, product_db, product.store_id)


def _assign_stores_to_product(db: Session, product: Product, store_ids: set[int]) -> None:
    for store_id in store_ids:
        store = store_repository.get_or_create_store(db, store_id)
        db_logger.info(f"INSERT product_store ({product.product_id}, {store.store_id})")
        product_store_repository.add_product_store(db, product.product_id, store.store_id)


def _is_product_changed(product_db: Product, product_input: ProductInput) -> bool:
    return (product_db.title != product_input.title) or (product_db.price != product_input.price)


def _sync_product_stores(db: Session, product: Product, store_ids: set[int]) -> None:
    db_stores = product_store_repository.get_product_stores(db, product.product_id)
    db_store_ids = {ps.store_id for ps in db_stores}

    stores_to_add = store_ids - db_store_ids
    stores_to_remove = db_store_ids - store_ids

    for store_id in stores_to_add:
        store = store_repository.get_or_create_store(db, store_id)
        db_logger.info(f"INSERT product_store ({product.product_id}, {store.store_id})")
        product_store_repository.add_product_store(db, product.product_id, store.store_id)

    for store_id in stores_to_remove:
        db_logger.info(f"DELETE product_store ({product.product_id}, {store_id})")
        product_store_repository.delete_product_store_by_ids(db, product.product_id, store_id)
