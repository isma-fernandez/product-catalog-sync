from sqlalchemy.orm import Session
from src.db.product import Product

def get_all_products(db: Session) -> list[Product]:
    """
    Recupera todos los productos de la base de datos
    """
    return db.query(Product).all()

def get_product_by_PK(db: Session, product_id: int, store_id: int) -> Product | None:
    """
    Recupera un producto por su ID y store_id
    """
    return db.query(Product).filter(Product.product_id == product_id, Product.store_id == store_id).first()

def get_product_by_id(db: Session, product_id: int) -> list[Product] | None:
    """
    Recupera un producto por su ID
    """
    return db.query(Product).filter(Product.product_id == product_id).all()

def create_product(db: Session, product: Product) -> Product:
    """
    Crea un nuevo producto en la base de datos
    """
    db.add(product)
    return product

def delete_product(db: Session, product: Product) -> None:
    """
    Elimina un producto de la base de datos
    """
    db.delete(product)

def update_product(db: Session, product: Product, updated_fields: dict) -> Product:
    """
    Actualiza un producto existente con los campos dados.
    """
    for field, value in updated_fields.items():
        setattr(product, field, value)
    return product