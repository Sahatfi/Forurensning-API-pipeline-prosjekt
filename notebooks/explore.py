import sys
import os
import pandas as pd
sys.path.insert(0, os.getcwd())
from src.data_loader import load_config, param_config_forecast, load_data, param_config_forurensning, forurensning_loading
from src.modeling import Data, ForurensningsModel
from src.data_processor import process_weather_data, process_airquality_data, merge_forecasts
import json
import requests
from pydantic import ValidationError

def run_pipeline():
    #Adjusting configurationr
    config = load_config()
    #Adjusting for parameters for data loading
    url, headers, params  = param_config_forecast(config)

    #Try to load data:
    try:
        print("Starter henting av værdata...")
        vær_data = load_data(url, headers, params)
        print("Værdata hentet suksessfullt!")
    except requests.exceptions.RequestException as e:
        print("Kunne ikke hente værdata etter 5 forsøk. Feilmelding:", e)
        return None

    # Konverter vær til BaseModel
    try :
        vær_valid = Data(**vær_data)  
        print("Vær data validated successfully")
    except ValidationError as e: 
        print(f"Vær  validation failed: {e}")
    except Exception as e: 
        print(f"Unexpected error validating Vær  data: {e}")
        return None

    #Adjusting for parameters for data loading for forurensning
    url_foruransning, params_forurensning, headers_forurensning = param_config_forurensning(config)
    try:
        print("Starter henting av  forurensningsdata...")
        forurensnings_data = forurensning_loading(url_foruransning, headers_forurensning, params_forurensning)
        print("ForurensningsdataData hentet suksessfullt!")
    except requests.exceptions.RequestException as e:
        print("Kunne ikke hente forurensningsdatadata etter 5 forsøk. Feilmelding:", e)
        return None

    # Konverter vær til BaseMode
    try:
        forurensning_valid = ForurensningsModel(**forurensnings_data)
        print("Forurensningsdata validated successfully")
    except ValidationError as e: 
        print(f"Forurensning validation failed: {e}")
        return None
    except Exception as e: 
        print(f"Unexpected error validating forurensning data: {e}")
        return None
    
    #validating location
    #Long og Lat forurensning
    latitude_vær = vær_valid.geometry.coordinates.lat
    longitude_vær = vær_valid.geometry.coordinates.lon
    # Long og Lat forurensning
    latitude_forurensning = forurensning_valid.meta.location.latitude
    longitude_forurensning = forurensning_valid.meta.location.longitude
    #Definerer differens
    lat_diff = abs(latitude_vær - latitude_forurensning)
    lon_diff = abs(longitude_vær - longitude_forurensning)
    if lat_diff > 0.05 or lon_diff > 0.05:
        raise ValueError(f"Koordinasjoner er ikke de samme! Vær vs Forurensnings long{longitude_vær} vs{longitude_forurensning},Vær vs Forurensnings lat {latitude_vær}{latitude_forurensning}")
    print("Koordinasjoner samsvarer!")
    
    # Laging av vær dataframe:
    vær_df = process_weather_data(vær_valid) 
    # Laging av air-quality dataframe
    forurensning_df = process_airquality_data(forurensning_valid)
    #Slå sammen dataframes
    merged_df = merge_forecasts(vær_df ,forurensning_df)


  
  # test_insert.py
from src.modeling import Data, ForurensningsModel
import pandas as pd
from datetime import datetime
from src.storage import get_db_path
import sqlite3
import pytest
from pydantic import ValidationError

# 1. Can your tests actually run?
python -m pytest tests/test_database.py -v

# Expected: FAIL (missing imports)

# 2. Does your edge case work?
python -c "
from src.data_loader import load_config, param_config_forecast, load_data
from src.modeling import Data
from src.data_processor import process_weather_data

config = load_config()
url, headers, params = param_config_forecast(config)
vær_data = load_data(url, headers, params)
vær_valid = Data(**vær_data)

# Get last valid index
max_index = len(vær_valid.properties.timeseries) - 1
print(f'Timeseries length: {len(vær_valid.properties.timeseries)}')
print(f'Trying hours_ahead={max_index} (should work)...')

# This should succeed but your code rejects it
process_weather_data(vær_valid, hours_ahead=max_index)
"

# Expected: ValueError even though it's valid