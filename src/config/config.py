from pydantic import BaseSettings

class AppConfig(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    # Leer configuración desde archivo .env
    class Config:
        env_file = ".env"

settings = AppConfig()   
