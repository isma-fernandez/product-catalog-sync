from src.db.database import init_db
from src.db.healthcheck import verify_db_connection
import logging
from src.utils.logging import setup_logging, get_logger
# DB Tests
from src.repositories import db_repository
from src.db import database
from src.db.product import Product

def main():
    # Configurar logging
    setup_logging()
    logger: logging.Logger = get_logger(f"app.{__name__}")
    logger.info("Iniciando la aplicación...")
    
    # Inicializar la base de datos
    verify_db_connection()
    init_db()   

    # Test db_repository
    logger.info("Probando operaciones de la base de datos...")
    db = database.create_session()
    new_product = Product(product_id=1,store_id=3,
                    title="Camiseta Azul",price=19.99)
    logger.info(f"Creando nuevo producto: {new_product}")
    db_repository.create_product(db, new_product)
    products = db_repository.get_all_products(db)
    logger.info(f"Productos en la base de datos: {products}")
    database.commit_session(db)
    database.close_session(db)


if __name__ == "__main__":
    main()