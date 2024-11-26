# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from api import app as api_app  # Importa la aplicación desde api.py

# Crear la instancia principal
app = FastAPI(
    title="API de Proyecto Final",
    openapi_url="/api/v1/openapi.json",
    description="API para el proyecto final con endpoints para predicción y estado de salud.",
    version="0.1.0"
)

# Incluir las rutas de api.py
app.mount("/", api_app)  # Monta la aplicación de `api.py` en la raíz

# Página principal
@app.get("/", response_class=HTMLResponse)
def read_root():
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Bienvenido a la API de Proyecto Final</h1>"
        "<div>"
        "Accede a la documentación en: <a href='/docs'>Swagger UI</a><br>"
        "Revisa el estado de salud en: <a href='/health'>/health</a>"
        "</div>"
        "</body>"
        "</html>"
    )
    return body

