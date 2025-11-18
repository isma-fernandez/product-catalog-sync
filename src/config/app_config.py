from pydantic_settings import BaseSettings
from pathlib import Path

class AppConfig(BaseSettings):
    # Configuraciones de la base de datos
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    # Ruta configuración del logging
    logging_config_file: Path = Path("src/config/logging.conf")

    # Leer configuración desde archivo .env
    class Config:
        env_file = ".env"

settings = AppConfig()
