from fastapi import FastAPI, HTTPException
from sklearn.datasets import load_wine
import joblib
import os

app = FastAPI()

model = joblib.load('model.joblib')
wine = load_wine()
feature_names = list(wine.feature_names)

APP_VERSION = os.environ.get('APP_VERSION', 'dev')
MODEL_NAME = os.environ.get('MODEL_NAME', 'wine-classifier')

@app.get("/")
def root():
    return {
        "message": "Wine classification API",
        "app_version": APP_VERSION,
        "model_name": MODEL_NAME
    }

@app.post("/predict")
def predict(data: dict):
    if "features" not in data:
        raise HTTPException(status_code=400, detail="Brak wymaganej wartosci 'features'")

    features = data["features"]

    if not isinstance(features, list):
        raise HTTPException(status_code=400, detail="'features' musi byc lista")

    if len(features) != len(feature_names):
        raise HTTPException(
            status_code=400,
            detail=f"Oczekiwano {len(feature_names)} cech, otrzymano {len(features)}"
        )

    try:
        features = [float(x) for x in features]
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Wszystkie cechy musza byc liczbami")

    prediction = model.predict([features])

    return {"prediction": int(prediction[0]), "app_version": APP_VERSION}

@app.get("/info")
def info():
    return {
        "model_type": type(model).__name__,
        "model_name": MODEL_NAME,
        "app_version": APP_VERSION,
        "n_features": len(feature_names),
        "feature_names": feature_names,
        "classes": [int(c) for c in model.classes_]
    }

@app.get("/health")
def health():
    return {"status": "ok"}