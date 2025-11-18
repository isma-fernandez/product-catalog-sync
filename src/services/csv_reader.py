import csv
from pathlib import Path
from src.schemas.product_input import ProductInput
from src.utils.logging import get_logger
from typing import List
from pydantic import ValidationError

logger = get_logger(f"app.{__name__}")

def read_products_from_csv(file_path: Path) -> List[ProductInput]:
    """
    Lee productos desde un archivo CSV y los valida usando el schema ProductInput.
    """
    products: List[ProductInput] = []
    try:
        with file_path.open(mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    product = ProductInput(**row)
                    products.append(product)
                except ValidationError as e:
                    logger.error(f"Validación fallida para el producto {row}: {e.errors()}", exc_info=True)
                except Exception as e:
                    logger.error(f"Error inesperado al procesar el producto {row}: {e}", exc_info=True)
    except FileNotFoundError:
        logger.error(f"Archivo no encontrado en {file_path}", exc_info=True)
    except Exception as e:
        logger.error(f"Error al leer el archivo CSV: {e}", exc_info=True)

    logger.info(f"Se leyeron {len(products)} productos del archivo CSV.")
    return products