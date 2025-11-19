from sqlalchemy import select, func
from src.db.models.product import Product
from src.db.models.product_store import ProductStore

def get_all_products_with_stores(db):
    """
    Obtiene todos los productos junto con las tiendas asociadas
    """
    query = (
        select(
            Product.product_id,
            Product.title,
            Product.price,
            func.array_agg(ProductStore.store_id).label("stores")
        )
        .join(ProductStore, Product.product_id == ProductStore.product_id)
        .group_by(Product.product_id)
    )

    return db.execute(query).mappings().all()
