from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

print("API KEY LOADED:", API_KEY is not None)

genai.configure(api_key=API_KEY)

gemini_model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# ==========================
# LOAD MODELS
# ==========================

segment_model = joblib.load("../models/kmeans.pkl")
spending_model = joblib.load("../models/spending_model.pkl")
subscription_model = joblib.load("../models/subscription_model.pkl")

# ==========================
# FASTAPI APP
# ==========================

app = FastAPI(
    title="Customer Intelligence API",
    version="2.0.0",
    description="Customer Segmentation + Spending Prediction + Subscription Prediction"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================
# SEGMENT NAMES
# ==========================

segment_names = {
    0: "Premium Loyal Customers",
    1: "Low-Spend Senior Customers",
    2: "Young Satisfied Shoppers",
    3: "High-Spend Occasional Buyers",
    4: "Loyal Repeat Customers",
    5: "Frequent Active Buyers"
}

# ==========================
# REQUEST SCHEMAS
# ==========================

class SegmentRequest(BaseModel):
    age: int
    purchase_amount: float
    review_rating: float
    previous_purchases: int
    purchases_per_year: float


class SpendingRequest(BaseModel):
    age: int
    gender: str
    category: str
    season: str
    review_rating: float
    subscription_status: str
    previous_purchases: int
    purchase_frequency_days: int

class SubscriptionRequest(BaseModel):
    age: int
    purchase_amount: float
    review_rating: float
    previous_purchases: int

    purchases_per_year: float
    purchase_frequency_days: int

    customer_segment: int

    gender: str
    category: str
    season: str
    shipping_type: str

class InsightRequest(BaseModel):
    segment_name: str
    predicted_spending: float
    subscription_prediction: str
    subscription_probability: float

# ==========================
# HOME
# ==========================

@app.get("/")
def home():
    print("HOME ENDPOINT HIT")
    return {"message": "OK"}


# ==========================
# MODEL STATUS
# ==========================

@app.get("/model-status")
def model_status():
    return {
        "segmentation_loaded": segment_model is not None,
        "spending_loaded": spending_model is not None,
        "subscription_loaded": subscription_model is not None
    }


# ==========================
# CUSTOMER SEGMENTATION
# ==========================

@app.post("/segment-customer")
def segment_customer(data: SegmentRequest):

    input_df = pd.DataFrame([{
        "age": data.age,
        "purchase_amount": data.purchase_amount,
        "review_rating": data.review_rating,
        "previous_purchases": data.previous_purchases,
        "purchases_per_year": data.purchases_per_year
    }])

    segment_id = int(segment_model.predict(input_df)[0])

    return {
        "segment_id": segment_id,
        "segment_name": segment_names.get(segment_id, "Unknown")
    }


# ==========================
# SPENDING PREDICTION
# ==========================

@app.post("/predict-spending")
def predict_spending(data: SpendingRequest):

    input_df = pd.DataFrame([{
        "age": data.age,
        "gender": data.gender,
        "category": data.category,
        "season": data.season,
        "review_rating": data.review_rating,
        "subscription_status": data.subscription_status,
        "previous_purchases": data.previous_purchases,
        "purchase_frequency_days": data.purchase_frequency_days
    }])

    prediction = float(spending_model.predict(input_df)[0])

    return {
        "predicted_spending": round(prediction, 2)
    }


# ==========================
# SUBSCRIPTION PREDICTION
# ==========================

@app.post("/predict-subscription")
def predict_subscription(data: SubscriptionRequest):

    input_df = pd.DataFrame([{
        "age": data.age,
        "purchase_amount": data.purchase_amount,
        "review_rating": data.review_rating,
        "previous_purchases": data.previous_purchases,
        "purchases_per_year": data.purchases_per_year,
        "purchase_frequency_days": data.purchase_frequency_days,
        "customer_segment": data.customer_segment,
        "gender": data.gender,
        "category": data.category,
        "season": data.season,
        "shipping_type": data.shipping_type
    }])

    prediction = int(subscription_model.predict(input_df)[0])

    probability = float(
        subscription_model.predict_proba(input_df)[0][1]
    )

    return {
        "subscription_prediction":
            "Yes" if prediction == 1 else "No",

        "subscription_probability":
            round(probability, 4)
    }

# ==========================
# GENAI INSIGHTS
# ==========================

@app.post("/generate-insight")
def generate_insight(data: InsightRequest):

    try:

        prompt = f"""
Customer Segment: {data.segment_name}

Predicted Spending: ₹{data.predicted_spending}

Subscription Prediction: {data.subscription_prediction}

Subscription Probability: {data.subscription_probability}

Generate:

1. Customer Insight
2. Business Recommendation
3. Marketing Strategy

Keep response under 150 words.
"""

        response = gemini_model.generate_content(prompt)

        return {
            "insight": response.text
        }

    except Exception as e:

        return {
            "insight": f"Error generating insight: {str(e)}"
        }
