import argparse
from pathlib import Path
from product_catalog_sync.db.database import init_db
from product_catalog_sync.db.healthcheck import verify_db_connection
from product_catalog_sync.utils.logging import setup_logging, get_logger
from product_catalog_sync.services.update_portal import update_portal
from product_catalog_sync.services.update_catalog import update_catalog
from product_catalog_sync.config.app_config import settings

logger = get_logger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", action="store_true", help="Actualiza el catálogo desde un archivo")
    parser.add_argument("--portal", action="store_true", help="Actualiza el portal desde un archivo")
    parser.add_argument("--file", type=str, help="Ruta del archivo a procesar (opcional)")
    parser.add_argument("--initdb", action="store_true", help="Inicializa la base de datos")
    args = parser.parse_args()

    setup_logging()
    logger.info("Configuración de logging completada.")

    verify_db_connection()
    if args.initdb:
        logger.info("Inicializando la base de datos...")
        init_db()
    else:
        logger.info("Iniciando la aplicación...")
    if args.file:
        settings.catalog_data_path = Path(args.file)
        settings.portal_data_path = Path(args.file)

    if args.catalog:
        update_catalog()
    elif args.portal:
        update_portal()
    elif not args.initdb:
        logger.error("No se especificó ninguna acción. Usa --catalog o --portal.")

if __name__ == "__main__":
    main()