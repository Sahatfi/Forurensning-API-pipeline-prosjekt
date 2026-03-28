from pathlib import Path
import yaml
import requests
def load_config():
    config_path = Path(__file__).resolve().parent.parent/ "config"/"config.yaml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
    
def data_load(config):
    url = config["api"]["url"]
    params = config["api"]["params"]
    headers = config["api"]["headers"]
    try:
        response = requests.get(url = url, headers  = headers, params = params)
        data = response.json()
        print("Ingested successfully- status code below:\n", response.status_code)
    except requests.exceptions.RequestException as e:
            print("ingestion failed! Explaination below:\n" , e)
    return data



