from pydantic import BaseModel
from typing import List

class ProductResponse(BaseModel):
    product_id: int
    title: str
    price: float
    stores: List[int]

    class Config:
        orm_mode = True
