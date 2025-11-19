from sqlalchemy.orm import declarative_base, DeclarativeMeta

Base: DeclarativeMeta = declarative_base()

# Necesario para registrar los modelos
from src.db.models.product import Product
from src.db.models.store import Store
from src.db.models.product_store import ProductStore