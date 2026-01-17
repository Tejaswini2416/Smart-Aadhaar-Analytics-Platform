import streamlit as st
import pandas as pd
import joblib

# ==================================
# Page Config
# ==================================
st.set_page_config(
    page_title="Smart Aadhaar Analytics",
    layout="wide"
)

st.title("🪪 Smart Aadhaar Analytics Platform")
st.caption("Mandal-level enrolment prediction, anomaly detection & regional insights")

# ==================================
# Load Real Dataset
# ==================================
df = pd.read_csv("data/aadhaar_data.csv")

df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')

# Total enrolments
df['Total_Enrolments'] = df[
    ['age_0_5', 'age_5_17', 'age_18_greater']
].sum(axis=1)

# Mandal-level aggregation (Pincode based)
mandal_df = df.groupby(
    ['pincode', 'date'], as_index=False
).agg({
    'age_0_5': 'sum',
    'age_5_17': 'sum',
    'age_18_greater': 'sum',
    'Total_Enrolments': 'sum'
})

mandal_df['Month'] = mandal_df['date'].dt.month
mandal_df['Year'] = mandal_df['date'].dt.year

# Mandal historical average (important feature)
mandal_avg = mandal_df.groupby(
    'pincode'
)['Total_Enrolments'].mean().to_dict()

# ==================================
# Load Models
# ==================================
xgb_model = joblib.load("models/xgboost_model.pkl")
iso_model = joblib.load("models/isolation_forest.pkl")

# ==================================
# Sidebar Inputs
# ==================================
st.sidebar.header("📍 Mandal-based Inputs")

pincode = st.sidebar.selectbox(
    "Select Mandal (Pincode)",
    sorted(mandal_df['pincode'].unique())
)

month = st.sidebar.slider("Month", 1, 12, 9)
year = st.sidebar.slider("Year", 2024, 2035, 2025)

age_0_5 = st.sidebar.number_input("Age 0–5", 0, 3000, 300)
age_5_17 = st.sidebar.number_input("Age 5–17", 0, 3000, 180)
age_18 = st.sidebar.number_input("Age 18+", 0, 3000, 25)

# ==================================
# Mandal-Level Prediction
# ==================================
st.subheader("📈 Mandal-Level Enrolment Prediction")

mandal_feature = mandal_avg.get(
    pincode, mandal_df['Total_Enrolments'].mean()
)

input_df = pd.DataFrame({
    'Month': [month],
    'Year': [year],
    'age_0_5': [age_0_5],
    'age_5_17': [age_5_17],
    'age_18_greater': [age_18],
})

predicted_enrolments = int(
    xgb_model.predict(input_df)[0]
)

st.success(
    f"Predicted Total Enrolments for Mandal {pincode}: "
    f"**{predicted_enrolments}**"
)

# ==================================
# Anomaly Detection & Explanation
# ==================================
st.subheader("🚨 Anomaly Detection & Explanation")

mandal_data = mandal_df[
    mandal_df['pincode'] == pincode
].copy()

mandal_data['Anomaly'] = iso_model.predict(
    mandal_data[['Total_Enrolments']]
)

anomalies = mandal_data[
    mandal_data['Anomaly'] == -1
]

if len(anomalies) > 0:
    st.error("⚠️ Anomaly spike(s) detected in this mandal")

    latest_anomaly = anomalies.sort_values(
        'date', ascending=False
    ).iloc[0]

    current_val = latest_anomaly['Total_Enrolments']
    avg_val = mandal_avg[pincode]

    if current_val > avg_val:
        reason = (
            "Unusual spike observed. Possible reasons include:\n"
            "- Special Aadhaar enrolment drives\n"
            "- Migration or population inflow\n"
            "- Backlog clearance at enrolment centers\n"
            "- Seasonal enrolment surge"
        )
    else:
        reason = (
            "Unusual drop observed. Possible reasons include:\n"
            "- Technical issues at enrolment centers\n"
            "- Temporary center shutdowns\n"
            "- Reduced footfall or seasonal decline"
        )

    st.markdown("### 📌 Likely Reason")
    st.info(reason)

    st.markdown("### 📋 Anomalous Records")
    st.dataframe(
        anomalies[['date', 'Total_Enrolments']]
    )

else:
    st.success("✅ No anomaly spikes detected for this mandal")

# ==================================
# Trend Visualization
# ==================================
st.subheader("📊 Mandal Enrolment Trend")

st.line_chart(
    mandal_data.set_index('date')['Total_Enrolments']
)

# ==================================
# Footer
# ==================================
st.markdown("---")
st.caption(
    "Built using XGBoost, Isolation Forest, Streamlit | "
    "Mandal-level Aadhaar Analytics"
)
