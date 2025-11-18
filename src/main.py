from src.db.base import init_db
from src.db.healthcheck import verify_db_connection
from src.utils import logging
from src.utils.logging import setup_logging, get_logger

def main():
    # Configurar logging
    setup_logging()
    logger: logging.Logger = get_logger(f"app.{__name__}")
    logger.info("Iniciando la aplicación...")
    
    # Inicializar la base de datos
    verify_db_connection()
    init_db()   

if __name__ == "__main__":
    main()