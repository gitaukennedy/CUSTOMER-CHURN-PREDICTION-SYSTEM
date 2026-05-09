import streamlit as st
import requests

st.set_page_config(page_title="Customer Churn Predictor", layout="centered")

st.title("📉 Customer Churn Prediction App")

st.write("Enter customer information below to predict churn risk.")

# Inputs
gender = st.selectbox("Gender", ["Male", "Female"])

senior = st.selectbox("Senior Citizen", [0, 1])

partner = st.selectbox("Partner", ["Yes", "No"])

dependents = st.selectbox("Dependents", ["Yes", "No"])

tenure = st.slider("Tenure (Months)", 0, 72, 12)

phone = st.selectbox("Phone Service", ["Yes", "No"])

multiple = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])

internet = st.selectbox(
    "Internet Service",
    ["DSL", "Fiber optic", "No"]
)

security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])

backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])

protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])

support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])

tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])

movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])

contract = st.selectbox(
    "Contract",
    ["Month-to-month", "One year", "Two year"]
)

paperless = st.selectbox("Paperless Billing", ["Yes", "No"])

payment = st.selectbox(
    "Payment Method",
    [
        "Electronic check",
        "Mailed check",
        "Bank transfer (automatic)",
        "Credit card (automatic)"
    ]
)

monthly = st.number_input("Monthly Charges", 0.0, 500.0, 70.0)

total = st.number_input("Total Charges", 0.0, 10000.0, 1000.0)

# Predict button
if st.button("Predict Churn"):

    url = "http://127.0.0.1:8000/predict"

    payload = {
        "gender": gender,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone,
        "MultipleLines": multiple,
        "InternetService": internet,
        "OnlineSecurity": security,
        "OnlineBackup": backup,
        "DeviceProtection": protection,
        "TechSupport": support,
        "StreamingTV": tv,
        "StreamingMovies": movies,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly,
        "TotalCharges": total
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()

        st.subheader("Prediction Result")
        st.success(result["prediction"])
        st.metric(
            "Churn Probability",
            f"{result['churn_probability'] * 100:.1f}%"
        )
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to the API. Ensure FastAPI is running at {url}")