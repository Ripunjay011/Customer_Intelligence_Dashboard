import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_error,
    r2_score
)

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("../data/processed/customer_segmented.csv")

print("Dataset Shape:", df.shape)

# =========================
# FEATURES & TARGET
# =========================

X = df[
    [
        "age",
        "gender",
        "category",
        "season",
        "review_rating",
        "subscription_status",
        "previous_purchases",
        "purchase_frequency_days"
    ]
]

y = df["purchase_amount"]

print("\nFeature Shape:", X.shape)
print("Target Shape:", y.shape)

# =========================
# CATEGORICAL & NUMERICAL
# =========================

categorical_features = [
    "gender",
    "category",
    "season",
    "subscription_status"
]

numerical_features = [
    "age",
    "review_rating",
    "previous_purchases",
    "purchase_frequency_days"
]

# =========================
# PREPROCESSOR
# =========================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "cat",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "num",
            "passthrough",
            numerical_features
        )
    ]
)

# =========================
# TRAIN TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining Samples:", len(X_train))
print("Testing Samples:", len(X_test))

# =========================
# LINEAR REGRESSION
# =========================

linear_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", LinearRegression())
    ]
)

linear_model.fit(X_train, y_train)

linear_pred = linear_model.predict(X_test)

linear_rmse = np.sqrt(
    mean_squared_error(y_test, linear_pred)
)

linear_mae = mean_absolute_error(
    y_test,
    linear_pred
)

linear_r2 = r2_score(
    y_test,
    linear_pred
)

print("\n=========================")
print("LINEAR REGRESSION")
print("=========================")

print(f"RMSE : {linear_rmse:.2f}")
print(f"MAE  : {linear_mae:.2f}")
print(f"R²   : {linear_r2:.4f}")

# =========================
# RANDOM FOREST
# =========================

rf_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "model",
            RandomForestRegressor(
                n_estimators=200,
                random_state=42,
                n_jobs=-1
            )
        )
    ]
)

rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)

rf_rmse = np.sqrt(
    mean_squared_error(y_test, rf_pred)
)

rf_mae = mean_absolute_error(
    y_test,
    rf_pred
)

rf_r2 = r2_score(
    y_test,
    rf_pred
)

print("\n=========================")
print("RANDOM FOREST")
print("=========================")

print(f"RMSE : {rf_rmse:.2f}")
print(f"MAE  : {rf_mae:.2f}")
print(f"R²   : {rf_r2:.4f}")

# =========================
# SELECT BEST MODEL
# =========================

if rf_r2 > linear_r2:
    best_model = rf_model
    best_name = "Random Forest"
else:
    best_model = linear_model
    best_name = "Linear Regression"

print("\n=========================")
print("BEST MODEL")
print("=========================")

print(best_name)

# =========================
# SAVE MODEL
# =========================

joblib.dump(
    best_model,
    "../models/spending_model.pkl"
)

print("\nModel Saved:")
print("../models/spending_model.pkl")