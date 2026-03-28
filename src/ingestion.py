import requests
from data_loader import load_config
config = load_config()
url = config["api"]["url"]
params = config["api"]["params"]

headers = config["api"]["headers"]
try:
    response = requests.get(url, headers  = headers, params = params)
    data = response.json()
    print("Ingested successfully- status code below:\n", response.status_code)
except requests.exceptions.RequestException as e:
    print("ingestion failed! Explaination below:\n" , e)
