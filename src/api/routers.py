from fastapi import APIRouter, Depends
from src.repositories.product_repository import get_all_products
from src.db.database import get_db