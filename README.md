# Customer Intelligence Dashboard Using Machine Learning, FastAPI and Generative AI

## Overview

The Customer Intelligence Dashboard is an end-to-end analytics platform that combines Machine Learning, FastAPI, Generative AI (Google Gemini), Power BI, and Web Technologies to transform customer shopping data into actionable business intelligence.

The system performs customer segmentation, spending prediction, subscription prediction, and AI-powered insight generation through an interactive dashboard. The goal is to help businesses improve customer engagement, marketing effectiveness, customer retention, and revenue growth through data-driven decision-making.

---

## Features

### Customer Segmentation

* K-Means Clustering
* Automatic customer classification
* Real-time segment prediction
* Business-friendly segment labels

### Spending Prediction

* Machine Learning regression model
* Predicts expected customer spending
* Supports revenue forecasting and customer value estimation

### Subscription Prediction

* Logistic Regression classification model
* Predicts subscription likelihood
* Provides subscription probability scores
* Supports targeted marketing campaigns

### AI-Powered Insights

* Integrated with Google Gemini API
* Generates:

  * Customer Insights
  * Business Recommendations
  * Marketing Strategies
* Converts model predictions into actionable business intelligence

### Interactive Dashboard

* Built using HTML, CSS, and JavaScript
* Real-time prediction interface
* User-friendly design

### Business Intelligence Dashboard

* Power BI integration
* Revenue analysis
* Customer behavior visualization
* Subscription analysis
* Interactive filtering

---

## Project Architecture

```text
Customer Dataset
        |
        v
Data Preprocessing
        |
        +-------------------------+
        |                         |
        v                         v
Customer Segmentation      Predictive Models
(K-Means Clustering)       (Regression + Classification)
        |                         |
        +-----------+-------------+
                    |
                    v
                FastAPI
                    |
      +-------------+-------------+
      |                           |
      v                           v
Frontend Dashboard         Gemini AI
(HTML/CSS/JavaScript)    Business Insights
      |
      v
Real-Time Customer Intelligence
```

---

## Dataset

### Dataset Size

* Records: 3900
* Features: Customer demographics, purchasing behavior, product preferences, subscription information, and shopping history.

### Key Features

* Age
* Gender
* Purchase Amount
* Review Rating
* Previous Purchases
* Category
* Season
* Subscription Status
* Shipping Type
* Purchase Frequency

### Feature Engineering

* Purchase Frequency Days
* Purchases Per Year

---

## Machine Learning Models

### Customer Segmentation

Algorithm:

* K-Means Clustering

Generated Segments:

* Premium Loyal Customers
* Low-Spend Senior Customers
* Young Satisfied Shoppers
* Loyal Repeat Customers
* High-Spend Occasional Buyers
* Frequent Active Buyers

---

### Spending Prediction

Algorithm:

* Linear Regression

Performance:

* RMSE: 23.73
* MAE: 20.70
* R² Score: -0.0067

---

### Subscription Prediction

Algorithm:

* Logistic Regression

Data Balancing:

* SMOTE (Synthetic Minority Oversampling Technique)

Performance:

* Accuracy: 59.49%
* Precision: 40.04%
* Recall: 100%
* F1 Score: 57.18%
* ROC-AUC: 72.68%

---

## API Endpoints

### Home

```http
GET /
```

### Model Status

```http
GET /model-status
```

### Customer Segmentation

```http
POST /segment-customer
```

### Spending Prediction

```http
POST /predict-spending
```

### Subscription Prediction

```http
POST /predict-subscription
```

### AI Insight Generation

```http
POST /generate-insight
```

---

## Technology Stack

### Backend

* Python
* FastAPI
* Uvicorn

### Machine Learning

* Scikit-Learn
* Pandas
* NumPy
* Imbalanced-Learn (SMOTE)
* Joblib

### Frontend

* HTML
* CSS
* JavaScript

### Generative AI

* Google Gemini API

### Business Intelligence

* Power BI

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd Customer-Intelligence-Dashboard
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

### Run FastAPI Backend

```bash
cd api
uvicorn main:app --reload
```

### Run Frontend

```bash
cd frontend
python -m http.server 5500
```

Open:

```text
http://127.0.0.1:5500
```

---

## Dashboard Workflow

1. Enter customer details.
2. Generate customer segment.
3. Predict customer spending.
4. Predict subscription likelihood.
5. Generate AI-powered business insights.
6. Analyze customer behavior using Power BI.

---

## Business Benefits

* Customer Segmentation
* Revenue Forecasting
* Subscription Growth
* Personalized Marketing
* Customer Retention
* AI-Powered Decision Support

---

## Future Scope

* Customer Churn Prediction
* Product Recommendation Systems
* Cloud Deployment
* Real-Time Analytics
* Deep Learning Models
* Retrieval-Augmented Generation (RAG)

---

## Author

Ripunjay Gogoi

Personal Project – Customer Intelligence Dashboard

---

## License

This project is intended for educational, portfolio, and research purposes.
