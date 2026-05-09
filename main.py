from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# Load model and columns
model = joblib.load("model.pkl")
columns = joblib.load("columns.pkl")

app = FastAPI(title="Customer Churn Prediction API")


# Input schema
class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: int
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float


@app.get("/")
def home():
    return {"message": "Customer Churn API Running"}


@app.post("/predict")
def predict(data: CustomerData):

    # Convert input to dataframe
    input_dict = data.model_dump()

    df = pd.DataFrame([input_dict])

    # One-hot encode
    df = pd.get_dummies(df)

    # Match training columns
    df = df.reindex(columns=columns, fill_value=0)

    # Predict
    prediction = model.predict(df)[0]

    probability = model.predict_proba(df)[0][1]

    result = "Customer Will Churn" if prediction == 1 else "Customer Will Stay"

    return {
        "prediction": result,
        "churn_probability": round(float(probability), 3)
    }