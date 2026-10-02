from pathlib import Path

import joblib
import pandas as pd

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


# ============================================================
# 1. PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "house_price_model.pkl"
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"


# ============================================================
# 2. CREATE FASTAPI APP
# ============================================================

app = FastAPI(
    title="House Price Prediction System",
    description="House Price Prediction using Machine Learning and FastAPI",
    version="1.0"
)


# ============================================================
# 3. CHECK REQUIRED FILES
# ============================================================

print("----------------------------------------")
print("HOUSE PRICE PREDICTION SYSTEM")
print("----------------------------------------")

print("Project folder:", BASE_DIR)
print("Model file:", MODEL_PATH)
print("Model exists:", MODEL_PATH.exists())
print("Templates folder exists:", TEMPLATE_DIR.exists())
print("Static folder exists:", STATIC_DIR.exists())


# ============================================================
# 4. LOAD MACHINE LEARNING MODEL
# ============================================================

if not MODEL_PATH.exists():

    raise FileNotFoundError(
        f"\nModel file not found:\n{MODEL_PATH}\n\n"
        "Please run this command first:\n"
        "python train_model.py"
    )


model = joblib.load(MODEL_PATH)

print("Model loaded successfully!")


# ============================================================
# 5. STATIC FILES
# ============================================================

if STATIC_DIR.exists():

    app.mount(
        "/static",
        StaticFiles(directory=str(STATIC_DIR)),
        name="static"
    )

else:

    print("WARNING: static folder not found!")


# ============================================================
# 6. HTML TEMPLATES
# ============================================================

templates = Jinja2Templates(
    directory=str(TEMPLATE_DIR)
)


# ============================================================
# 7. HOUSE DATA MODEL
# ============================================================

class HouseData(BaseModel):

    area: float
    bedrooms: int
    bathrooms: int
    floors: int
    age: float


# ============================================================
# 8. HOME PAGE
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# ============================================================
# 9. TEST ROUTE
# ============================================================

@app.get("/test")
async def test():

    return {
        "message": "FastAPI is working"
    }


# ============================================================
# 10. HEALTH CHECK
# ============================================================

@app.get("/health")
async def health():

    return {
        "status": "API is running",
        "model_loaded": True
    }


# ============================================================
# 11. HOUSE PRICE PREDICTION
# ============================================================

@app.post("/predict")
async def predict(data: HouseData):

    # Create DataFrame
    input_data = pd.DataFrame(
        [[
            data.area,
            data.bedrooms,
            data.bathrooms,
            data.floors,
            data.age
        ]],
        columns=[
            "area",
            "bedrooms",
            "bathrooms",
            "floors",
            "age"
        ]
    )


    # Make prediction
    prediction = model.predict(input_data)


    # Convert prediction to number
    predicted_price = round(
        float(prediction[0]),
        2
    )


    # Return result
    return {
        "success": True,
        "predicted_price": predicted_price,
        "message": "House price predicted successfully"
    }

