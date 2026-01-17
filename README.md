# 🪪 Smart Aadhaar Analytics Platform

An AI-driven analytics platform that provides **mandal-level Aadhaar enrolment prediction**, **anomaly detection**, and **regional insights** to support **data-driven governance**.

🔗 **Live Application:**
👉 [https://smart-aadhaar-analytics-platform-aacgm8dawahpniimw3hspt.streamlit.app/](https://smart-aadhaar-analytics-platform-aacgm8dawahpniimw3hspt.streamlit.app/)

---

## 📌 Problem Statement

Aadhaar enrolment and update services generate large volumes of data across regions. However:

* Enrolment demand is difficult to predict
* Anomalies (spikes/drops) are detected late
* Mandal-level (local) insights are not easily visible
* Decision-making is often reactive

There is a need for a **smart analytics platform** to enable **proactive planning and early warning**.

---

## 🎯 Objectives

This project aims to:

* Predict **future Aadhaar enrolment demand**
* Detect **abnormal spikes or drops** automatically
* Provide **mandal-level (pincode-based) insights**
* Explain anomalies in an interpretable manner
* Offer a **single interactive dashboard** for decision-makers

---

## 📂 Dataset

* **Dataset Name:** Aadhaar Enrolment Statistics by State, District and Age Group
* **Source:** UIDAI Open Data (data.gov.in)
* **Nature:** Aggregated & anonymised (no personal/biometric data)

### Key Features:

* Date
* State
* District
* Pincode (used as mandal proxy)
* Enrolments by age group:

  * 0–5 years
  * 5–17 years
  * 18+ years

---

## ⚙️ System Architecture

```
Data Ingestion (UIDAI Open Data)
        ↓
Data Preprocessing & Feature Engineering
        ↓
XGBoost → Enrolment Prediction
Isolation Forest → Anomaly Detection
K-Means → Regional Clustering
        ↓
Streamlit Interactive Dashboard
```

---

## 🤖 Models Used

### 1️⃣ XGBoost – Enrolment Prediction

* Predicts total Aadhaar enrolments
* Uses age group distribution and temporal features
* Handles non-linear patterns efficiently

**Evaluation Metrics:** RMSE, MAE, R² Score

---

### 2️⃣ Isolation Forest – Anomaly Detection

* Detects unusual spikes or drops in enrolments
* Unsupervised (no labeled anomalies required)
* Works efficiently on real-world data

**Output:** Normal / Anomaly flags with explanation

---

### 3️⃣ K-Means – Regional Clustering

* Groups mandals based on enrolment behaviour
* Identifies high, medium, and low-activity regions

**Evaluation Metric:** Silhouette Score

---

## 📊 Dashboard Features

* 📈 Mandal-level enrolment prediction
* 🚨 Anomaly alerts with **human-readable explanations**
* 📊 Time-based enrolment trends
* 🧩 Regional performance classification
* 🗺️ Map visualization (mandal-level)
* 📤 Downloadable CSV reports

---

## 🧠 Anomaly Explanation Logic

When an anomaly is detected, the system explains it using historical comparison:

* **Spike:** Special enrolment drives, migration, backlog clearance
* **Drop:** Technical issues, center downtime, seasonal decline

This improves **trust and interpretability** for governance use cases.

---

## 🛠️ Tech Stack

* **Programming Language:** Python
* **Machine Learning:** XGBoost, Isolation Forest, K-Means
* **Data Processing:** Pandas, NumPy
* **Visualization & UI:** Streamlit
* **Model Persistence:** Joblib
* **Deployment:** Streamlit Community Cloud

---

## 🚀 How to Run Locally

```bash
# Activate virtual environment
venv\Scripts\activate

# Run the application
python -m streamlit run app.py
```

---

## 📁 Project Structure

```
Smart-Aadhaar-Analytics-Platform/
├── app.py
├── data/
│   └── aadhaar_data.csv
├── models/
│   ├── xgboost_model.pkl
│   ├── isolation_forest.pkl
│   ├── kmeans.pkl
│   └── kmeans_scaler.pkl
├── requirements.txt
└── README.md
```

---

## 🏆 Hackathon & Impact Value

* Enables **proactive resource planning**
* Supports **early warning systems**
* Provides **localized (mandal-level) insights**
* Scalable to district/state/national level
* Uses **ethical, anonymised public data**

---

## 🎤 One-Line Summary (Viva / Pitch)

> “The Smart Aadhaar Analytics Platform uses AI to predict mandal-level enrolment demand, detect anomalies, and provide explainable insights for data-driven governance.”

---

## 📌 Future Enhancements

* Real-time data integration
* Advanced geospatial heatmaps
* API integration for government dashboards
* Automated policy recommendation engine

---

👩‍💻 Developed by

Tejaswini

Deepthisree

Aashritha

Shruthi

Moses

(Hackathon / Academic Project)
