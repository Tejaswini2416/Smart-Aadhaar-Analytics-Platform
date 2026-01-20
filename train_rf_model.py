import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor

# Load data
df = pd.read_csv("data/aadhaar_data.csv")
df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")

df["Total_Enrolments"] = (
    df["age_0_5"] + df["age_5_17"] + df["age_18_greater"]
)

df["Month"] = df["date"].dt.month
df["Year"] = df["date"].dt.year

X = df[["Month", "Year", "age_0_5", "age_5_17", "age_18_greater"]]
y = df["Total_Enrolments"]

# Train model
rf_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)
rf_model.fit(X, y)

# Save model
joblib.dump(rf_model, "models/rf_model.pkl")

print("✅ Random Forest model saved successfully")
