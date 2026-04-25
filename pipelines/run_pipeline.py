from src.data_loader import load_config, param_config_forecast, load_data, param_config_forurensning, forurensning_loading
from src.modeling import Data, ForurensningsModel
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
        vær_data_basemodel = Data(**vær_data)  
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
        forurensnings_data_basemodel = ForurensningsModel(**forurensnings_data)
        print("Forurensningsdata validated successfully")
    except ValidationError as e: 
        print(f"Forurensning validation failed: {e}")
        return None
    except Exception as e: 
        print(f"Unexpected error validating forurensning data: {e}")
        return None
    
    #validating location
    #Long og Lat forurensning
    latitude_vær = vær_data_basemodel.geometry.coordinates.lat
    longitude_vær = vær_data_basemodel.geometry.coordinates.lon
    # Long og Lat forurensning
    latitude_forurensning = forurensnings_data_basemodel.meta.location.latitude
    longitude_forurensning = forurensnings_data_basemodel.meta.location.longitude
    #Definerer differens
    lat_diff = abs(latitude_vær - latitude_forurensning)
    lon_diff = abs(longitude_vær - longitude_forurensning)
    if lat_diff > 0.05 or lon_diff > 0.05:
        raise ValueError(f"Koordinasjoner er ikke de samme! Vær vs Forurensnings long{longitude_vær} vs{longitude_forurensning},Vær vs Forurensnings lat {latitude_vær}{latitude_forurensning}")
    print("Koordinasjoner samsvarer!")
   


    return vær_data, vær_data_basemodel, forurensnings_data, forurensnings_data_basemodel