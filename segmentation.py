import pandas as pd
import numpy as np
import matplotlib

# Prevent matplotlib popup issues
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import os

BASE_DIR = os.getcwd()

MODEL_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODEL_DIR, exist_ok=True)

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "kmeans.pkl"
)

# =========================
# LOAD DATA
# =========================

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(
    BASE_DIR,
    "..",
    "data",
    "processed",
    "customer_cleaned.csv"
)

print("Loading:", DATA_PATH)

df = pd.read_csv(DATA_PATH)

print("Dataset Shape:", df.shape)
# =========================
# CREATE PURCHASES PER YEAR
# =========================

df["purchases_per_year"] = 365 / df["purchase_frequency_days"]

print("\nNew Feature Created:")
print(
    df[
        [
            "purchase_frequency_days",
            "purchases_per_year"
        ]
    ].head()
)

# =========================
# SELECT FEATURES
# =========================

features = [
    "age",
    "purchase_amount",
    "review_rating",
    "previous_purchases",
    "purchases_per_year"
]

X = df[features]

print("\nFeatures Selected:")
print(X.head())

print("\nFeature Shape:")
print(X.shape)

# =========================
# FEATURE SCALING
# =========================

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

print("\nScaled Feature Shape:")
print(X_scaled.shape)

print("\nFirst 5 Scaled Rows:")
print(X_scaled[:5])

# =========================
# ELBOW METHOD
# =========================

inertia = []

K = range(2, 11)

for k in K:

    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    kmeans.fit(X_scaled)

    inertia.append(kmeans.inertia_)

plt.figure(figsize=(8, 5))

plt.plot(
    K,
    inertia,
    marker="o"
)

plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia")
plt.title("Elbow Method")
plt.grid(True)

plt.savefig(
    "elbow_method.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nElbow Method graph saved as:")
print("elbow_method.png")

# =========================
# SILHOUETTE SCORES
# =========================

print("\n=========================")
print("SILHOUETTE SCORES")
print("=========================\n")

sample_size = 1000

print(f"Using sample_size={sample_size} for silhouette scoring\n")

for k in range(2, 11):

    kmeans = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    labels = kmeans.fit_predict(X_scaled)

    score = silhouette_score(
        X_scaled,
        labels,
        sample_size=sample_size,
        random_state=42
    )

    print(f"K = {k} ---> {score:.4f}")

# =========================
# FINAL KMEANS MODEL
# =========================

FINAL_K = 6

kmeans = KMeans(
    n_clusters=FINAL_K,
    random_state=42,
    n_init=10
)

df["customer_segment"] = kmeans.fit_predict(X_scaled)

segment_names = {
    0: "Premium Loyal Customers",
    1: "Low-Spend Senior Customers",
    2: "Young Satisfied Shoppers",
    3: "High-Spend Occasional Buyers",
    4: "Loyal Repeat Customers",
    5: "Frequent Active Buyers"
}

df["segment_name"] = df["customer_segment"].map(segment_names)

print("\n=========================")
print("SEGMENT NAME COUNTS")
print("=========================\n")

print(df["segment_name"].value_counts())

print("\n=========================")
print("CUSTOMER SEGMENT COUNTS")
print("=========================\n")

print(df["customer_segment"].value_counts())

# =========================
# SAVE MODEL
# =========================

joblib.dump(
    kmeans,
    MODEL_PATH
)

print("\nModel saved:")
print(MODEL_PATH)

# =========================
# SAVE DATASET
# =========================

OUTPUT_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "customer_segmented.csv"
)

import os

os.makedirs(
    os.path.join(BASE_DIR, "data", "processed"),
    exist_ok=True
)

df.to_csv(
    OUTPUT_PATH,
    index=False
)

print(OUTPUT_PATH)

print("\nSegmented dataset saved:")
print("../data/processed/customer_segmented.csv")

# =========================
# SEGMENT PROFILES
# =========================

segment_summary = (
    df.groupby("customer_segment")[
        [
            "age",
            "purchase_amount",
            "review_rating",
            "previous_purchases",
            "purchases_per_year"
        ]
    ]
    .mean()
    .round(2)
)

print("\n=========================")
print("SEGMENT PROFILES")
print("=========================\n")

print(segment_summary.to_string())