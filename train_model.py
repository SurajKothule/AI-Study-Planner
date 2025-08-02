import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import joblib

# Create a more realistic synthetic dataset
np.random.seed(42)
n_samples = 200

free_time = np.random.uniform(30, 300, size=n_samples)
days_completed = np.random.randint(1, 30, size=n_samples)
engagement_score = np.random.uniform(0.2, 1.0, size=n_samples)

# Formula to simulate output:
# Assume more free time, more days, and higher engagement = more minutes studied.
minutes_studied = (
    free_time * 0.5 +
    days_completed * 3 +
    engagement_score * 50 +
    np.random.normal(0, 10, size=n_samples)  # noise
)

# Create DataFrame
df = pd.DataFrame({
    "free_time_minutes": free_time,
    "days_completed": days_completed,
    "engagement_score": engagement_score,
    "minutes_studied": minutes_studied
})

# Features and target
X = df[["free_time_minutes", "days_completed", "engagement_score"]]
y = df["minutes_studied"]

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train model
model = LinearRegression()
model.fit(X_scaled, y)

# Save model and scaler
joblib.dump(model, "models/study_predictor.pkl")
joblib.dump(scaler, "models/scaler.pkl")

print("✅ Model trained and saved successfully.")
