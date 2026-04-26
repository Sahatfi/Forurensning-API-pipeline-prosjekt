
import pandas as pd

def process_weather_data(vær_valid):
    vær_df = pd.DataFrame({'timestamp_vær' : [vær_valid.properties.timeseries[10].time],
                       'latitude_vær' :[vær_valid.geometry.coordinates.lat],
                       'longitude_vær': [vær_valid.geometry.coordinates.lon],
                       'air_pressure_at_sea_level': [vær_valid.properties.timeseries[10].data.instant.details.air_pressure_at_sea_level],
                       'air_temperature': [vær_valid.properties.timeseries[10].data.instant.details.air_temperature],
                       'cloud_area_fraction':  [vær_valid.properties.timeseries[10].data.instant.details.cloud_area_fraction],
                       'relative_humidity' : [vær_valid.properties.timeseries[10].data.instant.details.relative_humidity],
                       'wind_from_direction': [vær_valid.properties.timeseries[10].data.instant.details.wind_from_direction],
                       'wind_speed': [vær_valid.properties.timeseries[10].data.instant.details.wind_speed]})
    return(vær_df)
#Forurensning dataframe

def process_airquality_data(forurensning_valid)
    forurensning_df = pd.DataFrame({'timestamp_for' : [forurensning_valid.data.time[10].from_],
                                'latitude_for': [forurensning_valid.meta.location.latitude],
                                'longitude_for': [forurensning_valid.meta.location.longitude],
                                'stednavn' : [forurensning_valid.meta.location.path],
                                #No2

                                'no2_concentration': [forurensning_valid.data.time[10].variables.no2_concentration.value],
                                'AQI': [forurensning_valid.data.time[10].variables.AQI.value],
                                'AQI_no2': [forurensning_valid.data.time[10].variables.AQI_no2.value],
                                'no2_nonlocal_fraction': [forurensning_valid.data.time[10].variables.no2_nonlocal_fraction.value],
                                'no2_nonlocal_fraction_seasalt': [forurensning_valid.data.time[10].variables.no2_nonlocal_fraction_seasalt.value],
                                'no2_local_fraction_traffic_exhaust': [forurensning_valid.data.time[10].variables.no2_local_fraction_traffic_exhaust.value],
                                'no2_local_fraction_traffic_nonexhaust': [forurensning_valid.data.time[10].variables.no2_local_fraction_traffic_nonexhaust.value],
                                'no2_local_fraction_shipping': [forurensning_valid.data.time[10].variables.no2_local_fraction_shipping.value],
                                'no2_local_fraction_heating': [forurensning_valid.data.time[10].variables.no2_local_fraction_heating.value],
                                'no2_local_fraction_industry': [forurensning_valid.data.time[10].variables.no2_local_fraction_industry.value],

                                #pm10
                                'pm10_concentration': [forurensning_valid.data.time[10].variables.pm10_concentration.value],
                                'AQI_pm10': [forurensning_valid.data.time[10].variables.AQI_pm10.value],
                                'pm10_nonlocal_fraction': [forurensning_valid.data.time[10].variables.pm10_nonlocal_fraction.value],
                                'pm10_nonlocal_fraction_seasalt': [forurensning_valid.data.time[10].variables.pm10_nonlocal_fraction_seasalt.value],
                                'pm10_local_fraction_traffic_exhaust': [forurensning_valid.data.time[10].variables.pm10_local_fraction_traffic_exhaust.value],
                                'pm10_local_fraction_traffic_nonexhaust': [forurensning_valid.data.time[10].variables.pm10_local_fraction_traffic_nonexhaust.value],
                                'pm10_local_fraction_shipping': [forurensning_valid.data.time[10].variables.pm10_local_fraction_shipping.value],
                                'pm10_local_fraction_heating': [forurensning_valid.data.time[10].variables.pm10_local_fraction_heating.value],
                                'pm10_local_fraction_industry': [forurensning_valid.data.time[10].variables.pm10_local_fraction_industry.value],
                                #pm25
                                'pm25_concentration': [forurensning_valid.data.time[10].variables.pm25_concentration.value],
                                'AQI_pm25': [forurensning_valid.data.time[10].variables.AQI_pm25.value],
                                'pm25_nonlocal_fraction': [forurensning_valid.data.time[10].variables.pm25_nonlocal_fraction.value],
                                'pm25_nonlocal_fraction_seasalt': [forurensning_valid.data.time[10].variables.pm25_nonlocal_fraction_seasalt.value],
                                'pm25_local_fraction_traffic_exhaust': [forurensning_valid.data.time[10].variables.pm25_local_fraction_traffic_exhaust.value],
                                'pm25_local_fraction_traffic_nonexhaust': [forurensning_valid.data.time[10].variables.pm25_local_fraction_traffic_nonexhaust.value],
                                'pm25_local_fraction_shipping': [forurensning_valid.data.time[10].variables.pm25_local_fraction_shipping.value],
                                'pm25_local_fraction_heating': [forurensning_valid.data.time[10].variables.pm25_local_fraction_heating.value],
                                'pm25_local_fraction_industry': [forurensning_valid.data.time[10].variables.pm25_local_fraction_industry.value],
                                #o3
     
                                'o3_concentration': [forurensning_valid.data.time[10].variables.o3_concentration.value],
                                'AQI_o3': [forurensning_valid.data.time[10].variables.AQI_o3.value],
                                'o3_nonlocal_fraction': [forurensning_valid.data.time[10].variables.o3_nonlocal_fraction.value],
                                'o3_nonlocal_fraction_seasalt': [forurensning_valid.data.time[10].variables.o3_nonlocal_fraction_seasalt.value],
                                'o3_local_fraction_traffic_exhaust': [forurensning_valid.data.time[10].variables.o3_local_fraction_traffic_exhaust.value],
                                'o3_local_fraction_traffic_nonexhaust': [forurensning_valid.data.time[10].variables.o3_local_fraction_traffic_nonexhaust.value],
                                'o3_local_fraction_shipping': [forurensning_valid.data.time[10].variables.o3_local_fraction_shipping.value],
                                'o3_local_fraction_heating': [forurensning_valid.data.time[10].variables.o3_local_fraction_heating.value],
                                'o3_local_fraction_industry': [forurensning_valid.data.time[10].variables.o3_local_fraction_industry.value]
 })
    return(forurensning_df)

def merge_forecasts(vær_df ,forurensning_df)
    df_merged = pd.merge(vær_df, forurensning_df, left_on = ['latitude_vær', 'longitude_vær'], right_on = ['latitude_for', 'longitude_for'],   how = 'left')

    return df_merged
