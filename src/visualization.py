from pathlib import Path
import yaml
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
import json
 https://api.met.no/weatherapi/airqualityforecast/0.1/
#data loading
