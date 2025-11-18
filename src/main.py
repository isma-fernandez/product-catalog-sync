import argparse
from src.db.database import init_db
from src.db.healthcheck import verify_db_connection
from src.utils.logging import setup_logging, get_logger
from src.services.update_portal import update_portal
from src.services.update_catalog import update_catalog

logger = get_logger("app.main")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", action="store_true")
    parser.add_argument("--portal", action="store_true")
    args = parser.parse_args()

    setup_logging()
    logger.info("Iniciando la aplicación...")

    verify_db_connection()
    init_db()
    
    if args.catalog:
        update_catalog()
    elif args.portal:
        update_portal()
    else:
        logger.error("No se especificó ninguna acción. Usa --catalog o --portal.")

if __name__ == "__main__":
    main()