import os
import io
import pandas as pd
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import project modules
from database import (
    init_db, get_all_farmers, add_farmer,
    delete_farmer,
    get_irrigation_history, log_irrigation, delete_irrigation_record,
    get_all_reports, get_db_connection,
    add_schedule, get_upcoming_schedules, get_alerts
)
from weather import fetch_weather_data
from irrigation_agent import get_irrigation_recommendation
from recommendation import predict_irrigation_requirement, train_and_save_ml_model
from scheduler import start_scheduler
from schemas import ScheduleCreate, ScheduleResponse, AlertResponse

from report import generate_pdf_report, REPORTS_DIR

app = FastAPI(title="Irrigation Scheduling Agent API", version="1.0.0")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup tasks
@app.on_event("startup")
def startup_event():
    init_db()
    train_and_save_ml_model()
    start_scheduler()

# Serve reports directory
app.mount("/reports", StaticFiles(directory=REPORTS_DIR), name="reports")

# Models for POST requests
class FarmerCreate(BaseModel):
    name: str
    location: str
    crop_type: str
    soil_type: str
    farm_size: float
    farm_unit: str = "Acres"

class RecommendationRequest(BaseModel):
    farmer_id: int
    soil_moisture: float
    temp: float
    humidity: float
    rain_prob: float
    wind_speed: float
    gemini_key: str = ""

@app.get("/")
def get_index():
    return FileResponse("index.html")

@app.get("/api/farmers")
def list_farmers():
    df = get_all_farmers()
    if df.empty:
        return []
    return df.to_dict(orient="records")

@app.post("/api/farmers")
def create_farmer(farmer: FarmerCreate):
    if not farmer.name.strip() or not farmer.location.strip():
        raise HTTPException(status_code=400, detail="Name and location are required.")
    try:
        farmer_id = add_farmer(
            name=farmer.name,
            location=farmer.location,
            crop_type=farmer.crop_type,
            soil_type=farmer.soil_type,
            farm_size=farmer.farm_size,
            farm_unit=farmer.farm_unit
        )
        return {"id": farmer_id, "status": "success", "message": "Farmer registered successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/farmers/{farmer_id}")
def remove_farmer(farmer_id: int):
    try:
        delete_farmer(farmer_id)
        return {"status": "success", "message": "Farmer profile deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/weather")
def get_weather(location: str, api_key: str = ""):
    if not location.strip():
        raise HTTPException(status_code=400, detail="Location is required.")
    return fetch_weather_data(location, api_key=api_key)

@app.post("/api/recommendation")
def run_recommendation(req: RecommendationRequest):
    # Fetch farmer profile from DB to get name, location, crop, soil, size, unit
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Farmers WHERE id = ?", (req.farmer_id,))
    farmer = cursor.fetchone()
    conn.close()
    
    if not farmer:
        raise HTTPException(status_code=404, detail="Farmer profile not found.")
        
    farmer_dict = dict(farmer)
    
    try:
        # 1. Run AI / Rule-Based recommendation
        ai_rec = get_irrigation_recommendation(
            farmer_name=farmer_dict['name'],
            location=farmer_dict['location'],
            crop_type=farmer_dict['crop_type'],
            soil_type=farmer_dict['soil_type'],
            farm_size=farmer_dict['farm_size'],
            farm_unit=farmer_dict['farm_unit'],
            soil_moisture=req.soil_moisture,
            temp=req.temp,
            humidity=req.humidity,
            rain_prob=req.rain_prob,
            wind_speed=req.wind_speed,
            api_key=req.gemini_key
        )
        
        # 2. Run ML Prediction model
        ml_pred_status, ml_conf = predict_irrigation_requirement(
            soil_moisture=req.soil_moisture,
            temp=req.temp,
            humidity=req.humidity,
            rain_prob=req.rain_prob,
            wind_speed=req.wind_speed
        )
        
        # 3. Log the history record in the database
        log_irrigation(
            farmer_id=req.farmer_id,
            soil_moisture=req.soil_moisture,
            temperature=req.temp,
            humidity=req.humidity,
            rain_prob=req.rain_prob,
            duration_minutes=int(ai_rec['duration_minutes']),
            water_liters=float(ai_rec['water_liters']),
            recommended_time=ai_rec['recommended_time'],
            status=ai_rec['irrigation_required'],
            reason=ai_rec['reason']
        )
        
        return {
            "ai_recommendation": ai_rec,
            "ml_prediction": {
                "status": ml_pred_status,
                "confidence": ml_conf
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/history")
def get_history(farmer_id: int = None):
    df = get_irrigation_history(farmer_id)
    if df.empty:
        return []
    return df.to_dict(orient="records")

@app.delete("/api/history/{record_id}")
def remove_history_record(record_id: int):
    try:
        delete_irrigation_record(record_id)
        return {"status": "success", "message": "History log deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Schedule Endpoints
@app.get("/api/schedule")
def list_schedules(farmer_id: int = None):
    df = get_upcoming_schedules(farmer_id)
    if df.empty:
        return []
    return df.to_dict(orient="records")

@app.post("/api/schedule")
def create_schedule(schedule: ScheduleCreate):
    # schedule.scheduled_time is a datetime (pydantic will parse ISO string)
    add_schedule(
        farmer_id=schedule.farmer_id,
        scheduled_time=schedule.scheduled_time,
        duration_minutes=schedule.duration_minutes,
    )
    # Return the created schedule details
    df = get_upcoming_schedules(schedule.farmer_id)
    entry = df[(df["scheduled_time"] == schedule.scheduled_time.isoformat()) & (df["duration_minutes"] == schedule.duration_minutes)]
    if not entry.empty:
        row = entry.iloc[0]
        return ScheduleResponse(
            id=int(row["id"]),
            farmer_id=int(row["farmer_id"]),
            scheduled_time=row["scheduled_time"],
            duration_minutes=int(row["duration_minutes"]),
            status=row.get("status", "PENDING"),
        )
    return {"status": "success", "message": "Schedule created"}

# Alert Endpoints
@app.get("/api/alerts")
def list_alerts(farmer_id: int = None):
    df = get_alerts(farmer_id)
    if df.empty:
        return []
    return df.to_dict(orient="records")

@app.post("/api/reports")
def compile_report(farmer_id: int = None, farmer_name: str = "All Farmers", report_type: str = "Weekly"):
    try:
        pdf_path = generate_pdf_report(farmer_id, farmer_name, report_type)
        if os.path.exists(pdf_path):
            filename = os.path.basename(pdf_path)
            return {
                "status": "success", 
                "filename": filename,
                "download_url": f"/reports/{filename}"
            }
        else:
            raise HTTPException(status_code=500, detail="Error generating PDF report file.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports")
def list_reports():
    df = get_all_reports()
    if df.empty:
        return []
    return df.to_dict(orient="records")

@app.get("/api/export")
def export_table(table: str = Query(..., description="Farmers, IrrigationHistory or Reports")):
    if table not in ["Farmers", "IrrigationHistory", "Reports"]:
        raise HTTPException(status_code=400, detail="Invalid table name. Choose Farmers, IrrigationHistory, or Reports.")
    
    conn = get_db_connection()
    try:
        df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        conn.close()
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=table, index=False)
        output.seek(0)
        
        headers = {
            'Content-Disposition': f'attachment; filename="{table.lower()}_export.xlsx"'
        }
        return StreamingResponse(
            output, 
            headers=headers, 
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app_fastapi:app", host="127.0.0.1", port=8000, reload=True)
