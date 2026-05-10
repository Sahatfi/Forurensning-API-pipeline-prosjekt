from pathlib import Path
import yaml
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
import json
import logging


logger = logging.getLogger(__name__)
#Justering config
def load_config():
    logger.info("Laster konfigurasjon...")
    config_path = Path(__file__).resolve().parent.parent/ "config"/"config.yaml"
    try:
        with open(config_path, "r") as f:
            logger.info("Konfigurasjon lastet!")
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error(f"Kunne ikke finne konfigurasjonsfil i {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Ugyldig YAML i konfigurasjonsfil: {e}")
        raise

#Justering av param via config
def param_config_forecast(config):
    url = config["api1"]["url"]
    params = config["api1"]["params"]
    headers = config["api1"]["headers"]
    return url, headers,params

# Vær data loading
@retry(stop=stop_after_attempt(5),wait=wait_exponential(multiplier=1, min=4, max=10),reraise=True)
def load_data(url, headers, params):
    logger.info("Henter Værdata fra MET.no...")
    try:
        response = requests.get(url=url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        logger.info("Værdata var hentet!")
        return response.json()
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
        logger.error("Værdata API forespørsel tidsavbrudd")
        raise
    except requests.exceptions.HTTPError as e: 
        logger.error(f"Værdata API HTTP feil: {e}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Værdata API forespørsel feilet: {e}")
        raise
    except json.JSONDecodeError: 
        logger.error("Værdata API returnerte ugyldig JSON")
        raise

# Justering config videre for data air quality
def param_config_forurensning(config):
    url = config["api2"]["url"]
    params = config["api2"]["params"]
    headers = config["api2"]["headers"]
    return url, params, headers

# Forurensning loader  
@retry(stop=stop_after_attempt(5),wait=wait_exponential(multiplier=1, min=4, max=10),reraise=True)
def forurensning_loading(url, headers, params):
    logger.info("Henter forurensningsdata fra MET.no")
    try:
        response_forurensning = requests.get(url=url, headers = headers, params=params)
        response_forurensning.raise_for_status()
        logger.info("Forurensningsdata var hentet")
        return response_forurensning.json()
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
        logger.error("Forurensningsdata API forespørsel tidsavbrudd")
        raise
    except requests.exceptions.HTTPError as e: 
        logger.error(f"Forurensningsdata API HTTP feil: {e}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Forurensningsdata API forespørsel feilet: {e}")
        raise
    except json.JSONDecodeError: 
        logger.error("Forurensningsdata API returnerte ugyldig JSON")
        raise



