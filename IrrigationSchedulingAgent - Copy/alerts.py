# alerts.py
"""Simple alert helper – currently supports email notifications.

Configuration is taken from `config.yaml`. In a production setup you would add
SMS, push, or webhook integrations.
"""

import smtplib
from email.mime.text import MIMEText
import yaml
import sqlite3
import os
from datetime import datetime

# Load config (fallback to empty dict if missing)
try:
    with open("config.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
except FileNotFoundError:
    cfg = {}

EMAIL_ENABLED = cfg.get("email_alerts_enabled", False)
SMTP_SERVER = cfg.get("smtp_server", "")
SMTP_PORT = cfg.get("smtp_port", 587)
SMTP_USER = cfg.get("smtp_user", "")
SMTP_PASSWORD = cfg.get("smtp_password", "")
ALERT_RECIPIENT = cfg.get("alert_recipient", "")

# Database helpers for logging alerts
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database", "irrigation.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def log_alert(farmer_id: int, channel: str, message: str):
    """Record an alert in the Alerts table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Alerts (farmer_id, timestamp, channel, message) VALUES (?, ?, ?, ?)",
        (farmer_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), channel, message)
    )
    conn.commit()
    conn.close()

def send_email_alert(subject: str, body: str, recipient: str = ALERT_RECIPIENT) -> bool:
    """Send a simple plain‑text email alert.

    Returns True on success, False otherwise.
    """
    if not EMAIL_ENABLED or not recipient:
        return False
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = recipient
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"[alerts] Failed to send email: {e}")
        return False
