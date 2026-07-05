# irrigation_agent.py
"""Core Irrigation Recommendation Engine

Provides `get_irrigation_recommendation` which combines weather data,
soil moisture, crop and farmer info to produce a human‑readable recommendation.
Thresholds are loaded from `config.yaml` for easy tuning.
"""

import yaml
from datetime import datetime, timedelta
from typing import Dict, Any

from weather import fetch_weather_data

# Load configuration (defaults if missing)
try:
    with open("config.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
except FileNotFoundError:
    cfg = {}

SOIL_MOISTURE_THRESHOLD = cfg.get("soil_moisture_threshold", 30.0)
RAIN_PROB_THRESHOLD = cfg.get("rain_probability_threshold", 30.0)
MAX_IRRIGATION_DURATION = cfg.get("max_irrigation_duration_minutes", 60)
WATER_PER_MIN_PER_SQM = cfg.get("water_per_min_per_sqm", 0.12)


def calculate_water_volume(area_m2: float, duration_min: int) -> float:
    """Calculate water volume (liters) based on area and duration.

    Args:
        area_m2: Farm area in square metres.
        duration_min: Irrigation duration in minutes.
    """
    return round(area_m2 * WATER_PER_MIN_PER_SQM * duration_min, 2)


def get_irrigation_recommendation(
    farmer_name: str,
    location: str,
    crop_type: str,
    soil_type: str,
    farm_size: float,
    farm_unit: str = "Acres",
    soil_moisture: float = 0.0,
    temp: float = 0.0,
    humidity: float = 0.0,
    rain_prob: float = 0.0,
    wind_speed: float = 0.0,
    api_key: str = "",
) -> Dict[str, Any]:
    """Generate an irrigation recommendation.

    Returns a dict compatible with the FastAPI endpoint expectations.
    """
    # Pull latest weather if any metric is missing (value 0.0)
    if any(v == 0.0 for v in (temp, humidity, rain_prob, wind_speed)):
        weather = fetch_weather_data(location, api_key=api_key)
        temp = weather["temp"]
        humidity = weather["humidity"]
        rain_prob = weather["rain_probability"]
        wind_speed = weather["wind_speed"]

    # Convert farm size to square metres
    multiplier = 4046.86 if farm_unit.lower() == "acres" else 10000.0  # hectares -> m²
    area_m2 = farm_size * multiplier

    # Decision logic based on configurable thresholds
    irrigate = soil_moisture < SOIL_MOISTURE_THRESHOLD and rain_prob < RAIN_PROB_THRESHOLD

    if irrigate:
        deficit = SOIL_MOISTURE_THRESHOLD - soil_moisture
        duration = min(int((deficit / SOIL_MOISTURE_THRESHOLD) * MAX_IRRIGATION_DURATION), MAX_IRRIGATION_DURATION)
        water_liters = calculate_water_volume(area_m2, duration)
        recommended_time = (datetime.now() + timedelta(hours=1)).strftime("%I:%M %p")
        status = "YES"
        reason = f"Soil moisture ({soil_moisture:.1f}%) is below threshold and rain chance ({rain_prob:.1f}%) is low."
    else:
        duration = 0
        water_liters = 0.0
        recommended_time = "N/A"
        status = "NO"
        reason = f"Soil moisture ({soil_moisture:.1f}%) is adequate or rain chance ({rain_prob:.1f}%) is high."

    return {
        "farmer_name": farmer_name,
        "location": location,
        "crop_type": crop_type,
        "soil_type": soil_type,
        "soil_moisture": soil_moisture,
        "temperature": temp,
        "humidity": humidity,
        "rain_probability": rain_prob,
        "wind_speed": wind_speed,
        "irrigation_required": status,
        "duration_minutes": duration,
        "water_liters": water_liters,
        "recommended_time": recommended_time,
        "reason": reason,
    }

# Demo execution
if __name__ == "__main__":
    demo = get_irrigation_recommendation(
        farmer_name="Demo Farmer",
        location="Phoenix, AZ",
        crop_type="Corn",
        soil_type="Loam",
        farm_size=10,
        farm_unit="Acres",
        soil_moisture=20.0,
    )
    print(demo)
