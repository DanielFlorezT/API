from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from loguru import logger
from config import settings, setup_app_logging
from api import app as api_app  # Importa tu API definida en api.py

# Configurar logging antes de inicializar la aplicación
setup_app_logging(settings)

# Inicializar FastAPI con configuración personalizada
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Definir rutas para la raíz y otras funcionalidades
root_router = APIRouter()

@root_router.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Página de bienvenida personalizada."""
    html_content = """
    <html>
        <head>
            <title>Welcome to Banckchurn API</title>
        </head>
        <body style='font-family: Arial, sans-serif;'>
            <h1>Welcome to Banckchurn API</h1>
            <p>Check the docs: <a href="/docs">here</a></p>
            <p>Swagger UI: <a href="/docs">Swagger</a></p>
            <p>Redoc: <a href="/redoc">Redoc</a></p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

# Incluir las rutas de la API desde api.py
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
    # Ejecutar el servidor en modo desarrollo
    import uvicorn
    logger.warning("Iniciando en modo desarrollo.")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")