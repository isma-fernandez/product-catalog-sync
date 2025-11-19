import csv
from pathlib import Path
from typing import List
from pydantic import ValidationError
from product_catalog_sync.schemas.product_input import ProductInput
from product_catalog_sync.utils.logging import get_logger
import sys


logger = get_logger(__name__)

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
                    logger.info(f"Producto leído: {product}")
                    products.append(product)
                except ValidationError as e:
                    logger.error(f"""Validación fallida para el producto con id {row['product_id']} 
                                 en fila {reader.line_num}: {e.errors()}""", exc_info=True)
                    continue
                except Exception as e:
                    logger.error(f"""Error inesperado al procesar el producto con id {row['product_id']} 
                                 en fila""", exc_info=True)
                    continue
    except FileNotFoundError:
        logger.error(f"Archivo no encontrado en {file_path}", exc_info=True)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error al leer el archivo CSV", exc_info=True)
        sys.exit(1)

    logger.info(f"Se leyeron {len(products)} productos del archivo CSV.")
    print(products)
    return products