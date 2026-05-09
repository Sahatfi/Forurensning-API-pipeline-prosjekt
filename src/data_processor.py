
import pandas as pd
from src.modeling import ForurensningsModel, Data
import logging


logger = logging.getLogger(__name__)


def process_weather_data(vær_valid: Data, hours_ahead: int = 10):

    logger.info(f"Processing weather data (forecast +{hours_ahead}h)...")
    
    # Bounds check
    timeseries_length = len(vær_valid.properties.timeseries)
    if hours_ahead >= timeseries_length:
        logger.error(f"Requested {hours_ahead}h forecast, only have {timeseries_length}h available")
        raise ValueError(f"Need {hours_ahead}h forecast, only have {timeseries_length}h")
    
    # Get the forecast item ONCE (instead of repeating this long path)
    forecast = vær_valid.properties.timeseries[hours_ahead]
    
    # Start with base fields (timestamp, location)
    result = {
        'timestamp_vær': forecast.time,
        'latitude_vær': vær_valid.geometry.coordinates.lat,
        'longitude_vær': vær_valid.geometry.coordinates.lon,
    }
    
    # List of weather field names (the ones that repeat)
    weather_fields = [
        'air_pressure_at_sea_level',
        'air_temperature',
        'cloud_area_fraction',
        'relative_humidity',
        'wind_from_direction',
        'wind_speed'
    ]
    
    # Loop through each field
    for field_name in weather_fields:
        # Get the value using getattr
        # This is the same as: forecast.data.instant.details.air_temperature
        field_value = getattr(forecast.data.instant.details, field_name)
        
        # Store it in result
        result[field_name] = field_value
    
    # Convert to DataFrame
    vær_df = pd.DataFrame([result])
    
    logger.info(f"✅ Extracted {len(vær_df)} weather record(s)")
    return vær_df

#Forurensning dataframe



def process_airquality_data(forurensning_valid: ForurensningsModel, hours_ahead : int = 10):
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

    forurensning_df = pd.DataFrame([result])

    return(forurensning_df)

def merge_forecasts(vær_df ,forurensning_df):
    df_merged = pd.merge(vær_df, forurensning_df, left_on = ['latitude_vær', 'longitude_vær'], right_on = ['latitude_for', 'longitude_for'],   how = 'left')
    return df_merged
