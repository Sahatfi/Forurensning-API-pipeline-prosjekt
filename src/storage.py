import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path
import logging
import traceback as tb

logger = logging.getLogger(__name__)


def get_db_path():
    """Get path to database file"""
    db_dir = Path(__file__).resolve().parent.parent / "data"
    db_dir.mkdir(exist_ok=True)
    return db_dir / "prognoser.db"


def create_database():
    """Create database and prognoser table if they don't exist"""
    logger.info("Lager en database...")
    
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prognoser (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TIMESTAMP NOT NULL,
            
            -- Weather data
            timestamp_vær TIMESTAMP,
            latitude_vær REAL,
            longitude_vær REAL,
            air_pressure_at_sea_level REAL,
            air_temperature REAL,
            cloud_area_fraction REAL,
            relative_humidity REAL,
            wind_from_direction REAL,
            wind_speed REAL,
            
            -- Air quality metadata
            timestamp_for TIMESTAMP,
            latitude_for REAL,
            longitude_for REAL,
            stednavn TEXT,
            
            -- AQI values
            AQI REAL,
            AQI_no2 REAL,
            AQI_pm10 REAL,
            AQI_pm25 REAL,
            AQI_o3 REAL,
            
            -- NO2 measurements
            no2_concentration REAL,
            no2_nonlocal_fraction REAL,
            no2_nonlocal_fraction_seasalt REAL,
            no2_local_fraction_traffic_exhaust REAL,
            no2_local_fraction_traffic_nonexhaust REAL,
            no2_local_fraction_shipping REAL,
            no2_local_fraction_heating REAL,
            no2_local_fraction_industry REAL,
            
            -- PM10 measurements
            pm10_concentration REAL,
            pm10_nonlocal_fraction REAL,
            pm10_nonlocal_fraction_seasalt REAL,
            pm10_local_fraction_traffic_exhaust REAL,
            pm10_local_fraction_traffic_nonexhaust REAL,
            pm10_local_fraction_shipping REAL,
            pm10_local_fraction_heating REAL,
            pm10_local_fraction_industry REAL,
            
            -- PM25 measurements
            pm25_concentration REAL,
            pm25_nonlocal_fraction REAL,
            pm25_nonlocal_fraction_seasalt REAL,
            pm25_local_fraction_traffic_exhaust REAL,
            pm25_local_fraction_traffic_nonexhaust REAL,
            pm25_local_fraction_shipping REAL,
            pm25_local_fraction_heating REAL,
            pm25_local_fraction_industry REAL,
            
            -- O3 measurements
            o3_concentration REAL,
            o3_nonlocal_fraction REAL,
            o3_nonlocal_fraction_seasalt REAL,
            o3_local_fraction_traffic_exhaust REAL,
            o3_local_fraction_traffic_nonexhaust REAL,
            o3_local_fraction_shipping REAL,
            o3_local_fraction_heating REAL,
            o3_local_fraction_industry REAL,
            
            UNIQUE(timestamp_vær, latitude_vær, longitude_vær)
        )
    """)
    
    conn.commit()
    conn.close()
    
    logger.info(f"✅ Databasen klar på {db_path}")


def insert_forecast(inserted_dataframe):
    """Save forecast DataFrame to database"""
    logger.info("Lagrer prognose til database...")
    
    if inserted_dataframe is None or inserted_dataframe.empty:
        logger.error("Kan ikke lagre tom DataFrame")
        raise ValueError("DataFrame er tom")
    
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    
    try:
        # Add timestamp
        df = inserted_dataframe.copy()
        df['created_at'] = datetime.now().isoformat()
        
        # Convert NaN to None for SQLite compatibility
        df = df.where(pd.notna(df), None)
        
        # Save to database
        df.to_sql('prognoser', conn, if_exists='append', index=False)
        
        logger.info(f"✅ Lagret {len(df)} prognose(r) til database")
        
    except Exception as e:
        # Get full error chain
        full_error = tb.format_exc()
        
        # Check if UNIQUE constraint violation (duplicate)
        if 'UNIQUE constraint failed' in full_error or 'UNIQUE constraint' in str(e):
            logger.warning("⚠️ Prognose finnes allerede (duplikat), hoppet over")
        else:
            logger.error(f"❌ Database feil: {e}")
            raise
    finally:
        conn.close()