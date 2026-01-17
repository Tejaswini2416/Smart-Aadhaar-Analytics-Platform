import streamlit as st
import pandas as pd
import joblib

# ==================================
# Load Models
# ==================================
xgb_model = joblib.load("models/xgboost_model.pkl")
iso_model = joblib.load("models/isolation_forest.pkl")
kmeans = joblib.load("models/kmeans.pkl")
scaler = joblib.load("models/kmeans_scaler.pkl")

# ==================================
# App Title
# ==================================
st.set_page_config(page_title="Smart Aadhaar Analytics", layout="centered")
st.title("🪪 Smart Aadhaar Analytics Platform")

st.write(
    "Predict Aadhaar enrolments, detect anomalies, and classify regional performance "
    "using AI-driven analytics."
)

# ==================================
# User Input Section
# ==================================
st.header("📥 Input Enrolment Details")

month = st.number_input("Month", min_value=1, max_value=12, value=9)
year = st.number_input("Year", min_value=2020, max_value=2035, value=2025)

age_0_5 = st.number_input("Age Group 0–5", min_value=0, value=320)
age_5_17 = st.number_input("Age Group 5–17", min_value=0, value=180)
age_18 = st.number_input("Age Group 18+", min_value=0, value=25)

# ==================================
# Prediction Button
# ==================================
if st.button("🔍 Analyze"):
    # Prepare input
    input_df = pd.DataFrame({
        "Month": [month],
        "Year": [year],
        "age_0_5": [age_0_5],
        "age_5_17": [age_5_17],
        "age_18_greater": [age_18]
    })

    # ------------------------------
    # 1️⃣ XGBoost Prediction
    # ------------------------------
    prediction = xgb_model.predict(input_df)
    total_pred = int(prediction[0])

    st.subheader("📈 Enrolment Prediction")
    st.success(f"Predicted Total Enrolments: **{total_pred}**")

    # ------------------------------
    # 2️⃣ Anomaly Detection
    # ------------------------------
    anomaly = iso_model.predict([[total_pred]])

    st.subheader("🚨 Anomaly Detection")
    if anomaly[0] == -1:
        st.error("⚠️ Anomaly detected (unusual spike or drop)")
    else:
        st.success("✅ Normal enrolment pattern")

    # ------------------------------
    # 3️⃣ K-Means Clustering
    # ------------------------------
    cluster_input = input_df[['age_0_5', 'age_5_17', 'age_18_greater']]
    cluster_scaled = scaler.transform(cluster_input)
    cluster = kmeans.predict(cluster_scaled)[0]

    st.subheader("🧩 Regional Performance Cluster")

    if cluster == 0:
        st.info("High Enrolment Region")
    elif cluster == 1:
        st.warning("Medium Enrolment Region")
    else:
        st.error("Low Enrolment Region")

# ==================================
# Footer
# ==================================
st.markdown("---")
st.caption("Built using XGBoost, Isolation Forest, K-Means & Streamlit")
