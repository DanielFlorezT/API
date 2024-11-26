# -*- coding: utf-8 -*-
# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import app as api_app  # Importar desde api.py
from config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar rutas de API
app.mount("/", api_app)

