from pydantic_settings import BaseSettings
from pathlib import Path

class AppConfig(BaseSettings):
    # Configuraciones de la base de datos
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str
    api_port: int = 8000

    # Ruta configuración del logging
    logging_config_file: Path = Path("product_catalog_sync/config/logging.conf")

    # Ruta de los datos
    data_path: Path = Path("data")
    catalog_data_path: Path = data_path / "feed_items.csv"
    portal_data_path: Path = data_path / "portal_items.csv"

    # Ruta de los logs
    logs_path: Path = Path("logs")

    # Leer configuración desde archivo .env
    class Config:
        env_file = ".env"

settings = AppConfig()
