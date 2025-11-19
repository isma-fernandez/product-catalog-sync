import sys
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from product_catalog_sync.db.database import engine
from product_catalog_sync.utils.logging import get_logger


logger = get_logger(__name__)

def verify_db_connection() -> None:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Conexión a la base de datos OK.")
    except SQLAlchemyError as e:
        logger.error("No se puede conectar a la base de datos. (Mira los logs para más detalles)", exc_info=True)
        sys.exit(1)