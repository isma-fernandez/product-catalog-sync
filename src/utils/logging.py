import logging, logging.config
import os
from pathlib import Path
from src.config.app_config import settings

def setup_logging() -> None:
    """
    Configura el logging de la aplicación usando el archivo de configuración especificado en settings.
    Si el archivo no existe, configura un logging básico.
    """
    log_config_path: Path = settings.logging_config_file

    if log_config_path.exists():
        logging.config.fileConfig(log_config_path, disable_existing_loggers=False)
    else:
        logging.basicConfig(level=logging.INFO)
        logging.getLogger().warning(f"Archivo de configuración de logging no encontrado: {log_config_path}. Usando configuración básica.")

def get_logger(name: str) -> logging.Logger:
    """
    Devuelve un logger con el nombre especificado.
    """
    return logging.getLogger(name)

