
import pytest
from src.data_loader import load_config, param_config_forecast, load_data
from unittest.mock import MagicMock
import responses
import requests
from requests.exceptions import HTTPError
from unittest.mock import patch, Mock

from src.storage import get_db_path

db_path = get_db_path()
print(f"Database will be at: {db_path}")

def create_database():
    """Create database and forecasts table if they don't exist"""
    logger.info("Setting up database...")
    
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS forecasts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            forecast_time TEXT NOT NULL,
            created_at TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            location_name TEXT,
            air_temperature REAL,
            air_pressure_at_sea_level REAL,
            cloud_area_fraction REAL,
            relative_humidity REAL,
            wind_from_direction REAL,
            wind_speed REAL,
            aqi REAL,
            aqi_no2 REAL,
            aqi_pm10 REAL,
            aqi_pm25 REAL,
            aqi_o3 REAL,
            no2_concentration REAL,
            pm10_concentration REAL,
            pm25_concentration REAL,
            o3_concentration REAL,
            UNIQUE(forecast_time, latitude, longitude)
        )
    """)
    
    conn.commit()
    conn.close()
    
    logger.info(f"✅ Database ready at {db_path}")