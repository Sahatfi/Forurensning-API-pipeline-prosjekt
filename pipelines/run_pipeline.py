from src.data_loader import load_config, param_config_forecast, load_data, param_config_forurensning, forurensning_loading
from src.modeling import Data, ForurensningsModel
import json
import requests

def run_pipeline():
    #Adjusting configuration
    config = load_config()
    #Adjusting for parameters for data loading
    url, headers, params  = param_config_forecast(config)

    #Try to load data:
    try:
        print("Starter henting av data...")
        vær_data = load_data(url, headers, params)
        print("Data hentet suksessfullt!")
    except requests.exceptions.RequestException as e:
        print("Kunne ikke hente data etter 5 forsøk. Feilmelding:", e)

    # Konverter til BaseModel
    try :
        vær_data_basemodel = Data(**vær_data)  
    except: print("failed")

    #Adjusting for parameters for data loading for forurensning
    url_foruransning, params_forurensning, headers_forurensning = param_config_forurensning(config)
    forurensnings_data = forurensning_loading(url_foruransning, headers_forurensning, params_forurensning)
    print(forurensnings_data)
    try:
        forurensnings_data_basemodel = ForurensningsModel(**forurensnings_data)
    except:
        print("Det var noe feil")
    return  vær_data, vær_data_basemodel, forurensnings_data, forurensnings_data_basemodel,