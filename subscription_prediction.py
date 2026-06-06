import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from imblearn.over_sampling import SMOTE

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix
)

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("../data/processed/customer_segmented.csv")

print("Dataset Shape:", df.shape)

# =========================
# TARGET VARIABLE
# =========================

df["subscription_target"] = (
    df["subscription_status"]
    .map({"Yes": 1, "No": 0})
)

# =========================
# CHECK CLASS DISTRIBUTION
# =========================

print("\n=========================")
print("SUBSCRIPTION DISTRIBUTION")
print("=========================\n")

print(df["subscription_status"].value_counts())

print("\nPercentage:")

print(
    round(
        df["subscription_status"]
        .value_counts(normalize=True) * 100,
        2
    )
)

# =========================
# FEATURES
# =========================

X = df[
    [
        "age",
        "gender",
        "category",
        "season",
        "purchase_amount",
        "review_rating",
        "previous_purchases",
        "purchase_frequency_days",
        "customer_segment"
    ]
]

y = df["subscription_target"]

print("\nFeature Shape:", X.shape)
print("Target Shape:", y.shape)

# =========================
# TRAIN TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining Samples:", len(X_train))
print("Testing Samples:", len(X_test))

# =========================
# PREPROCESSOR
# =========================

categorical_features = [
    "gender",
    "category",
    "season"
]

numerical_features = [
    "age",
    "purchase_amount",
    "review_rating",
    "previous_purchases",
    "purchase_frequency_days",
    "customer_segment"
]

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
# LOGISTIC REGRESSION
# =========================

logistic_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "model",
            LogisticRegression(
                max_iter=2000,
                class_weight="balanced"
            )
        )
    ]
)

logistic_model.fit(X_train, y_train)

logistic_pred = logistic_model.predict(X_test)
logistic_prob = logistic_model.predict_proba(X_test)[:, 1]

print("\n=========================")
print("LOGISTIC REGRESSION")
print("=========================")

print(f"Accuracy : {accuracy_score(y_test, logistic_pred):.4f}")
print(f"Precision: {precision_score(y_test, logistic_pred, zero_division=0):.4f}")
print(f"Recall   : {recall_score(y_test, logistic_pred, zero_division=0):.4f}")
print(f"F1 Score : {f1_score(y_test, logistic_pred, zero_division=0):.4f}")
print(f"ROC-AUC  : {roc_auc_score(y_test, logistic_prob):.4f}")

# =========================
# RANDOM FOREST
# =========================

rf_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "model",
            RandomForestClassifier(
                n_estimators=200,
                random_state=42,
                n_jobs=-1,
                class_weight="balanced"
            )
        )
    ]
)

rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)
rf_prob = rf_model.predict_proba(X_test)[:, 1]

print("\n=========================")
print("RANDOM FOREST")
print("=========================")

print(f"Accuracy : {accuracy_score(y_test, rf_pred):.4f}")
print(f"Precision: {precision_score(y_test, rf_pred, zero_division=0):.4f}")
print(f"Recall   : {recall_score(y_test, rf_pred, zero_division=0):.4f}")
print(f"F1 Score : {f1_score(y_test, rf_pred, zero_division=0):.4f}")
print(f"ROC-AUC  : {roc_auc_score(y_test, rf_prob):.4f}")

# =========================
# BEST MODEL
# =========================

logistic_auc = roc_auc_score(
    y_test,
    logistic_prob
)

rf_auc = roc_auc_score(
    y_test,
    rf_prob
)

if rf_auc > logistic_auc:
    best_model = rf_model
    best_name = "Random Forest Classifier"
    best_pred = rf_pred
else:
    best_model = logistic_model
    best_name = "Logistic Regression"
    best_pred = logistic_pred

print("\n=========================")
print("BEST MODEL")
print("=========================\n")

print(best_name)

# =========================
# SAVE MODEL
# =========================

joblib.dump(
    best_model,
    "../models/subscription_model.pkl"
)

print("\nModel Saved:")
print("../models/subscription_model.pkl")

# =========================
# CONFUSION MATRIX
# =========================

print("\n=========================")
print("CONFUSION MATRIX")
print("=========================\n")

cm = confusion_matrix(y_test, best_pred)

print(cm)