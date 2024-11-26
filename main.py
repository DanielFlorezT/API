# -*- coding: utf-8 -*-
from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from loguru import logger
from config import settings, setup_app_logging
from api import app as api_app  # Importar las rutas de tu API

# Configurar logging antes de iniciar la aplicación
setup_app_logging(settings)

# Inicializar la aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Rutas principales
root_router = APIRouter()

@root_router.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Página de bienvenida."""
    html_content = """
    <html>
        <head>
            <title>Banckchurn API</title>
        </head>
        <body style="font-family: Arial, sans-serif;">
            <h1>Welcome to Banckchurn API</h1>
            <p>Check the documentation:</p>
            <ul>
                <li><a href="/docs">Swagger UI</a></li>
                <li><a href="/redoc">Redoc</a></li>
            </ul>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Incluir las rutas de la API
app.include_router(api_app.router, prefix=settings.API_V1_STR)
app.include_router(root_router)

# Configuración de CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if __name__ == "__main__":
    # Ejecutar la aplicación en modo desarrollo
    import uvicorn
    logger.warning("Iniciando la aplicación en modo desarrollo.")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
