import streamlit as st
import pandas as pd
import joblib
import os

from pincode_map import show_pincode_map

# ================================
# Optional Groq AI Assistant
# ================================
try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

# ================================
# Page Config
# ================================
st.set_page_config(
    page_title="Smart Aadhaar Analytics Platform",
    layout="wide"
)

# ================================
# API Key Loader (ENV ONLY)
# ================================
def get_groq_api_key():
    return os.getenv("GROQ_API_KEY")

API_KEY = get_groq_api_key()

# ================================
# Header
# ================================
st.title("Smart Aadhaar Analytics Platform")
st.caption(
    "Mandal-level enrolment prediction, anomaly detection & decision support"
)

if API_KEY and GROQ_AVAILABLE:
    st.success("🟢 AI Assistant: ONLINE")
else:
    st.info("🟡 AI Assistant: OFFLINE (dashboard insights still available)")

# ================================
# Helper Functions
# ================================
def anomaly_severity(current, avg):
    ratio = abs(current - avg) / avg
    if ratio > 0.6:
        return "High", 100
    elif ratio > 0.3:
        return "Medium", 70
    else:
        return "Low", 40

# ================================
# AI Chatbot
# ================================
def groq_chatbot(question, context):
    if not API_KEY or not GROQ_AVAILABLE:
        return (
            "AI assistant is running in offline mode.\n\n"
            "You can interpret predictions, anomaly severity, "
            "risk scores and actions directly from the dashboard."
        )

    client = Groq(api_key=API_KEY)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are an Aadhaar analytics assistant."},
            {"role": "user", "content": f"{context}\n\nQuestion: {question}"}
        ],
        temperature=0.4
    )

    return response.choices[0].message.content

# ================================
# Load Dataset
# ================================
df = pd.read_csv("data/aadhaar_data.csv")
df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")

df["Total_Enrolments"] = (
    df["age_0_5"] + df["age_5_17"] + df["age_18_greater"]
)

mandal_df = df.groupby(
    ["pincode", "date"], as_index=False
)["Total_Enrolments"].sum()

mandal_df["Month"] = mandal_df["date"].dt.month
mandal_df["Year"] = mandal_df["date"].dt.year

mandal_avg = mandal_df.groupby("pincode")["Total_Enrolments"].mean().to_dict()

# ================================
# Load Models
# ================================
rf_model = joblib.load("models/rf_model.pkl")
iso_model = joblib.load("models/isolation_forest.pkl")

# ================================
# Sidebar Inputs
# ================================
st.sidebar.header("📍 Mandal Inputs")

pincode = st.sidebar.selectbox(
    "Select Mandal (Pincode)",
    sorted(mandal_df["pincode"].unique())
)

month = st.sidebar.slider("Month", 1, 12, 9)
year = st.sidebar.slider("Year", 2024, 2035, 2025)

age_0_5 = st.sidebar.number_input("Age 0–5", 0, 3000, 300)
age_5_17 = st.sidebar.number_input("Age 5–17", 0, 3000, 180)
age_18 = st.sidebar.number_input("Age 18+", 0, 3000, 25)

view_mode = st.sidebar.radio(
    "📊 View Mode",
    ["Trend View", "Pincode Map View"]
)

# ================================
# Enrolment Prediction
# ================================
st.header("📈 Enrolment Prediction")

input_df = pd.DataFrame({
    "Month": [month],
    "Year": [year],
    "age_0_5": [age_0_5],
    "age_5_17": [age_5_17],
    "age_18_greater": [age_18]
})

prediction = int(rf_model.predict(input_df)[0])

st.success(
    f"Predicted Total Enrolments for Mandal {pincode}: **{prediction}**"
)

# ================================
# Anomaly Detection & Risk Analysis
# ================================
st.header("🚨 Anomaly Detection & Risk Analysis")

mandal_data = mandal_df[mandal_df["pincode"] == pincode].copy()
mandal_data["anomaly"] = iso_model.predict(
    mandal_data[["Total_Enrolments"]]
)

anomalies = mandal_data[mandal_data["anomaly"] == -1]

if anomalies.empty:
    st.success("✅ No anomalies detected for this mandal.")
else:
    st.error("⚠️ Anomalies Detected")

    for _, row in anomalies.sort_values("date").iterrows():
        current_val = row["Total_Enrolments"]
        avg_val = mandal_avg[pincode]

        direction = "Spike" if current_val > avg_val else "Drop"
        severity, risk = anomaly_severity(current_val, avg_val)

        if direction == "Spike":
            causes = (
                "Special enrolment drives, migration inflow, "
                "backlog clearance or awareness campaigns."
            )
            actions = (
                "Deploy temporary centres, increase staff, "
                "conduct audits and close monitoring."
            )
        else:
            causes = (
                "Temporary centre shutdowns, technical failures, "
                "staff shortage or seasonal low demand."
            )
            actions = "Continue monitoring and routine optimisation."

        with st.container(border=True):
            st.markdown(
                f"""
**📅 Date:** {row['date'].date()}  
**📊 Enrolments:** {current_val}  
**📉 Direction:** {direction}  
**🔥 Severity:** {severity}  
**⚠️ Risk Score:** {risk}/100  

**💡 Likely Causes:**  
{causes}

**🛠 Recommended Actions:**  
{actions}
"""
            )

# ================================
# Visualization
# ================================
if view_mode == "Trend View":
    st.header("📊 Mandal Enrolment Trend")
    st.line_chart(
        mandal_data.set_index("date")["Total_Enrolments"]
    )
else:
    st.header("🗺️ Pincode-wise Aadhaar Enrolment Map")
    show_pincode_map(mandal_df, anomalies)

# ================================
# AI Assistant
# ================================
st.markdown("---")
st.header("🤖 Aadhaar AI Assistant")

question = st.text_input(
    "Ask about predictions, anomalies, severity, risk or actions:"
)

if question:
    context = f"""
Pincode: {pincode}
Predicted Enrolments: {prediction}
Average Enrolments: {mandal_avg[pincode]}
Anomaly Detected: {"Yes" if not anomalies.empty else "No"}
"""
    with st.spinner("Thinking..."):
        st.success(groq_chatbot(question, context))

# ================================
# Footer
# ================================
st.markdown("---")
st.caption(
    "Smart Aadhaar Analytics Platform | "
    "Prediction • Anomaly Severity • Risk Scoring • Decision Support"
)
