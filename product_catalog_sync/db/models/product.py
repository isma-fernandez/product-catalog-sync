from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from product_catalog_sync.db.base import Base

class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    stores = relationship(
        "ProductStore",
        back_populates="product",
        cascade="all, delete-orphan"
    )
