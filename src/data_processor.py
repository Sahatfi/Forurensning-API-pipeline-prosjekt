import pandas as pd
from src.modeling import ForurensningsModel, Data
import logging


logger = logging.getLogger(__name__)


def process_weather_data(vær_valid: Data, hours_ahead: int = 10):

    logger.info(f"Prossesserer værdata- Værvarsel + {hours_ahead}h)...")
    
    # Bounds check
    timeseries_length = len(vær_valid.properties.timeseries)
    if hours_ahead >= timeseries_length:
        logger.error(f"Ba om {hours_ahead}t prognose, men har bare {timeseries_length}t tilgjengelig")
        raise ValueError(f"Trenger {hours_ahead}t prognose, men har bare {timeseries_length}t")
    # Definerer vei til variablene jeg trenger
    forecast = vær_valid.properties.timeseries[hours_ahead]
    # definerer (timestamp, location)
    result = {
        'timestamp_vær': forecast.time,
        'latitude_vær': vær_valid.geometry.coordinates.lat,
        'longitude_vær': vær_valid.geometry.coordinates.lon,
        }
    
    # Navnliste til variabler
    weather_fields = [
        'air_pressure_at_sea_level',
        'air_temperature',
        'cloud_area_fraction',
        'relative_humidity',
        'wind_from_direction',
        'wind_speed'
    ]
    
    # Loop gjennom hver variable for å få verdi
    for field_name in weather_fields:
        field_value = getattr(forecast.data.instant.details, field_name)
        
        # Lag resultat i result, altså dictionary som skal konverteres tl df
        result[field_name] = field_value
    #To df
    vær_df = pd.DataFrame([result])
    logger.info(f"Fikk tak i {len(vær_df)} vær data")

    return vær_df

#Forurensning dataframe

def process_airquality_data(forurensning_valid: ForurensningsModel, hours_ahead : int = 6):
    timeseries_length = len(forurensning_valid.data.time)
    if hours_ahead >= timeseries_length:
        logger.error(f"Ba om {hours_ahead}t prognose, men har bare {timeseries_length}t tilgjengelig")
        raise ValueError(f"Trenger {hours_ahead}t prognose, men har bare {timeseries_length}t")
    
    
    logger.info(f"Processerer forurensnings data (forecast +{hours_ahead}h)...")
    result = {
    'timestamp_for': forurensning_valid.data.time[hours_ahead].from_,
    'latitude_for': forurensning_valid.meta.location.latitude,
    'longitude_for': forurensning_valid.meta.location.longitude,
    'stednavn' : forurensning_valid.meta.location.path,
    'AQI': forurensning_valid.data.time[hours_ahead].variables.AQI.value}
    pollutants = ['no2', 'pm10', 'pm25', 'o3']
    suffix =['_concentration',
             '_nonlocal_fraction',
             '_nonlocal_fraction_seasalt',
             '_local_fraction_traffic_exhaust',
             '_local_fraction_traffic_nonexhaust',
             '_local_fraction_shipping',
             '_local_fraction_heating',
             '_local_fraction_industry']
    # Ekstraksjon av AQI
    pathname = forurensning_valid.data.time[hours_ahead].variables
    for pollutant in pollutants:
        aqi = f"AQI_{pollutant}"
        field_value = getattr(pathname, aqi).value
        result[aqi] = field_value
    # Ekstraksjon av forurensende stoffer
        for one_suffix in suffix:
            pollutant_suffix = f"{pollutant}{one_suffix}"
            suffix_value = getattr(pathname,pollutant_suffix).value
            result[pollutant_suffix] = suffix_value
    #To df
    forurensning_df = pd.DataFrame([result])
    logger.info(f" Ekstraherte {len(forurensning_df)} forurensningsdata rad(er)")
    return forurensning_df

def merge_forecasts(vær_df ,forurensning_df):
    df_merged = pd.merge(vær_df, forurensning_df, left_on = ['latitude_vær', 'longitude_vær'], right_on = ['latitude_for', 'longitude_for'],   how = 'left')
    logger.info("Dataset slått sammen")
    return df_merged
