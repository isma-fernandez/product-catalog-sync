from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from src.db.base import engine
from src.utils.logging import get_logger
import sys

logger = get_logger("app.db")

def verify_db_connection() -> None:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Conexión a la base de datos OK.")
    except SQLAlchemyError:
        logger.error("No se puede conectar a la base de datos. (Mira los logs para más detalles)", exc_info=True)
        sys.exit(1)