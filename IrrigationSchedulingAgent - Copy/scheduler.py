# scheduler.py
"""Background scheduler that runs irrigation recommendations at a configurable interval.

Uses APScheduler (BackgroundScheduler) to trigger the recommendation engine for each
farmer and stores the resulting schedule in the database. Also sends alerts.
"""

import yaml
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from database import get_db_connection, log_irrigation, add_schedule
from irrigation_agent import get_irrigation_recommendation
from alerts import send_email_alert, log_alert

# Load configuration
with open("config.yaml", "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f) or {}

SCHEDULE_INTERVAL = cfg.get("schedule_interval", "0 * * * *")  # default hourly


def cron_expr_to_kwargs(expr: str) -> dict:
    """Convert a 5‑field cron string to APScheduler keyword arguments.
    Supports minute hour day month day_of_week.
    """
    minute, hour, day, month, day_of_week = expr.split()
    return {
        "minute": minute,
        "hour": hour,
        "day": day,
        "month": month,
        "day_of_week": day_of_week,
    }


def run_recommendations_for_all():
    """Iterate over all farmers and log a recommendation.
    This function is intended to be called by the scheduler.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, location, crop_type, soil_type, farm_size, farm_unit FROM Farmers")
    farmers = cursor.fetchall()
    conn.close()

    import random

    for farmer in farmers:
        farmer_dict = dict(farmer)
        soil_moisture = random.uniform(10.0, 40.0)
        recommendation = get_irrigation_recommendation(
            farmer_name=farmer_dict["name"],
            location=farmer_dict["location"],
            crop_type=farmer_dict["crop_type"],
            soil_type=farmer_dict["soil_type"],
            farm_size=farmer_dict["farm_size"],
            farm_unit=farmer_dict["farm_unit"],
            soil_moisture=soil_moisture,
        )
        # Log to history
        log_irrigation(
            farmer_id=farmer_dict["id"],
            soil_moisture=soil_moisture,
            temperature=recommendation["temperature"],
            humidity=recommendation["humidity"],
            rain_prob=recommendation["rain_probability"],
            duration_minutes=int(recommendation["duration_minutes"]),
            water_liters=float(recommendation["water_liters"]),
            recommended_time=recommendation["recommended_time"],
            status=recommendation["irrigation_required"],
            reason=recommendation["reason"],
        )
        # Add to schedule table
        if recommendation["irrigation_required"] == "YES":
            # Scheduled time is today's recommended_time (assuming HH:MM AM/PM)
            # Convert to a datetime for today
            time_str = recommendation["recommended_time"]
            try:
                scheduled_dt = datetime.strptime(time_str, "%I:%M %p")
                scheduled_dt = datetime.now().replace(hour=scheduled_dt.hour, minute=scheduled_dt.minute, second=0, microsecond=0)
            except Exception:
                scheduled_dt = datetime.now()
            add_schedule(
                farmer_id=farmer_dict["id"],
                scheduled_time=scheduled_dt,
                duration_minutes=int(recommendation["duration_minutes"]),
            )
        # Send alert if enabled
        if recommendation["irrigation_required"] == "YES":
            subject = f"Irrigation Recommendation for {farmer_dict['name']}"
            body = f"Recommended at {recommendation['recommended_time']}: {recommendation['duration_minutes']} minutes, {recommendation['water_liters']} liters. Reason: {recommendation['reason']}"
            sent = send_email_alert(subject, body)
            if sent:
                log_alert(farmer_dict['id'], "email", body)
        print(f"[{datetime.now().isoformat()}] Processed farmer {farmer_dict['name']}: {recommendation['irrigation_required']}")


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_recommendations_for_all, "cron", **cron_expr_to_kwargs(SCHEDULE_INTERVAL))
    scheduler.start()
    print("Scheduler started with interval", SCHEDULE_INTERVAL)

if __name__ == "__main__":
    start_scheduler()
