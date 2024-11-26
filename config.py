import logging
import sys
from typing import List
from pydantic import BaseSettings, AnyHttpUrl
from loguru import logger

# Configuraci�n de la API y logging
class LoggingSettings(BaseSettings):
    LOGGING_LEVEL: int = logging.INFO  # Nivel de logging

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"  # Ruta base para la API
    PROJECT_NAME: str = "Banckchurn API"  # Nombre del proyecto

    # Configuraci�n CORS (para permitir peticiones desde ciertos or�genes)
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://localhost:3000",
        "https://localhost:8000",
    ]

    # Clase interna para sensibilidad a may�sculas/min�sculas
    class Config:
        case_sensitive = True

# Configuraci�n global de la aplicaci�n
settings = Settings()

# Configuraci�n del logger usando Loguru
def setup_app_logging(config: Settings) -> None:
    """Configura el logging para la aplicaci�n."""
    logging.getLogger().handlers = [InterceptHandler()]
    logger.configure(handlers=[{"sink": sys.stderr, "level": config.LOGGING_LEVEL}])

class InterceptHandler(logging.Handler):
    """Intercepta mensajes de logging de otros m�dulos."""
    def emit(self, record: logging.LogRecord) -> None:
        logger.opt(exception=record.exc_info).log(record.levelname, record.getMessage())