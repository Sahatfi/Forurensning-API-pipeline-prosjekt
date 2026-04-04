from pathlib import Path
import yaml
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
import json

#Justering config
def load_config():
    config_path = Path(__file__).resolve().parent.parent/ "config"/"config.yaml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

#Justering av param via config
def param_config_forecast(config):
    url = config["api1"]["url"]
    params = config["api1"]["params"]
    headers = config["api1"]["headers"]
    return url, headers,params

# data loading
@retry(stop=stop_after_attempt(5),wait=wait_exponential(multiplier=1, min=4, max=10),reraise=True)
def load_data(url, headers, params):
    response = requests.get(url=url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

# Justering config videre for data air quality
def param_config_forurensning(config):
    url = config["api2"]["url"]
    params = config["api2"]["params"]
    headers = config["api2"]["headers"]
    return url , params, headers


@retry(stop=stop_after_attempt(5),wait=wait_exponential(multiplier=1, min=4, max=10),reraise=True)
# Forurensning loader  
def forurensning_loading(url, headers, params):
    response_forurensning = requests.get(url=url, headers = headers, params=params)
    response_forurensning.raise_for_status()
    return response_forurensning.json()
   





