from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.db.healthcheck import verify_db_connection
from src.api.routers import router 
from src.utils.logging import setup_logging, get_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Operaciones de inicio y cierre de la aplicación FastAPI
    """
    setup_logging()
    logger = get_logger("app.api")
    logger.info("Inicializando aplicación FastAPI...")

    verify_db_connection()

    yield 

    logger.info("Cerrando aplicación FastAPI...")

app = FastAPI(title="Product Catalog Sync API", version="1.0.0", lifespan=lifespan)

app.include_router(router, prefix="/api")