from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FarmerCreate(BaseModel):
    name: str = Field(..., example="John Doe")
    location: str = Field(..., example="Salinas Valley, CA")
    crop_type: str = Field(..., example="Lettuce")
    soil_type: str = Field(..., example="Loamy")
    farm_size: float = Field(..., example=15.5)
    farm_unit: str = Field(default="Acres", example="Acres")

class RecommendationRequest(BaseModel):
    farmer_id: int = Field(..., example=1)
    soil_moisture: float = Field(..., example=25.0)
    temp: Optional[float] = None
    humidity: Optional[float] = None
    rain_prob: Optional[float] = None
    wind_speed: Optional[float] = None
    gemini_key: str = ""

class ScheduleCreate(BaseModel):
    farmer_id: int = Field(..., example=1)
    scheduled_time: datetime = Field(..., example="2026-07-10T06:00:00")
    duration_minutes: int = Field(..., example=30)

class ScheduleResponse(BaseModel):
    id: int
    farmer_id: int
    scheduled_time: datetime
    duration_minutes: int
    status: str

class AlertResponse(BaseModel):
    id: int
    farmer_id: int
    timestamp: datetime
    channel: str
    message: str
