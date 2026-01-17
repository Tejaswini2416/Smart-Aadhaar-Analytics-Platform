import pandas as pd
import numpy as np
import joblib, os

from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load data
df = pd.read_csv("data/aadhaar_data.csv")

df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
df['Month'] = df['date'].dt.month
df['Year'] = df['date'].dt.year

df['Total_Enrolments'] = df[['age_0_5','age_5_17','age_18_greater']].sum(axis=1)

# XGBoost
X = df[['Month','Year','age_0_5','age_5_17','age_18_greater']]
y = df['Total_Enrolments']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

xgb_model = XGBRegressor(random_state=42)
xgb_model.fit(X_train, y_train)

# Isolation Forest
iso_model = IsolationForest(contamination=0.05, random_state=42)
iso_model.fit(df[['Total_Enrolments']])

# KMeans
scaler = StandardScaler()
scaled = scaler.fit_transform(df[['age_0_5','age_5_17','age_18_greater']])

kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(scaled)

# Save models
os.makedirs("models", exist_ok=True)

joblib.dump(xgb_model, "models/xgboost_model.pkl")
joblib.dump(iso_model, "models/isolation_forest.pkl")
joblib.dump(kmeans, "models/kmeans.pkl")
joblib.dump(scaler, "models/kmeans_scaler.pkl")

print("Models trained and saved successfully")
