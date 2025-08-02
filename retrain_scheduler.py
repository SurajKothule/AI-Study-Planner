import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

def retrain_model():
    try:
        df = pd.read_json("data/user_activity_log.json")

        # Drop rows with missing data
        df = df.dropna()

        # ❌ If file is empty after dropping missing
        if df.empty:
            print("⚠️ No valid data to retrain the model.")
            return

        # Prepare features
        X = df[["free_time_minutes", "days_completed", "engagement_score"]]
        y = df["predicted_minutes"]

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        model = LinearRegression()
        model.fit(X_scaled, y)

        with open("models/study_predictor.pkl", "wb") as f:
            pickle.dump(model, f)

        with open("models/scaler.pkl", "wb") as f:
            pickle.dump(scaler, f)

        print("✅ Model retrained successfully.")

    except Exception as e:
        print(f"❌ Failed to retrain model: {e}")

if __name__ == "__main__":
    retrain_model()
