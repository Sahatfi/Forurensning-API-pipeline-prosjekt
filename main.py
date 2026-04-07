from src.data_loader import load_config, param_config_forecast, load_data, param_config_forurensning, forurensning_loading
from src.modeling import Data, ForurensningsModel
import json
import requests

#Adjusting configuration
config = load_config()

#Adjusting for parameters for data loading
url, headers, params  = param_config_forecast(config)

#Try to load data:
try:
    print("Starter henting av data...")
    data = load_data(url, headers, params)
    print("Data hentet suksessfullt!")
    #print(data)
except requests.exceptions.RequestException as e:
    print("Kunne ikke hente data etter 5 forsøk. Feilmelding:", e)

# Anta at 'data' er JSON fra API
data_obj = Data(**data)  # Konverter til BaseModel

# Loop gjennom timeseries med indeks
for idx, ts in enumerate(data_obj.properties.timeseries):
    print(idx, ts.time)

#__________________________

#Forirensning test
url_foruransning, params_forurensning, headers_forurensning = param_config_forurensning(config)
print(url_foruransning, params_forurensning, headers_forurensning)
fx = forurensning_loading(url_foruransning, headers_forurensning, params_forurensning)
print(fx)
ax = ForurensningsModel(**fx)
e = fx["data"]["time"][6]["from"]
g = ax.data.time[6].from_
print(e)
print(g)
print("Is it true that code is correct? This statement is ", e == g)