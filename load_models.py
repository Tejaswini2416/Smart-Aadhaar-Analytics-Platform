import pandas as pd
import joblib

# ================================
# Load Saved Models
# ================================

xgb_model = joblib.load("models/xgboost_model.pkl")
iso_model = joblib.load("models/isolation_forest.pkl")
kmeans = joblib.load("models/kmeans.pkl")
scaler = joblib.load("models/kmeans_scaler.pkl")

print("All models loaded successfully ✅")

# ================================
# Sample Input Data
# ================================

sample_input = pd.DataFrame({
    "Month": [9],
    "Year": [2025],
    "age_0_5": [320],
    "age_5_17": [180],
    "age_18_greater": [25]
})

# ================================
# 1️⃣ XGBoost – Enrolment Prediction
# ================================

prediction = xgb_model.predict(sample_input)
predicted_enrolments = int(prediction[0])

print("\n📈 XGBoost Prediction")
print("Predicted Total Enrolments:", predicted_enrolments)

# ================================
# 2️⃣ Isolation Forest – Anomaly Detection
# ================================

anomaly = iso_model.predict([[predicted_enrolments]])

print("\n🚨 Anomaly Detection")
if anomaly[0] == -1:
    print("⚠️ Anomaly detected (unusual spike/drop)")
else:
    print("✅ Normal enrolment pattern")

# ================================
# 3️⃣ K-Means – Regional Clustering
# ================================

cluster_input = sample_input[['age_0_5', 'age_5_17', 'age_18_greater']]
cluster_scaled = scaler.transform(cluster_input)
cluster = kmeans.predict(cluster_scaled)

print("\n🧩 Regional Clustering")
print("Region belongs to Cluster:", cluster[0])

# Optional interpretation
if cluster[0] == 0:
    print("Cluster Type: High Enrolment Region")
elif cluster[0] == 1:
    print("Cluster Type: Medium Enrolment Region")
else:
    print("Cluster Type: Low Enrolment Region")
