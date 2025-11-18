from sqlalchemy.orm import Session
from src.db.models.product_store import ProductStore

def get_product_stores(db: Session, product_id: int) -> list[ProductStore]:
    return db.query(ProductStore).filter(
        ProductStore.product_id == product_id
    ).all()

def get_product_store(db: Session, product_id: int, store_id: int) -> ProductStore | None:
    return db.query(ProductStore).filter(
        ProductStore.product_id == product_id,
        ProductStore.store_id == store_id
    ).first()

def add_product_store(db: Session, product_id: int, store_id: int) -> ProductStore:
    link = ProductStore(product_id=product_id, store_id=store_id)
    db.add(link)
    return link

def delete_product_store(db: Session, link: ProductStore):
    db.delete(link)
