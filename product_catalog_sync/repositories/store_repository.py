from sqlalchemy.orm import Session
from product_catalog_sync.db.models.store import Store

def get_store(db: Session, store_id: int) -> Store | None:
    return db.query(Store).filter(Store.store_id == store_id).first()

def get_or_create_store(db: Session, store_id: int) -> Store:
    store = get_store(db, store_id)
    if not store:
        store = create_store(db, store_id)
    return store

def create_store(db: Session, store_id: int) -> Store:
    store = Store(store_id=store_id)
    db.add(store)
    return store