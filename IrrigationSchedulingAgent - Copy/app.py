import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# Import project modules
from database import (
    init_db, get_all_farmers, add_farmer, delete_farmer,
    get_irrigation_history, log_irrigation, delete_irrigation_record,
    get_all_reports, get_db_connection
)
from weather import fetch_weather_data
from irrigation_agent import get_irrigation_recommendation
from recommendation import predict_irrigation_requirement, train_and_save_ml_model
from report import generate_pdf_report

# Initialize database and train ML model if needed
init_db()
train_and_save_ml_model()

# Set up page configurations
st.set_page_config(
    page_title="Irrigation Scheduling Agent",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Agriculture Theme Styling
st.markdown("""
    <style>
        /* General styling */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }
        
        .main {
            background-color: #f7fafc;
        }
        
        /* Metric card styling */
        .metric-card {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
            border-left: 5px solid #2E7D32;
            margin-bottom: 15px;
        }
        
        .metric-title {
            font-size: 14px;
            color: #718096;
            font-weight: 600;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        
        .metric-value {
            font-size: 28px;
            color: #1A202C;
            font-weight: 700;
        }
        
        /* Sidebar styling */
        .sidebar .sidebar-content {
            background-color: #1E4620;
        }
        
        /* Custom titles */
        .main-header {
            color: #1B5E20;
            font-weight: 700;
            margin-bottom: 20px;
        }
        
        .section-header {
            color: #2E7D32;
            font-weight: 600;
            border-bottom: 2px solid #E2E8F0;
            padding-bottom: 8px;
            margin-top: 25px;
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# Navigation
st.sidebar.markdown("<h2 style='text-align: center; color: #2E7D32;'>🌱 Irrigation Agent</h2>", unsafe_allow_html=True)
page = st.sidebar.radio(
    "Navigation Menu",
    [
        "🏠 Home",
        "📊 Dashboard",
        "👤 Farmer Registration",
        "🌤️ Weather",
        "🤖 AI Recommendation",
        "📜 History",
        "📈 Reports",
        "⚙️ Admin"
    ]
)

# ----------------- PAGE 1: HOME -----------------
if page == "🏠 Home":
    st.markdown("<h1 class='main-header'>Welcome to the Irrigation Scheduling Agent</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### AI-Powered Agriculture at Your Fingertips
        This agent is designed to help modern farmers optimize water usage by bringing together advanced AI, machine learning prediction models, and live weather forecasting.
        
        #### Core Benefits:
        * **Prevent Overwatering**: Keep your crops healthy without wasting vital water resources.
        * **AI Analysis**: Harness the Gemini LLM for expert agronomist recommendations.
        * **ML Soil Moisture Predictions**: Leverage a Scikit-learn predictive classifier to backup decisions.
        * **Historical Tracking**: Automatically archive every watering action for seasonal audits.
        
        #### Quick Start Guide:
        1. Register your farm under the **Farmer Registration** tab.
        2. Set up your OpenWeather API Key (optional) in the environment to fetch live weather details.
        3. Head to the **AI Recommendation** tab to run decisions, input current soil levels, and generate schedule suggestions.
        4. Track trends on the **Dashboard** and download compilation reports on the **Reports** tab.
        """)
        
        st.info("💡 **Aesthetic Theme Notes**: The layout utilizes structured earthy greens and chocolate browns to fit standard eco-conscious agriculture tools.")
        
    with col2:
        st.markdown("### Quick Stats")
        
        # Pull stats from DB
        farmers_df = get_all_farmers()
        history_df = get_irrigation_history()
        
        total_farmers = len(farmers_df)
        total_logs = len(history_df)
        water_saved_estimate = 0
        if not history_df.empty:
            water_saved_estimate = history_df[history_df['status'] == 'NO'].shape[0] * 350 # Liters saved per negative trigger
            
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Registered Farmers</div>
                <div class="metric-value">{total_farmers}</div>
            </div>
            <div class="metric-card" style="border-left-color: #5D4037;">
                <div class="metric-title">Irrigation Recommendations Run</div>
                <div class="metric-value">{total_logs}</div>
            </div>
            <div class="metric-card" style="border-left-color: #1976D2;">
                <div class="metric-title">Estimated Water Preserved</div>
                <div class="metric-value">{water_saved_estimate:,} Liters</div>
            </div>
        """, unsafe_allow_html=True)

# ----------------- PAGE 2: DASHBOARD -----------------
elif page == "📊 Dashboard":
    st.markdown("<h1 class='main-header'>Irrigation Operations Dashboard</h1>", unsafe_allow_html=True)
    
    farmers_df = get_all_farmers()
    
    if farmers_df.empty:
        st.warning("Please register a farmer profile first to view dashboard telemetry.")
    else:
        # Farmer Select
        farmer_options = {f"{row['name']} ({row['crop_type']})": row['id'] for _, row in farmers_df.iterrows()}
        selected_farmer_label = st.selectbox("Select Active Farmer Profile", list(farmer_options.keys()))
        selected_farmer_id = farmer_options[selected_farmer_label]
        
        # Get details of selected farmer
        farmer_details = farmers_df[farmers_df['id'] == selected_farmer_id].iloc[0]
        
        # Get last weather entry & last irrigation entry for this farmer
        history_farmer = get_irrigation_history(selected_farmer_id)
        
        latest_moisture = 35.0 # default
        latest_temp = 25.0
        latest_humidity = 60.0
        latest_rain_prob = 15.0
        latest_wind = 10.0
        latest_status = "N/A"
        latest_duration = 0
        latest_water = 0
        latest_time = "N/A"
        
        if not history_farmer.empty:
            latest_row = history_farmer.iloc[0]
            latest_moisture = latest_row['soil_moisture']
            latest_temp = latest_row['temperature']
            latest_humidity = latest_row['humidity']
            latest_rain_prob = latest_row['rain_prob']
            latest_status = latest_row['status']
            latest_duration = latest_row['duration_minutes']
            latest_water = latest_row['water_liters']
            latest_time = latest_row['recommended_time']
            
        # Layout metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        # 1. Soil Moisture Gauge
        with col1:
            color = "#D32F2F" if latest_moisture < 30 else ("#F57C00" if latest_moisture < 45 else "#388E3C")
            st.markdown(f"""
                <div class="metric-card" style="border-left-color: {color};">
                    <div class="metric-title">Soil Moisture Content</div>
                    <div class="metric-value">{latest_moisture}%</div>
                    <div style="font-size: 11px; margin-top:5px; color:#718096;">Latest Sensor Input</div>
                </div>
            """, unsafe_allow_html=True)
            
        # 2. Water Tank Level (Simulated)
        with col2:
            # Simple simulation: base on soil moisture level. 
            # High soil moisture = low water tank (used up) or high level. Let's make a mock tank level.
            tank_level = max(15, min(95, int(100 - (latest_moisture * 1.2))))
            tank_color = "#388E3C" if tank_level > 35 else "#D32F2F"
            st.markdown(f"""
                <div class="metric-card" style="border-left-color: {tank_color};">
                    <div class="metric-title">Water Tank capacity</div>
                    <div class="metric-value">{tank_level}%</div>
                    <div style="font-size: 11px; margin-top:5px; color:#718096;">
                        {'⚠️ Tank level low!' if tank_level <= 35 else 'Optimal Water Supply'}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        # 3. Weather
        with col3:
            st.markdown(f"""
                <div class="metric-card" style="border-left-color: #1976D2;">
                    <div class="metric-title">Outdoor Temp & Rain</div>
                    <div class="metric-value">{latest_temp}°C / {latest_rain_prob:.0f}%</div>
                    <div style="font-size: 11px; margin-top:5px; color:#718096;">Precipitation Chance</div>
                </div>
            """, unsafe_allow_html=True)
            
        # 4. Irrigation Status
        with col4:
            bg_badge = "#E8F5E9" if latest_status == "YES" else "#FFEBEE"
            txt_color = "#2E7D32" if latest_status == "YES" else "#C62828"
            st.markdown(f"""
                <div class="metric-card" style="border-left-color: {txt_color};">
                    <div class="metric-title">Irrigation Decision</div>
                    <div class="metric-value" style="color: {txt_color};">{latest_status}</div>
                    <div style="font-size: 11px; margin-top:5px; color:#718096;">
                        {f'Duration: {latest_duration} mins ({latest_water:.0f} L)' if latest_status == 'YES' else 'Soil moisture healthy / rain expected'}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        # Dashboard Alerts & Notifications
        st.markdown("<h3 class='section-header'>Notifications & Active Alerts</h3>", unsafe_allow_html=True)
        alerts_found = False
        
        if latest_rain_prob >= 75.0:
            st.warning("⚠️ **Heavy Rain Expected**: Forecast predicts a high likelihood of rain. Hold off manual irrigation schedules to conserve water.")
            alerts_found = True
        if latest_moisture < 30.0:
            st.error("🚨 **Low Soil Moisture Alert**: Soil moisture levels are below critical 30% threshold. Recommended scheduling action required immediately.")
            alerts_found = True
        if tank_level < 35.0:
            st.error("🚨 **Water Tank Level Low**: Water storage reserves are critical. Schedule lower volume irrigation to protect pump integrity.")
            alerts_found = True
        if latest_status == "NO" and latest_moisture >= 45.0:
            st.success("✅ **Optimal Conditions**: Soil moisture levels are in healthy range. No watering required.")
            alerts_found = True
            
        if not alerts_found:
            st.info("ℹ️ No active system alerts or moisture flags at this time.")
            
        # Historical charts using matplotlib
        st.markdown("<h3 class='section-header'>Moisture Trends & Water Consumption (Last 7 Logs)</h3>", unsafe_allow_html=True)
        if len(history_farmer) < 2:
            st.info("Log history details will appear here once more recommendation entries are saved.")
        else:
            # Prepare plot data
            chart_df = history_farmer.head(7).iloc[::-1] # Reverse to chronological order
            chart_df['date_short'] = chart_df['date_time'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S").strftime("%m/%d %H:%M"))
            
            fig, ax1 = plt.subplots(figsize=(10, 3.5))
            
            # Line chart for soil moisture
            color = '#1B5E20'
            ax1.set_xlabel('Log Timestamp')
            ax1.set_ylabel('Soil Moisture (%)', color=color)
            ax1.plot(chart_df['date_short'], chart_df['soil_moisture'], color=color, marker='o', linewidth=2, label='Soil Moisture')
            ax1.tick_params(axis='y', labelcolor=color)
            ax1.set_ylim(0, 100)
            
            # Bar chart for water quantity
            ax2 = ax1.twinx()
            color = '#1976D2'
            ax2.set_ylabel('Water Recommended (Liters)', color=color)
            ax2.bar(chart_df['date_short'], chart_df['water_liters'], color=color, alpha=0.3, width=0.4, label='Water Quantity')
            ax2.tick_params(axis='y', labelcolor=color)
            
            fig.tight_layout()
            st.pyplot(fig)

# ----------------- PAGE 3: FARMER REGISTRATION -----------------
elif page == "👤 Farmer Registration":
    st.markdown("<h1 class='main-header'>Register Farmer Profile</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Profile Form")
        with st.form("farmer_reg_form"):
            name = st.text_input("Farmer Full Name", placeholder="e.g. John Doe")
            location = st.text_input("Farm Location / City", placeholder="e.g. Salinas, CA")
            crop_type = st.selectbox("Crop Type", ["Lettuce", "Almonds", "Apples", "Rice", "Corn", "Wheat", "Tomatoes"])
            soil_type = st.selectbox("Soil Type", ["Sandy", "Sandy Clay", "Loamy", "Silt Loam", "Clayey"])
            farm_size = st.number_input("Farm Size (Acres / Hectares)", min_value=0.1, max_value=1000.0, value=10.0, step=0.5)
            
            submit = st.form_submit_button("Register Farmer Profile")
            
            if submit:
                if name.strip() == "" or location.strip() == "":
                    st.error("Please fill in both name and location details.")
                else:
                    new_id = add_farmer(name, location, crop_type, soil_type, farm_size)
                    st.success(f"Successfully registered farmer {name} with ID: {new_id}!")
                    st.rerun()
                    
    with col2:
        st.markdown("### Registered Profiles")
        df = get_all_farmers()
        if df.empty:
            st.info("No farmers registered yet.")
        else:
            st.dataframe(
                df[['id', 'name', 'location', 'crop_type', 'soil_type', 'farm_size']],
                hide_index=True,
                use_container_width=True
            )

# ----------------- PAGE 4: WEATHER -----------------
elif page == "🌤️ Weather":
    st.markdown("<h1 class='main-header'>Location Weather forecast</h1>", unsafe_allow_html=True)
    
    farmers_df = get_all_farmers()
    
    # Allow searching weather by raw location text or pulling from active farmer profile
    source_type = st.radio("Query Source", ["Select Registered Farmer Profile Location", "Input Location Manually"])
    
    target_location = ""
    if source_type == "Select Registered Farmer Profile Location":
        if farmers_df.empty:
            st.warning("No farmer profiles found. Register a profile first or write manual location.")
        else:
            farmer_options = {f"{row['name']} ({row['location']})": row['location'] for _, row in farmers_df.iterrows()}
            selected_lbl = st.selectbox("Select Profile Location", list(farmer_options.keys()))
            target_location = farmer_options[selected_lbl]
    else:
        target_location = st.text_input("Enter Location Name (City, State/Country)", "Seattle, WA")
        
    if target_location:
        api_key = st.text_input("Override OpenWeather API Key (Leave empty to use mock forecast simulation)", type="password")
        
        if st.button("Query Forecast Data"):
            with st.spinner("Fetching forecast details..."):
                weather_res = fetch_weather_data(target_location, api_key=api_key)
                
                # Check for warnings/notices
                if "notice" in weather_res:
                    st.info(f"💡 {weather_res['notice']}")
                    
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                        <div class="metric-card" style="border-left-color: #EF6C00;">
                            <div class="metric-title">Temperature</div>
                            <div class="metric-value">{weather_res['temp']}°C</div>
                            <div style="font-size: 11px; margin-top:5px; color:#718096;">{weather_res['description']}</div>
                        </div>
                        <div class="metric-card" style="border-left-color: #0288D1;">
                            <div class="metric-title">Humidity</div>
                            <div class="metric-value">{weather_res['humidity']}%</div>
                        </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                        <div class="metric-card" style="border-left-color: #37474F;">
                            <div class="metric-title">Wind Speed</div>
                            <div class="metric-value">{weather_res['wind_speed']} km/h</div>
                        </div>
                        <div class="metric-card" style="border-left-color: #2E7D32;">
                            <div class="metric-title">Precipitation Chance</div>
                            <div class="metric-value">{weather_res['rain_probability']}%</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                st.markdown(f"**Data Source Tag**: `{weather_res['source']}`")

# ----------------- PAGE 5: AI RECOMMENDATION -----------------
elif page == "🤖 AI Recommendation":
    st.markdown("<h1 class='main-header'>Agent Evaluation & Recommendations</h1>", unsafe_allow_html=True)
    
    farmers_df = get_all_farmers()
    
    if farmers_df.empty:
        st.warning("Please register a farmer profile to run recommendations.")
    else:
        # Step 1: Select Farmer
        farmer_options = {f"{row['name']} ({row['crop_type']})": row['id'] for _, row in farmers_df.iterrows()}
        selected_farmer_lbl = st.selectbox("Select Target Farmer Profile", list(farmer_options.keys()))
        selected_farmer_id = farmer_options[selected_farmer_lbl]
        
        # Load profile details
        profile = farmers_df[farmers_df['id'] == selected_farmer_id].iloc[0]
        
        st.markdown(f"**Selected Profile Details**: Crop: `{profile['crop_type']}` | Soil: `{profile['soil_type']}` | Farm Size: `{profile['farm_size']} ac/ha` | Location: `{profile['location']}`")
        
        # Step 2: Fetch current weather for the profile location to pre-fill values
        if 'weather_prefetch' not in st.session_state or st.session_state.get('prefetch_loc') != profile['location']:
            with st.spinner("Fetching pre-fill weather values for location..."):
                st.session_state['weather_prefetch'] = fetch_weather_data(profile['location'])
                st.session_state['prefetch_loc'] = profile['location']
                
        p_weather = st.session_state['weather_prefetch']
        
        # Inputs Form
        st.markdown("<h3 class='section-header'>Environmental & Sensor Readings</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            soil_moisture = st.slider("Current Soil Moisture Content (%)", 0.0, 100.0, 28.0, 0.5)
            temp = st.number_input("Air Temperature (°C)", value=float(p_weather['temp']), step=0.5)
            humidity = st.slider("Relative Humidity (%)", 0.0, 100.0, float(p_weather['humidity']))
        with col2:
            rain_prob = st.slider("Forecast Rain Probability (%)", 0.0, 100.0, float(p_weather['rain_probability']))
            wind_speed = st.number_input("Wind Speed (km/h)", value=float(p_weather['wind_speed']), step=0.5)
            gemini_key = st.text_input("Gemini API Key (Leave empty to use rule-based fallback decision)", type="password")
            
        if st.button("Evaluate Watering Recommendation", type="primary"):
            with st.spinner("Agent running evaluation..."):
                # Run AI Recommendation
                ai_rec = get_irrigation_recommendation(
                    farmer_name=profile['name'],
                    location=profile['location'],
                    crop_type=profile['crop_type'],
                    soil_type=profile['soil_type'],
                    farm_size=profile['farm_size'],
                    soil_moisture=soil_moisture,
                    temp=temp,
                    humidity=humidity,
                    rain_prob=rain_prob,
                    wind_speed=wind_speed,
                    api_key=gemini_key
                )
                
                # Run Scikit-learn Prediction Model
                ml_pred_status, ml_conf = predict_irrigation_requirement(
                    soil_moisture=soil_moisture,
                    temp=temp,
                    humidity=humidity,
                    rain_prob=rain_prob,
                    wind_speed=wind_speed
                )
                
                # Show fallback warnings if any
                if "notice" in ai_rec:
                    st.info(f"💡 {ai_rec['notice']}")
                    
                # Save recommendation record to DB
                log_irrigation(
                    farmer_id=selected_farmer_id,
                    soil_moisture=soil_moisture,
                    temperature=temp,
                    humidity=humidity,
                    rain_prob=rain_prob,
                    duration_minutes=int(ai_rec['duration_minutes']),
                    water_liters=float(ai_rec['water_liters']),
                    recommended_time=ai_rec['recommended_time'],
                    status=ai_rec['irrigation_required'],
                    reason=ai_rec['reason']
                )
                
                # Display Results
                st.markdown("<h3 class='section-header'>Agent Evaluation Results</h3>", unsafe_allow_html=True)
                
                col_res1, col_res2 = st.columns([2, 1])
                
                with col_res1:
                    status_color = "#2E7D32" if ai_rec['irrigation_required'] == "YES" else "#C62828"
                    st.markdown(f"""
                        <div style="background-color: #ffffff; padding: 25px; border-radius: 12px; border-left: 8px solid {status_color}; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                            <h2 style="color: {status_color}; margin-top: 0;">Irrigation Required: {ai_rec['irrigation_required']}</h2>
                            <p style="font-size: 16px; line-height: 1.6; color: #4A5568;"><b>Agent Justification:</b><br>{ai_rec['reason']}</p>
                            <hr style="border-top: 1px solid #E2E8F0; margin: 15px 0;">
                            <div style="display: flex; justify-content: space-between;">
                                <div>
                                    <span style="color:#718096; font-size:12px; font-weight:600; text-transform:uppercase;">Recommended Time</span><br>
                                    <b style="font-size:16px; color:#2D3748;">{ai_rec['recommended_time']}</b>
                                </div>
                                <div>
                                    <span style="color:#718096; font-size:12px; font-weight:600; text-transform:uppercase;">Duration</span><br>
                                    <b style="font-size:16px; color:#2D3748;">{ai_rec['duration_minutes']} Minutes</b>
                                </div>
                                <div>
                                    <span style="color:#718096; font-size:12px; font-weight:600; text-transform:uppercase;">Water Required</span><br>
                                    <b style="font-size:16px; color:#2D3748;">{ai_rec['water_liters']:.0f} Liters</b>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    st.caption(f"Decision Logic Engine: `{ai_rec['agent_source']}`")
                    
                with col_res2:
                    # ML Model box
                    ml_badge_color = "#C8E6C9" if ml_pred_status == "YES" else "#FFCDD2"
                    ml_txt_color = "#2E7D32" if ml_pred_status == "YES" else "#C62828"
                    st.markdown(f"""
                        <div style="background-color: #F7FAFC; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; text-align: center;">
                            <h4 style="margin-top:0; color:#4A5568;">ML Prediction Model</h4>
                            <span style="background-color: {ml_badge_color}; color: {ml_txt_color}; padding: 6px 16px; border-radius: 20px; font-weight: 700; font-size: 18px;">
                                {ml_pred_status}
                            </span>
                            <p style="margin-top:15px; font-size:13px; color:#718096;">
                                Model Type: <b>Random Forest Classifier</b><br>
                                Prediction Confidence: <b>{ml_conf}%</b>
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                st.success("Irrigation recommendation logged to database history successfully.")

# ----------------- PAGE 6: HISTORY -----------------
elif page == "📜 History":
    st.markdown("<h1 class='main-header'>Irrigation Action History Logs</h1>", unsafe_allow_html=True)
    
    farmers_df = get_all_farmers()
    
    if farmers_df.empty:
        st.info("Register farmer profiles to view local history.")
    else:
        # Filters
        farmer_options = {"All Farmers": None}
        for _, row in farmers_df.iterrows():
            farmer_options[f"{row['name']} ({row['crop_type']})"] = row['id']
            
        selected_filter = st.selectbox("Filter History Logs by Farmer", list(farmer_options.keys()))
        selected_id = farmer_options[selected_filter]
        
        history_logs = get_irrigation_history(selected_id)
        
        if history_logs.empty:
            st.warning("No irrigation recommendation runs logged for this selection.")
        else:
            # Re-format DataFrame for presentation
            show_df = history_logs.copy()
            show_df = show_df[['id', 'date_time', 'farmer_name', 'crop_type', 'soil_moisture', 'temperature', 'rain_prob', 'status', 'water_liters', 'duration_minutes', 'reason']]
            show_df.columns = ['ID', 'Date & Time', 'Farmer Profile', 'Crop', 'Soil Moisture (%)', 'Temperature (°C)', 'Rain Prob (%)', 'Irrigated?', 'Water (Liters)', 'Duration (Mins)', 'Evaluation Justification']
            
            st.dataframe(show_df, hide_index=True, use_container_width=True)

# ----------------- PAGE 7: REPORTS -----------------
elif page == "📈 Reports":
    st.markdown("<h1 class='main-header'>Water Consumption Reports</h1>", unsafe_allow_html=True)
    
    farmers_df = get_all_farmers()
    
    if farmers_df.empty:
        st.warning("Register farmer profiles to compile reports.")
    else:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Generate PDF Report")
            
            # Select Farmer or aggregate
            farmer_options = {"All Farmers": None}
            for _, row in farmers_df.iterrows():
                farmer_options[f"{row['name']} ({row['crop_type']})"] = row['id']
                
            selected_f = st.selectbox("Select Report Target Profile", list(farmer_options.keys()))
            farmer_id = farmer_options[selected_f]
            farmer_name_clean = "All Farmers" if not farmer_id else selected_f.split(" (")[0]
            
            # Report period
            report_type = st.selectbox("Select Compilation Period", ["Daily", "Weekly", "Monthly"])
            
            if st.button("Compile & Export PDF Report", type="primary"):
                with st.spinner("Compiling PDF document layout..."):
                    pdf_path = generate_pdf_report(farmer_id, farmer_name_clean, report_type)
                    
                    if os.path.exists(pdf_path):
                        with open(pdf_path, "rb") as f:
                            pdf_bytes = f.read()
                        
                        st.success("PDF Compiled successfully!")
                        st.download_button(
                            label="⬇️ Download PDF Report",
                            data=pdf_bytes,
                            file_name=os.path.basename(pdf_path),
                            mime="application/pdf"
                        )
                    else:
                        st.error("Error generating PDF document file.")
                        
        with col2:
            st.markdown("### Archive of Generated Report Entries")
            reports_df = get_all_reports()
            
            if reports_df.empty:
                st.info("No compiled PDF reports registered yet. Generate one to view history.")
            else:
                st.dataframe(
                    reports_df[['id', 'title', 'type', 'date_generated', 'file_path']],
                    hide_index=True,
                    use_container_width=True
                )

# ----------------- PAGE 8: ADMIN -----------------
elif page == "⚙️ Admin":
    st.markdown("<h1 class='main-header'>Admin Management Console</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Profile Management", "History Logs", "Data Export"])
    
    with tab1:
        st.markdown("### Registered Farmers List")
        farmers = get_all_farmers()
        if farmers.empty:
            st.info("No farmers registered.")
        else:
            for idx, row in farmers.iterrows():
                col_f1, col_f2 = st.columns([4, 1])
                with col_f1:
                    st.markdown(f"👤 **{row['name']}** | {row['location']} | Crop: **{row['crop_type']}** | Soil: **{row['soil_type']}** | Size: **{row['farm_size']} ac/ha**")
                with col_f2:
                    if st.button("Delete Profile", key=f"del_f_{row['id']}"):
                        delete_farmer(row['id'])
                        st.success(f"Deleted profile {row['name']}")
                        st.rerun()
                st.markdown("<hr style='margin: 8px 0; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
                
    with tab2:
        st.markdown("### Clear Recommendation Records")
        history = get_irrigation_history()
        if history.empty:
            st.info("No logs present in the database.")
        else:
            for idx, row in history.iterrows():
                col_h1, col_h2 = st.columns([4, 1])
                with col_h1:
                    st.markdown(f"📜 **{row['date_time']}** - Profile: **{row['farmer_name']}** | Irrigated: **{row['status']}** ({row['water_liters']:.0f} L)")
                with col_h2:
                    if st.button("Delete Record", key=f"del_h_{row['id']}"):
                        delete_irrigation_record(row['id'])
                        st.success("Deleted history log record.")
                        st.rerun()
                st.markdown("<hr style='margin: 8px 0; border-top: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
                
    with tab3:
        st.markdown("### Export Tables to Excel")
        
        export_target = st.selectbox("Select Database Table to Export", ["Farmers", "IrrigationHistory", "Reports"])
        
        if st.button("Generate Excel Export"):
            conn = get_db_connection()
            try:
                exp_df = pd.read_sql_query(f"SELECT * FROM {export_target}", conn)
                conn.close()
                
                # Excel file writing to memory buffers
                import io
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    exp_df.to_excel(writer, sheet_name=export_target, index=False)
                    
                st.success(f"Excel table compiled for `{export_target}`! Click below to download.")
                st.download_button(
                    label=f"⬇️ Download {export_target}.xlsx",
                    data=buffer.getvalue(),
                    file_name=f"{export_target.lower()}_export.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                conn.close()
                st.error(f"Error compiling Excel output: {str(e)}")
