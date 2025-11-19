from sqlalchemy.orm import declarative_base, DeclarativeMeta

Base: DeclarativeMeta = declarative_base()

# Necesario para registrar los modelos
from product_catalog_sync.db.models.product import Product
from product_catalog_sync.db.models.store import Store
from product_catalog_sync.db.models.product_store import ProductStore