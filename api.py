# -*- coding: utf-8 -*-
import boto3
import pandas as pd
from fastapi import APIRouter
from pydantic import BaseModel
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

router = APIRouter()

# Configuración de S3
BUCKET_NAME = "proyecto-dvcstore-dsa-team4"
FILE_KEY = "files/md5/94/0b416bb13a9b24bb5c9e1589284005"

# Modelo y preprocesamiento
COLUMNAS_RELEVANTES = ["LIMIT_BAL", "AGE", "PAY_0", "SEX", "EDUCATION", "MARRIAGE"]
VALORES_POR_DEFECTO = {
    "LIMIT_BAL": 200000,
    "AGE": 35,
    "PAY_0": 0,
    "SEX": 2,
    "EDUCATION": 2,
    "MARRIAGE": 2,
}

# Variables globales
modelo = None
scaler = None

# Función para cargar datos desde S3
def cargar_datos_desde_s3():
    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_KEY)
    df = pd.read_csv(obj["Body"])
    return df

# Entrenar modelo al iniciar
try:
    df = cargar_datos_desde_s3()
    scaler = StandardScaler()
    df[COLUMNAS_RELEVANTES] = scaler.fit_transform(df[COLUMNAS_RELEVANTES])
    X = df[COLUMNAS_RELEVANTES]
    y = df["default.payment.next.month"]
    modelo = LogisticRegression(max_iter=500, penalty="l2", solver="saga")
    modelo.fit(X, y)
except Exception as e:
    print(f"Error: {e}")

# Esquema de entrada
class InputData(BaseModel):
    LIMIT_BAL: float
    AGE: float
    PAY_0: float
    SEX: int
    EDUCATION: int
    MARRIAGE: int

# Rutas
@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/predict")
def predict(data: InputData):
    if modelo is None:
        return {"error": "Modelo no entrenado."}
    nueva_data = pd.DataFrame([[data.LIMIT_BAL, data.AGE, data.PAY_0, data.SEX, data.EDUCATION, data.MARRIAGE]],
                              columns=COLUMNAS_RELEVANTES)
    nueva_data_scaled = scaler.transform(nueva_data)
    probabilidad = modelo.predict_proba(nueva_data_scaled)[0][1]
    riesgo = "BAJO" if probabilidad <= 0.35 else "MEDIO" if probabilidad <= 0.65 else "ALTO"
    return {"probabilidad": probabilidad, "riesgo": riesgo}