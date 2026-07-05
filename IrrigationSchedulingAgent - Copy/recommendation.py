import os
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "irrigation_model.pkl")

def get_crop_water_requirements():
    """Returns a dictionary of supported crops and their relative water requirements."""
    return {
        "Lettuce": {"daily_need_mm": 3.5, "root_depth_cm": 25},
        "Almonds": {"daily_need_mm": 6.5, "root_depth_cm": 90},
        "Apples": {"daily_need_mm": 5.0, "root_depth_cm": 75},
        "Rice": {"daily_need_mm": 8.0, "root_depth_cm": 35},
        "Corn": {"daily_need_mm": 5.5, "root_depth_cm": 60},
        "Wheat": {"daily_need_mm": 4.5, "root_depth_cm": 50},
        "Tomatoes": {"daily_need_mm": 4.8, "root_depth_cm": 45}
    }

def get_soil_water_retention():
    """Returns drainage and retention characteristics of soil types."""
    return {
        "Sandy": {"retention": 0.4, "drainage_speed": "High"},
        "Sandy Clay": {"retention": 0.7, "drainage_speed": "Medium-High"},
        "Loamy": {"retention": 0.8, "drainage_speed": "Medium"},
        "Silt Loam": {"retention": 0.9, "drainage_speed": "Medium-Low"},
        "Clay": {"retention": 1.2, "drainage_speed": "Low"},
        "Clayey": {"retention": 1.2, "drainage_speed": "Low"}
    }

def train_and_save_ml_model():
    """
    Generates synthetic historical records, trains a Random Forest Classifier,
    and serializes the model to disk.
    """
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Generate 500 synthetic dataset rows
    np.random.seed(42)
    n_samples = 500
    
    soil_moisture = np.random.uniform(10.0, 60.0, n_samples)
    temp = np.random.uniform(15.0, 42.0, n_samples)
    humidity = np.random.uniform(20.0, 95.0, n_samples)
    rain_prob = np.random.uniform(0.0, 100.0, n_samples)
    wind_speed = np.random.uniform(2.0, 30.0, n_samples)
    
    # Label generation: Irrigation is required if moisture is low (<32%) AND there is little rain expected (<45%)
    # Add a bit of noise to make it a realistic machine learning problem
    y = []
    for i in range(n_samples):
        # Base criteria
        score = 0
        if soil_moisture[i] < 30.0:
            score += 3
        elif soil_moisture[i] < 45.0:
            score += 1
            
        if rain_prob[i] < 40.0:
            score += 2
            
        if temp[i] > 30.0:
            score += 1
            
        # Add a random noise factor (-1 to +1)
        noise = np.random.randint(-1, 2)
        final_score = score + noise
        
        # Threshold: if score >= 4, irrigation is required
        if final_score >= 4:
            y.append(1)
        else:
            y.append(0)
            
    X = pd.DataFrame({
        "soil_moisture": soil_moisture,
        "temp": temp,
        "humidity": humidity,
        "rain_prob": rain_prob,
        "wind_speed": wind_speed
    })
    
    # Train the Random Forest
    clf = RandomForestClassifier(n_estimators=50, random_state=42)
    clf.fit(X, y)
    
    # Save to file
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(clf, f)
        
    return clf

def get_ml_model():
    """Retrieves the trained machine learning model, training it if necessary."""
    if not os.path.exists(MODEL_PATH):
        return train_and_save_ml_model()
    try:
        with open(MODEL_PATH, "rb") as f:
            return pickle.load(f)
    except Exception:
        return train_and_save_ml_model()

def predict_irrigation_requirement(soil_moisture, temp, humidity, rain_prob, wind_speed):
    """
    Uses the trained Scikit-learn model to predict if irrigation is required.
    Returns: YES/NO and the confidence score.
    """
    model = get_ml_model()
    features = pd.DataFrame([{
        "soil_moisture": soil_moisture,
        "temp": temp,
        "humidity": humidity,
        "rain_prob": rain_prob,
        "wind_speed": wind_speed
    }])
    
    prediction = model.predict(features)[0]
    probabilities = model.predict_proba(features)[0]
    
    status = "YES" if prediction == 1 else "NO"
    confidence = probabilities[prediction] * 100
    
    return status, round(confidence, 1)

if __name__ == "__main__":
    print("Training ML model...")
    train_and_save_ml_model()
    print("Testing ML prediction for dry soil:")
    print(predict_irrigation_requirement(15.0, 35.0, 30.0, 10.0, 5.0))
    print("Testing ML prediction for wet soil:")
    print(predict_irrigation_requirement(50.0, 20.0, 70.0, 80.0, 15.0))
