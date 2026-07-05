import os
import sqlite3
from datetime import datetime, timedelta
import pandas as pd

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")
DB_PATH = os.path.join(DB_DIR, "irrigation.db")

def get_db_connection():
    """Establishes and returns a connection to the SQLite database."""
    # Ensure the directory exists
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema and populates with sample data if empty."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Farmers Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            crop_type TEXT NOT NULL,
            soil_type TEXT NOT NULL,
            farm_size REAL NOT NULL,
            farm_unit TEXT DEFAULT 'Acres',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Migration: Add farm_unit if it doesn't exist (in case database was already created)
    cursor.execute("PRAGMA table_info(Farmers)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'farm_unit' not in columns:
        cursor.execute("ALTER TABLE Farmers ADD COLUMN farm_unit TEXT DEFAULT 'Acres'")

    # 2. Weather Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER NOT NULL,
            temp REAL NOT NULL,
            humidity REAL NOT NULL,
            rain_probability REAL NOT NULL,
            wind_speed REAL NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (farmer_id) REFERENCES Farmers (id) ON DELETE CASCADE
        )
    """)

    # 3. IrrigationHistory Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS IrrigationHistory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER NOT NULL,
            soil_moisture REAL NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            rain_prob REAL NOT NULL,
            duration_minutes INTEGER NOT NULL,
            water_liters REAL NOT NULL,
            recommended_time TEXT NOT NULL,
            status TEXT NOT NULL, -- YES or NO
            reason TEXT NOT NULL,
            date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (farmer_id) REFERENCES Farmers (id) ON DELETE CASCADE
        )
    """)

    # 4. Reports Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            type TEXT NOT NULL, -- Daily, Weekly, Monthly
            date_generated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            file_path TEXT NOT NULL
        )
    """)

    # 5. IrrigationSchedule Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS IrrigationSchedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER NOT NULL,
            scheduled_time TIMESTAMP NOT NULL,
            duration_minutes INTEGER NOT NULL,
            status TEXT DEFAULT 'PENDING',
            FOREIGN KEY (farmer_id) REFERENCES Farmers (id) ON DELETE CASCADE
        )
    """)

    # 6. Alerts Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            channel TEXT NOT NULL,
            message TEXT NOT NULL,
            FOREIGN KEY (farmer_id) REFERENCES Farmers (id) ON DELETE CASCADE
        )
    """)

    conn.commit()

    # Seed sample data if Farmers table is empty
    cursor.execute("SELECT COUNT(*) FROM Farmers")
    if cursor.fetchone()[0] == 0:
        seed_sample_data(conn)

    conn.close()

def seed_sample_data(conn):
    """Inserts mock farmer profiles and irrigation logs to populate the app immediately."""
    cursor = conn.cursor()
    
    # Insert Farmers
    farmers_data = [
        ("John Doe", "Salinas Valley, CA", "Lettuce", "Loamy", 15.5, "Acres"),
        ("Maria Garcia", "Central Valley, CA", "Almonds", "Sandy Clay", 40.0, "Acres"),
        ("Chen Wei", "Yakima, WA", "Apples", "Silt Loam", 25.0, "Acres"),
        ("Amina Diallo", "Senegal River Basin", "Rice", "Clayey", 5.0, "Hectares")
    ]
    
    cursor.executemany("""
        INSERT INTO Farmers (name, location, crop_type, soil_type, farm_size, farm_unit, created_at)
        VALUES (?, ?, ?, ?, ?, ?, datetime('now', '-30 days'))
    """, farmers_data)
    
    # Get inserted farmer IDs
    cursor.execute("SELECT id, name, farm_size, farm_unit FROM Farmers")
    farmers = cursor.fetchall()
    
    # Generate past weather & irrigation logs (last 14 days)
    today = datetime.now()
    
    for f in farmers:
        fid, name, size, unit = f['id'], f['name'], f['farm_size'], f['farm_unit']
        multiplier = 4046.86 if unit == "Acres" else 10000.0
        size_m2 = size * multiplier
        
        # Insert Weather and Irrigation logs
        for i in range(14):
            log_date = today - timedelta(days=i)
            log_date_str = log_date.strftime("%Y-%m-%d %H:%M:%S")
            
            # Simple synthetic values based on crop types
            if "Lettuce" in name or fid == 1:
                temp, hum, rain_prob, wind = 22.0 + (i % 5), 60.0 - (i % 10), 10.0 + (i * 5) % 80, 5.0 + (i % 3)
                moisture = 25.0 + (i * 7) % 35
                status = "YES" if moisture < 35 and rain_prob < 40 else "NO"
                duration = 30 if status == "YES" else 0
                # Lettuce: 3.5 mm/day. Apply mm based on moisture factor.
                moisture_factor = (100.0 - moisture) / 100.0
                water = round(size_m2 * 3.5 * moisture_factor, 0) if status == "YES" else 0.0
                rec_time = "06:00 AM" if status == "YES" else "N/A"
                reason = "Soil moisture is low ({:.1f}%) and rain probability is low ({:.1f}%).".format(moisture, rain_prob) if status == "YES" else "Soil moisture is adequate ({:.1f}%) or rain is expected.".format(moisture)
            elif "Almonds" in name or fid == 2:
                temp, hum, rain_prob, wind = 32.0 + (i % 6), 40.0 - (i % 12), (i * 3) % 30, 8.0 + (i % 4)
                moisture = 18.0 + (i * 9) % 30
                status = "YES" if moisture < 28 and rain_prob < 30 else "NO"
                duration = 60 if status == "YES" else 0
                # Almonds: 6.5 mm/day.
                moisture_factor = (100.0 - moisture) / 100.0
                water = round(size_m2 * 6.5 * moisture_factor, 0) if status == "YES" else 0.0
                rec_time = "07:30 PM" if status == "YES" else "N/A"
                reason = "High temperature ({:.1f}°C) and low soil moisture ({:.1f}%).".format(temp, moisture) if status == "YES" else "Soil moisture levels are within optimal range."
            else:
                temp, hum, rain_prob, wind = 25.0 + (i % 4), 55.0 - (i % 8), (i * 8) % 90, 6.0 + (i % 2)
                moisture = 30.0 + (i * 6) % 40
                status = "YES" if moisture < 30 and rain_prob < 40 else "NO"
                duration = 45 if status == "YES" else 0
                # Default: 5.0 mm/day.
                moisture_factor = (100.0 - moisture) / 100.0
                water = round(size_m2 * 5.0 * moisture_factor, 0) if status == "YES" else 0.0
                rec_time = "05:00 AM" if status == "YES" else "N/A"
                reason = "Irrigation triggered due to soil moisture dropping to {:.1f}%.".format(moisture) if status == "YES" else "No irrigation needed. Rain expected or soil moisture healthy."
            
            # Write weather
            cursor.execute("""
                INSERT INTO Weather (farmer_id, temp, humidity, rain_probability, wind_speed, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (fid, temp, hum, rain_prob, wind, log_date_str))
            
            # Write irrigation history
            cursor.execute("""
                INSERT INTO IrrigationHistory (farmer_id, soil_moisture, temperature, humidity, rain_prob, duration_minutes, water_liters, recommended_time, status, reason, date_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (fid, moisture, temp, hum, rain_prob, duration, water, rec_time, status, reason, log_date_str))
            
    conn.commit()

# Helper operations for Farmers
def add_farmer(name, location, crop_type, soil_type, farm_size, farm_unit='Acres'):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Farmers (name, location, crop_type, soil_type, farm_size, farm_unit)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, location, crop_type, soil_type, farm_size, farm_unit))
    conn.commit()
    farmer_id = cursor.lastrowid
    conn.close()
    return farmer_id

def get_all_farmers():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM Farmers ORDER BY created_at DESC", conn)
    conn.close()
    return df

def delete_farmer(farmer_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Cascading deletes manually in sqlite
    cursor.execute("DELETE FROM Weather WHERE farmer_id = ?", (farmer_id,))
    cursor.execute("DELETE FROM IrrigationHistory WHERE farmer_id = ?", (farmer_id,))
    cursor.execute("DELETE FROM Farmers WHERE id = ?", (farmer_id,))
    conn.commit()
    conn.close()

# Helper operations for Weather
def log_weather(farmer_id, temp, humidity, rain_probability, wind_speed):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Weather (farmer_id, temp, humidity, rain_probability, wind_speed)
        VALUES (?, ?, ?, ?, ?)
    """, (farmer_id, temp, humidity, rain_probability, wind_speed))
    conn.commit()
    conn.close()

# Helper operations for IrrigationHistory
def log_irrigation(farmer_id, soil_moisture, temperature, humidity, rain_prob, duration_minutes, water_liters, recommended_time, status, reason, date_time=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if date_time is None:
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO IrrigationHistory (farmer_id, soil_moisture, temperature, humidity, rain_prob, duration_minutes, water_liters, recommended_time, status, reason, date_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (farmer_id, soil_moisture, temperature, humidity, rain_prob, duration_minutes, water_liters, recommended_time, status, reason, date_time))
    conn.commit()
    conn.close()

def get_irrigation_history(farmer_id=None):
    conn = get_db_connection()
    if farmer_id:
        query = """
            SELECT h.*, f.name as farmer_name, f.crop_type, f.farm_size, f.farm_unit 
            FROM IrrigationHistory h 
            JOIN Farmers f ON h.farmer_id = f.id
            WHERE h.farmer_id = ?
            ORDER BY h.date_time DESC
        """
        df = pd.read_sql_query(query, conn, params=(farmer_id,))
    else:
        query = """
            SELECT h.*, f.name as farmer_name, f.crop_type, f.farm_size, f.farm_unit 
            FROM IrrigationHistory h 
            JOIN Farmers f ON h.farmer_id = f.id
            ORDER BY h.date_time DESC
        """
        df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def add_schedule(farmer_id: int, scheduled_time: datetime, duration_minutes: int):
    """Insert a new irrigation schedule entry."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO IrrigationSchedule (farmer_id, scheduled_time, duration_minutes) VALUES (?, ?, ?)",
        (farmer_id, scheduled_time.strftime("%Y-%m-%d %H:%M:%S"), duration_minutes)
    )
    conn.commit()
    conn.close()

def get_upcoming_schedules(farmer_id: int = None):
    """Return upcoming schedules (scheduled_time >= now)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if farmer_id:
        cursor.execute(
            "SELECT * FROM IrrigationSchedule WHERE farmer_id = ? AND scheduled_time >= ? ORDER BY scheduled_time",
            (farmer_id, now_str)
        )
    else:
        cursor.execute(
            "SELECT * FROM IrrigationSchedule WHERE scheduled_time >= ? ORDER BY scheduled_time",
            (now_str,)
        )
    rows = cursor.fetchall()
    conn.close()
    # Convert to DataFrame for consistency
    import pandas as pd
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description]) if rows else pd.DataFrame()
    return df


# Reports Table Helpers
def get_alerts(farmer_id: int = None):
    """Fetch recent alerts, optionally filtered by farmer."""
    conn = get_db_connection()
    cursor = conn.cursor()
    if farmer_id:
        cursor.execute("SELECT * FROM Alerts WHERE farmer_id = ? ORDER BY timestamp DESC", (farmer_id,))
    else:
        cursor.execute("SELECT * FROM Alerts ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    import pandas as pd
    df = pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description]) if rows else pd.DataFrame()
    return df


def get_all_reports():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM Reports ORDER BY date_generated DESC", conn)
    conn.close()
    return df

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)
