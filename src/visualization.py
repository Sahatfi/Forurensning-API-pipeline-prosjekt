from pathlib import Path
import yaml
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
import json
 https://api.met.no/weatherapi/airqualityforecast/0.1/
#data loading



 AQI
    no2_concentration
    AQI_no2
    no2_nonlocal_fraction
    no2_nonlocal_fraction_seasalt
    no2_local_fraction_traffic_exhaust
    no2_local_fraction_traffic_nonexhaust
    no2_local_fraction_shipping
    no2_local_fraction_heating
    no2_local_fraction_industry
    pm10_concentration
    AQI_pm10
    pm10_nonlocal_fraction
    pm10_nonlocal_fraction_seasalt
    pm10_local_fraction_traffic_exhaust
    pm10_local_fraction_traffic_nonexhaust
    pm10_local_fraction_shipping
    pm10_local_fraction_heating
    pm10_local_fraction_industry
    pm25_concentration
    AQI_pm25
    pm25_nonlocal_fraction
    pm25_nonlocal_fraction_seasalt
    pm25_local_fraction_traffic_exhaust
    pm25_local_fraction_traffic_nonexhaust
    pm25_local_fraction_shipping
    pm25_local_fraction_heating
    pm25_local_fraction_industry
    o3_concentration
    AQI_o3
    o3_nonlocal_fraction
    vo3_nonlocal_fraction_seasalt
    o3_local_fraction_traffic_exhaust
    o3_local_fraction_traffic_nonexhaust
    o3_local_fraction_shipping
    o3_local_fraction_heating
    o3_local_fraction_industry
