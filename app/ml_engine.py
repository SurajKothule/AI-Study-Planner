import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

# === Retraining Function ===
def retrain_model():
    """
    Retrains the study time prediction model using historical user activity logs.
    """
    try:
        # Load user activity log
        df = pd.read_json("data/user_activity_log.json")

        # Make sure these columns match exactly what you store
        X = df[["free_time_minutes", "days_completed", "engagement_score"]]
        y = df["predicted_minutes"]

        # Fit scaler
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Fit model
        model = LinearRegression()
        model.fit(X_scaled, y)

        # Save model and scaler
        with open("models/study_predictor.pkl", "wb") as f:
            pickle.dump(model, f)
        with open("models/scaler.pkl", "wb") as f:
            pickle.dump(scaler, f)

        print("✅ Model retrained successfully.")

    except Exception as e:
        print(f"❌ Failed to retrain model: {e}")

# === Prediction Function ===
def predict_study_time(data):
    """
    Predict study time given input features.

    Parameters:
        data (dict): {
            "free_time_minutes": float,
            "days_completed": int,
            "engagement_score": float
        }

    Returns:
        float: Predicted study time in minutes (non-negative)
    """
    try:
        # Load model and scaler
        with open("models/study_predictor.pkl", "rb") as f:
            model = pickle.load(f)
        with open("models/scaler.pkl", "rb") as f:
            scaler = pickle.load(f)

        # Prepare input
        X = np.array([[
            data["free_time_minutes"],
            data["days_completed"],
            data["engagement_score"]
        ]])
        X_scaled = scaler.transform(X)

        # Predict
        y_pred = model.predict(X_scaled)
        prediction = max(0, y_pred[0])  # Clamp negative to zero

        return float(prediction)

    except Exception as e:
        raise RuntimeError(f"Prediction failed: {e}")
