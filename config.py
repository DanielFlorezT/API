import logging
import sys
from typing import List
from pydantic import BaseSettings, AnyHttpUrl
from loguru import logger

# Configuración de la API y logging
class LoggingSettings(BaseSettings):
    LOGGING_LEVEL: int = logging.INFO  # Nivel de logging

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"  # Ruta base para la API
    PROJECT_NAME: str = "Banckchurn API"  # Nombre del proyecto

    # Configuración CORS (para permitir peticiones desde ciertos orígenes)
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://localhost:3000",
        "https://localhost:8000",
    ]

    # Clase interna para sensibilidad a mayúsculas/minúsculas
    class Config:
        case_sensitive = True

# Configuración global de la aplicación
settings = Settings()

# Configuración del logger usando Loguru
def setup_app_logging(config: Settings) -> None:
    """Configura el logging para la aplicación."""
    logging.getLogger().handlers = [InterceptHandler()]
    logger.configure(handlers=[{"sink": sys.stderr, "level": config.LOGGING_LEVEL}])

class InterceptHandler(logging.Handler):
    """Intercepta mensajes de logging de otros módulos."""
    def emit(self, record: logging.LogRecord) -> None:
        logger.opt(exception=record.exc_info).log(record.levelname, record.getMessage())