from fastapi import APIRouter, Depends
from product_catalog_sync.repositories.product_queries import get_all_products_with_stores
from product_catalog_sync.db.database import get_db
from product_catalog_sync.schemas.product_response import ProductResponse

router = APIRouter()

@router.get("/products", response_model=list[ProductResponse])
def read_products(db=Depends(get_db)):
    """
    Endpoint para obtener todos los productos con sus tiendas asociadas
    """
    products = get_all_products_with_stores(db)
    return products