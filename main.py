# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from api import app as api_app  # Importa la aplicación desde api.py

# Crear la instancia principal
app = FastAPI(
    title="API de Proyecto Final",
    description="API para predicción de riesgo de incumplimiento en clientes de tarjetas de crédito.",
    version="0.1.0",
    openapi_url="/api/v1/openapi.json"  # URL de la documentación
)

# Montar las rutas de la API principal
app.mount("/", api_app)

# Ruta raíz personalizada
@app.get("/", response_class=HTMLResponse)
def read_root():
    """
    Página principal con el enlace a la documentación.
    """
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Bienvenido a la API de Proyecto Final</h1>"
        "<div>"
        "Accede a la documentación en: <a href='/docs'>Swagger UI</a><br>"
        "Revisa el estado de salud en: <a href='/health'>/health</a><br>"
        "Realiza predicciones en: <a href='/predict'>/predict</a>"
        "</div>"
        "</body>"
        "</html>"
    )
    return body


