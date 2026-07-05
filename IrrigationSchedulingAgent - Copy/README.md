# Irrigation Scheduling Agent 🌾💧

An AI-powered and Machine Learning-assisted Irrigation Scheduling Agent that helps farmers determine optimal crop watering times, durations, and water volumes based on weather forecasts, soil moisture sensors, crop types, and temperatures.

## Features
- **Interactive Dashboard**: Modern agriculture-themed UI displaying weather conditions, soil moisture metrics, water tank capacity, alerts, and historical trend plots.
- **Farmer Profile Manager**: Form to register and manage multiple farm profiles with fields for crop types, soil conditions, and farm size.
- **Live/Mock Weather Module**: Fetches live metrics from OpenWeather API with intelligent location-based mock simulation when API keys are not supplied.
- **AI Decision Agent**: Leverages the Gemini API to formulate professional agronomist watering schedules and reasoning, with seamless local rule-based fallback.
- **ML Predictor**: Embeds a Scikit-learn Random Forest Classifier to estimate irrigation needs based on sensor data.
- **Automated Reports**: Compiles daily, weekly, and monthly statistics into beautiful PDF sheets using ReportLab.
- **Admin Utilities**: Allows deleting records, examining raw tables, and exporting any database table to Excel sheet files.

## Project Structure
```text
IrrigationSchedulingAgent/
│
├── app.py                 # Streamlit application UI & navigation
├── database.py            # SQLite database schema initialization & helpers
├── weather.py             # OpenWeather API integration and mock logic
├── irrigation_agent.py    # Gemini API recommendation agent & fallback rules
├── recommendation.py      # Water volume formulas & Scikit-learn Random Forest model
├── report.py              # PDF generator utilizing ReportLab compiler
├── requirements.txt       # Python package dependencies
├── README.md              # Project usage and instructions
├── data/
│   └── reports/           # Generated PDF report folder
└── database/
    └── irrigation.db      # SQLite local database binary
```

## Installation & Setup

1. **Clone or copy** the project files to a local directory:
   ```bash
   cd IrrigationSchedulingAgent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys (Optional)**:
   - Set environment variables for live API integration:
     - **Gemini API**: `GEMINI_API_KEY` (highly recommended for AI recommendations)
     - **OpenWeather API**: `OPENWEATHER_API_KEY` (for live local forecast lookups)
   
   *Note: If these keys are not set, the application will automatically fall back to rule-based decisions and simulated weather forecasts, allowing immediate, fully functional testing.*

4. **Launch the Streamlit dashboard**:
   ```bash
   streamlit run app.py
   ```

5. Access the app in your browser at `http://localhost:8501`.
