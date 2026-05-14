import pandas as pd
from datetime import datetime
from src.storage import get_db_path
import sqlite3

# Lag enkel test-data
test_data = {
    'created_at': [datetime.now().isoformat()],
    'timestamp_vær': ['2026-05-14T22:00:00'],
    'latitude_vær': [69.651],
    'longitude_vær': [18.955],
    'air_temperature': [5.2],
    'AQI': [45.0]
}

df = pd.DataFrame(test_data)

print("Test DataFrame:")
print(df)
print(f"\nDtypes:\n{df.dtypes}")

# Prøv å lagre
db_path = get_db_path()
conn = sqlite3.connect(db_path)

try:
    df.to_sql('prognoser', conn, if_exists='append', index=False)
    print("\n✅ SUCCESS! Data saved!")
except Exception as e:
    print(f"\n❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
finally:
    conn.close()
