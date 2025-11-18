from src.models.base import init_db
from src.utils import logging
from src.utils.logging import setup_logging, get_logger

def main():
    # Configurar logging
    setup_logging()
    logger: logging.Logger = get_logger("app." + __name__)
    logger.info("Inicializando la base de datos...")
    # Inicializar la base de datos
    init_db()
    logger.info("Base de datos inicializada.")


if __name__ == "__main__":
    main()