import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import pickle

def retrain_model():
    data = pd.read_csv("data/processed_data.csv")
    X = data[["difficulty", "motivation", "available_hours"]]
    y = data["study_hours"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = LinearRegression()
    model.fit(X_scaled, y)

    with open("models/study_predictor.pkl", "wb") as f:
        pickle.dump(model, f)

    with open("models/scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    print("Model retrained successfully.")

