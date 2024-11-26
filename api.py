# -*- coding: utf-8 -*-
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

app = FastAPI()  # Define el objeto 'app' aquí

# Variables globales
modelo = None
scaler = None
COLUMNAS_RELEVANTES = ["LIMIT_BAL", "AGE", "PAY_0", "SEX", "EDUCATION", "MARRIAGE"]

# Clase para datos de entrada
class InputData(BaseModel):
    LIMIT_BAL: float
    AGE: float
    PAY_0: float
    SEX: int
    EDUCATION: int
    MARRIAGE: int

@app.get("/health")
def health():
    return {"status": "OK"}

@app.post("/predict")
def predict(data: InputData):
    global modelo, scaler
    try:
        if modelo is None or scaler is None:
            return {"error": "Modelo no está entrenado. Revisa los logs."}
        
        # Transformar datos
        nueva_data = pd.DataFrame([[
            data.LIMIT_BAL, data.AGE, data.PAY_0,
            data.SEX, data.EDUCATION, data.MARRIAGE
        ]], columns=COLUMNAS_RELEVANTES)
        
        nueva_data_scaled = scaler.transform(nueva_data)
        probabilidad = modelo.predict_proba(nueva_data_scaled)[0][1]
        riesgo = (
            "BAJO" if probabilidad <= 0.35
            else "MEDIO" if probabilidad <= 0.65
            else "ALTO"
        )
        
        return {"probabilidad": round(probabilidad, 2), "riesgo": riesgo}
    except Exception as e:
        return {"error": f"No se pudo procesar la prediccion: {e}"}
