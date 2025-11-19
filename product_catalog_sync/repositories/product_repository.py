from sqlalchemy.orm import Session
from product_catalog_sync.db.models.product import Product

def get_all_products(db: Session) -> list[Product]:
    return db.query(Product).all()

def get_product(db: Session, product_id: int) -> Product | None:
    return db.query(Product).filter(Product.product_id == product_id).first()

def create_product(db: Session, product_id: int, title: str, price: float) -> Product:
    product = Product(
        product_id=product_id,
        title=title,
        price=price
    )
    db.add(product)
    return product

def update_product(product: Product, title: str, price: float) -> Product:
    product.title = title
    product.price = price
    return product

def delete_product(db: Session, product: Product):
    db.delete(product)
