import os
import requests
import random
import re

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

def clean_location(location):
    """Clean the location string for better API searches."""
    # Remove state abbreviations, countries or details in parentheses
    clean = re.sub(r'\(.*?\)', '', location)
    clean = clean.split(',')[0].strip()
    return clean

def fetch_weather_data(location, api_key=None):
    """
    Fetches real-time weather using OpenWeather API.
    Falls back to high-fidelity simulated weather if key is missing or request fails.
    """
    key = api_key or OPENWEATHER_API_KEY
    clean_loc = clean_location(location)
    
    if not key or key.strip() == "":
        return generate_mock_weather(location, "API key not configured. Using high-fidelity local weather simulation.")
    
    try:
        # Step 1: Geocoding to get Lat/Lon
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={clean_loc}&limit=1&appid={key}"
        geo_response = requests.get(geo_url, timeout=5)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        
        if not geo_data:
            return generate_mock_weather(location, f"Could not find coordinates for '{clean_loc}'. Simulated fallback active.")
        
        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]
        display_name = f"{geo_data[0].get('name')}, {geo_data[0].get('country')}"
        
        # Step 2: Fetch 5-Day / 3-Hour Forecast to get rain probability (pop)
        # Using forecast because standard weather API doesn't include future rain probability.
        forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={key}&units=metric"
        res = requests.get(forecast_url, timeout=5)
        res.raise_for_status()
        forecast_data = res.json()
        
        # Extract immediate weather (current) and rain probability
        current_list = forecast_data.get("list", [])
        if not current_list:
            return generate_mock_weather(location, "API returned empty forecast. Simulated fallback active.")
        
        # Current or closest forecast point
        current = current_list[0]
        temp = current["main"]["temp"]
        humidity = current["main"]["humidity"]
        wind_speed = current["wind"]["speed"] * 3.6  # Convert m/s to km/h
        
        # Rain probability (pop is between 0 and 1, convert to %)
        # Look ahead at the next 24 hours (next 8 entries in 3-hour forecast)
        rain_probabilities = [item.get("pop", 0.0) * 100 for item in current_list[:8]]
        rain_probability = max(rain_probabilities) if rain_probabilities else 0.0
        
        # Description
        desc = current["weather"][0]["description"].capitalize()
        
        return {
            "location": display_name,
            "temp": round(temp, 1),
            "humidity": round(humidity, 1),
            "rain_probability": round(rain_probability, 1),
            "wind_speed": round(wind_speed, 1),
            "description": desc,
            "source": "OpenWeather API (Live)"
        }
        
    except Exception as e:
        return generate_mock_weather(location, f"Error fetching live weather: {str(e)}. Simulated fallback active.")

def generate_mock_weather(location, notice_msg=""):
    """
    Generates intelligent weather characteristics based on location string.
    """
    loc_lower = location.lower()
    
    # Initialize defaults
    temp = 24.0
    humidity = 60.0
    rain_probability = 20.0
    wind_speed = 10.0
    desc = "Partly Cloudy"
    
    # Custom attributes for climates
    if any(keyword in loc_lower for keyword in ["california", "ca", "desert", "phoenix", "arizona", "vegas", "texas", "tx", "sahara", "senegal", "sahel"]):
        temp = random.uniform(30.0, 39.0)
        humidity = random.uniform(15.0, 35.0)
        rain_probability = random.uniform(0.0, 15.0)
        wind_speed = random.uniform(8.0, 18.0)
        desc = "Sunny and Dry"
    elif any(keyword in loc_lower for keyword in ["washington", "wa", "seattle", "london", "uk", "oregon", "canada", "rainy", "vietnam", "rice"]):
        temp = random.uniform(12.0, 18.0)
        humidity = random.uniform(75.0, 95.0)
        rain_probability = random.uniform(55.0, 90.0)
        wind_speed = random.uniform(12.0, 25.0)
        desc = "Light Rain / Overcast"
    elif any(keyword in loc_lower for keyword in ["florida", "fl", "miami", "tropical", "brazil", "amazon"]):
        temp = random.uniform(28.0, 34.0)
        humidity = random.uniform(80.0, 98.0)
        rain_probability = random.uniform(40.0, 85.0)
        wind_speed = random.uniform(5.0, 15.0)
        desc = "Humid / Threat of Showers"
    else:
        # Default temperate
        temp = random.uniform(20.0, 27.0)
        humidity = random.uniform(45.0, 65.0)
        rain_probability = random.uniform(10.0, 45.0)
        wind_speed = random.uniform(6.0, 14.0)
        desc = "Scattered Clouds"
        
    return {
        "location": location,
        "temp": round(temp, 1),
        "humidity": round(humidity, 1),
        "rain_probability": round(rain_probability, 1),
        "wind_speed": round(wind_speed, 1),
        "description": desc,
        "source": "Weather Simulation (Mock)",
        "notice": notice_msg
    }

if __name__ == "__main__":
    print("Testing Mock Weather:")
    print(fetch_weather_data("Phoenix, AZ"))
    print(fetch_weather_data("Seattle, WA"))
