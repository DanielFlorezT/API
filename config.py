# -*- coding: utf-8 -*-
import logging
import sys
from typing import List
from pydantic_settings import BaseSettings  # Cambiado a pydantic-settings
from pydantic import AnyHttpUrl
from loguru import logger

# Configuración de logging
class LoggingSettings(BaseSettings):
    LOGGING_LEVEL: int = logging.INFO  # Nivel de logging predeterminado

# Configuración general del proyecto
class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"  # Prefijo para los endpoints
    PROJECT_NAME: str = "Banckchurn API"
    
    # Configuración de CORS: Permitir orígenes específicos para desarrollo o producción
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:8000",  # Desarrollo local
        "http://localhost:3000",
    ]

    logging: LoggingSettings = LoggingSettings()  # Configuración del logging

    class Config:
        case_sensitive = True

# Configuración de loggers personalizados
class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)
        logger.opt(depth=2, exception=record.exc_info).log(level, record.getMessage())

def setup_app_logging(config: Settings) -> None:
    """Configura el logging de la aplicación."""
    logging.getLogger().handlers = [InterceptHandler()]
    logger.configure(handlers=[{"sink": sys.stderr, "level": config.logging.LOGGING_LEVEL}])

# Instancia global de configuración
settings = Settings()

