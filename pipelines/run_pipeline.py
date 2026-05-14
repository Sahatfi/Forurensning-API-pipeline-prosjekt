from src.data_loader import load_config, param_config_forecast, load_data, param_config_forurensning, forurensning_loading
from src.modeling import Data, ForurensningsModel
from src.data_processor import process_weather_data, process_airquality_data, merge_forecasts
from src.storage import get_db_path, create_database, insert_forecast
import json
import requests
from pydantic import ValidationError
import logging


logger = logging.getLogger(__name__)
def run_pipeline():
    logger.info("="*60)
    logger.info("Starter pipeline...")
    logger.info("="*60)
    #Adjusting configurationr
    config = load_config()
    #Adjusting for parameters for data loading
    url, headers, params  = param_config_forecast(config)

    #Try to load data:
    try:
        vær_data = load_data(url, headers, params)
    except requests.exceptions.RequestException as e:
        logger.error(f"Kunne ikke hente værdata etter 5 forsøk. Feilmelding: {e}")
        return None, None, None

    # Konverter vær til BaseModel(Validering)
    try :
        vær_valid = Data(**vær_data)  
        logger.info("Vær data validert!")
    except ValidationError as e: 
        logger.error(f"Vær  validering feilet: {e}")
        return None, None, None
    except Exception as e: 
        logger.error(f"Uforventet feil ved validating Vær  data: {e}")
        return None, None, None

    #Adjusting for parameters for data loading for forurensning
    url_foruransning, params_forurensning, headers_forurensning = param_config_forurensning(config)
    try:
        forurensnings_data = forurensning_loading(url_foruransning, headers_forurensning, params_forurensning)
    except requests.exceptions.RequestException as e:
        logger.error(f"Kunne ikke hente forurensningsdatadata etter 5 forsøk. Feilmelding: {e}")
        return None, None, None

    # Konverter forurensning til BaseModel(Validering)
    try:
        forurensning_valid = ForurensningsModel(**forurensnings_data)
        logger.info("Forurensningsdata validated successfully")
    except ValidationError as e: 
        logger.error(f"Forurensning validation feil: {e}")
        return None, None, None
    except Exception as e: 
        logger.error(f"Uforventet feil ved validering av forurensning data: {e}")
        return None, None, None
    
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
        logger.error(f"Koordinater matcher ikke! Vær: ({latitude_vær}, {longitude_vær}), Luftkvalitet: ({latitude_forurensning}, {longitude_forurensning})")
        raise ValueError("Koordinater er ikke de samme!")
    logger.info("Koordinater matcher")

    # Data prossessering:
    vær_df = process_weather_data(vær_valid)
    # Laging av air-quality dataframe
    forurensning_df = process_airquality_data(forurensning_valid)
    #Slå sammen dataframes
    merged_df = merge_forecasts(vær_df, forurensning_df)
    logger.info("Pipeline fullført")

    #Laging av database:
    get_db_path()
    create_database()
    #Inserting dataframe 
    insert_forecast(merged_df)

    return merged_df
