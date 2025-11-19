import logging
import logging.config
from pathlib import Path
from product_catalog_sync.config.app_config import settings

logger = logging.getLogger("app.utils.logging")

def setup_logging() -> None:
    """
    Configura el logging de la aplicación usando el archivo de configuración especificado en settings.
    Si el archivo no existe, configura un logging básico.
    """
    log_config_path: Path = settings.logging_config_file

    # Asegurarse de que el directorio de logs exista
    logs_path = settings.logs_path
    logs_path.mkdir(parents=True, exist_ok=True)

    if log_config_path.exists():
        logging.config.fileConfig(log_config_path, disable_existing_loggers=False)
        logger.info(f"Logging configurado usando: {log_config_path}")
    else:
        logging.basicConfig(level=logging.INFO)
        logger.warning(f"Archivo de configuración de logging no encontrado: {log_config_path}. Usando configuración básica.")

def get_logger(name: str) -> logging.Logger:
    """
    Devuelve un logger con el nombre especificado.
    """
    return logging.getLogger(name)
