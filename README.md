# 🪪 Smart Aadhaar Analytics Platform

**AI-Driven Enrolment Prediction, Anomaly Detection & Decision Support**

🔗 **Live App:**
(https://smart-aadhaar-analytics-platform-ms7xn6ryqfapoxe9vnaz9d.streamlit.app/)

---

## 📌 Problem Statement

Aadhaar enrolment and update systems generate massive volumes of data, but:

* Insights are not immediately visible
* Anomalies (spikes/drops) are detected late
* Regional (mandal-level) performance is unclear
* Decision-making is mostly reactive

➡️ There is a need for an **AI-driven analytics platform** that transforms raw Aadhaar data into **actionable governance insights**.

---

## 🎯 Solution Overview

The **Smart Aadhaar Analytics Platform** is a **single-window decision dashboard** that:

* Predicts future Aadhaar enrolments
* Detects abnormal enrolment patterns automatically
* Explains anomalies with severity & risk scoring
* Recommends policy actions
* Visualizes mandal-level trends and spatial intensity
* Supports officials using an AI assistant

⚠️ **No personal or biometric data is used.**
All data is anonymized and aggregated.

---

## 🚀 Key Features

### 🔹 Mandal-Level Enrolment Prediction

* Predicts future enrolments using ML
* Inputs:

  * Month, Year
  * Age groups (0–5, 5–17, 18+)
* Output:

  * Predicted total enrolments
* Helps in **proactive resource planning**

---

### 🔹 Automated Anomaly Detection

* Uses **Isolation Forest (unsupervised ML)**
* Detects:

  * Sudden spikes
  * Sudden drops
* Works without labeled anomaly data

---

### 🔹 Anomaly Severity & Risk Scoring

For each detected anomaly:

* Direction: **Spike / Drop**
* Severity: **Low / Medium / High**
* Risk Score: **0–100**
* Date-wise anomalous records

---

### 🔹 Explainable AI (Root Cause Analysis)

Automatically explains anomalies:

* Migration inflow
* Special enrolment drives
* Technical failures
* Temporary centre shutdowns
* Seasonal demand changes

---

### 🔹 Policy & Action Recommendations

Based on severity and risk:

* Deploy temporary enrolment centres
* Increase staff
* Conduct awareness campaigns
* Perform audits
* Continue monitoring (low risk)

---

### 🔹 Pincode-Based Spatial Visualization

* Pincode-wise enrolment intensity map
* Bubble size = enrolment volume
* Color = anomaly vs normal
* No GPS or personal tracking

---

### 🔹 Time-Based Trend Analysis

* Historical enrolment trends by mandal
* Supports long-term monitoring

---

### 🔹 AI-Powered Aadhaar Assistant

* Natural language Q&A
* Answers questions like:

  * “Why is this mandal risky?”
  * “What action should be taken?”
* Works in:

  * **Online mode** (Groq API)
  * **Offline mode** (dashboard insights)

---

## 🧠 Machine Learning Models Used

| Model                   | Purpose              |
| ----------------------- | -------------------- |
| Random Forest / XGBoost | Enrolment Prediction |
| Isolation Forest        | Anomaly Detection    |

---

## 📊 Dataset

* Source: **data.gov.in – Aadhaar enrolment statistics**
* Fields include:

  * Date
  * State / District
  * Pincode (mandal proxy)
  * Age-wise enrolment counts

📌 No Aadhaar numbers, names, or biometric data are used.

---

## 🛠️ Tech Stack

* **Frontend / Dashboard:** Streamlit
* **Backend / ML:** Python, scikit-learn
* **Visualization:** Plotly
* **AI Assistant:** Groq API
* **Deployment:** Streamlit Cloud
* **Version Control:** GitHub

---

## ⚙️ Installation & Local Setup

```bash
git clone https://github.com/your-username/smart-aadhaar-analytics-platform.git
cd smart-aadhaar-analytics-platform
pip install -r requirements.txt
streamlit run app.py
```

---

## 🔐 API Key Configuration (AI Assistant)

### Streamlit Cloud (Recommended)

1. Go to **Manage App → Settings → Secrets**
2. Add:

```toml
GROQ_API_KEY = "your_api_key_here"
```

3. Save & reboot app

### Offline Mode

If API key is not provided, the app **automatically runs in offline mode**
(core analytics remain fully functional).

---

## 🧑‍💻 Developed By

* **Tejaswini**
* **Deepthi**
* **Aashritha**
* **Shruthi**
* **Moses**

---

## 🏆 Hackathon Highlights

* AI-driven (not just visualization)
* Explainable & actionable insights
* Real-world governance use case
* Scalable to national level
* Secure & privacy-preserving design

---

## 📌 Future Enhancements

* Integration with real-time UIDAI feeds
* District/state comparison dashboards
* NLP-based policy report generation
* Role-based access for officials

---


Just tell me 👍
