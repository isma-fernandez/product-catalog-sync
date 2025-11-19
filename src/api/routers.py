from fastapi import APIRouter, Depends
from src.repositories.product_queries import get_all_products_with_stores
from src.db.database import get_db
from src.schemas.product_response import ProductResponse

router = APIRouter()

@router.get("/products", response_model=list[ProductResponse])
def read_products(db=Depends(get_db)):
    """
    Endpoint para obtener todos los productos con sus tiendas asociadas
    """
    products = get_all_products_with_stores(db)
    return products