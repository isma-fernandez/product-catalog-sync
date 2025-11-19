from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from product_catalog_sync.db.base import Base

class Store(Base):
    __tablename__ = "stores"

    store_id = Column(Integer, primary_key=True, index=True)

    products = relationship(
        "ProductStore",
        back_populates="store",
        cascade="all, delete-orphan"
    )
