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
                product = _validate_product_data(row, reader)
                if product:  
                    products.append(product)

    except FileNotFoundError:
        logger.error(f"Archivo no encontrado en {file_path}", exc_info=True)
        sys.exit(1)

    except Exception:
        logger.error("Error al leer el archivo CSV", exc_info=True)
        sys.exit(1)

    logger.info(f"Se leyeron {len(products)} productos del archivo CSV.")
    print(products)
    return products


def _validate_product_data(row: dict, reader: csv.DictReader) -> ProductInput:
    """ 
    Valida los datos del producto usando el schema ProductInput. 
    """
    try:
        # Filas vacías
        if _is_row_empty(row):
            logger.error(f"Fila vacía o inválida en el CSV en la línea {reader.line_num}")
            return None

        # Filas con columnas extra
        if None in row:
            logger.error(f"Fila con columnas extra en la línea {reader.line_num}: {row[None]}")
            return None

        # Eliminar carácteres BOM
        row = {k: (v or "").replace("\ufeff", "").strip() for k, v in row.items()}

        # Validar usando Pydantic
        product = ProductInput(**row)
        logger.info(f"Producto leído: {product}")
        return product
    
    except ValidationError as e:
        logger.error(f"Validación fallida para los datos del producto: {row.get('product_id', '')}", exc_info=True)
        return None
    
    except Exception:
        logger.error(
            f"Error inesperado al procesar el producto con id {row.get('product_id', '')} "
            f"en fila {reader.line_num}",
            exc_info=True
        )
        return None


def _is_row_empty(row: dict) -> bool:
    """ 
    Verifica si una fila del CSV está vacía o contiene solo espacios en blanco. 
    """
    return all(not(v or "").strip() for v in row.values() if isinstance(v, str))
