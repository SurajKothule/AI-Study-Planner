import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Number of samples
num_rows = 10000

# For reproducibility
np.random.seed(42)

# Generate raw data
data = {
    "user_id": [f"user_{i}" for i in range(1, num_rows + 1)],
    "free_time_minutes": np.random.randint(30, 240, size=num_rows),
    "days_completed": np.random.randint(0, 30, size=num_rows),
    "engagement_score": np.round(np.random.uniform(0.2, 1.0, size=num_rows), 2),
}

# Generate planned_minutes target with noise
data["planned_minutes"] = (
    data["free_time_minutes"] * 0.6
    + data["days_completed"] * 2
    + data["engagement_score"] * 20
    + np.random.normal(0, 10, size=num_rows)
).round().astype(int)

# Create DataFrame
df_raw = pd.DataFrame(data)

# Save raw data
df_raw.to_csv("raw_data.csv", index=False)
print("✅ raw_data.csv created successfully!")

# Processed data (scaled)
X = df_raw[["free_time_minutes", "days_completed", "engagement_score"]]
y = df_raw["planned_minutes"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

df_processed = pd.DataFrame(
    X_scaled,
    columns=["free_time_scaled", "days_completed_scaled", "engagement_score_scaled"]
)
df_processed["planned_minutes"] = y

# Save processed data
df_processed.to_csv("processed_data.csv", index=False)
print("✅ processed_data.csv created successfully!")
