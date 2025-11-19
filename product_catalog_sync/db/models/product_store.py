from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from product_catalog_sync.db.base import Base

class ProductStore(Base):
    __tablename__ = "product_store"

    product_id = Column(Integer, ForeignKey("products.product_id"), primary_key=True)
    store_id = Column(Integer, ForeignKey("stores.store_id"), primary_key=True)

    product = relationship("Product", back_populates="stores")
    store = relationship("Store", back_populates="products")
