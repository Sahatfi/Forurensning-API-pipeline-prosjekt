import sys
import os
import pandas as pd

sys.path.insert(0, os.getcwd())
from pipelines.run_pipeline import run_pipeline

vær_json, vær_valid, forurensning_json, forurensning_valid = run_pipeline()
print(vær_json.keys())
print(vær_json.keys())
print(forurensning_valid.data.time[1].from_)
#Trekke ut  navn på lokasjon latitude og longitude fra forurensning
latitude_forurensning = forurensning_valid.meta.location.latitude
longitude_forurensning = forurensning_valid.meta.location.longitude
navn_forurensning = forurensning_valid.meta.location.path
#date
date_forurensning = forurensning_valid.data.time[1].from_
#Trekke ut latitude og longitude fra vær data
latitude_vær = vær_valid.geometry.coordinates.lat
longitude_vær = vær_valid.geometry.coordinates.lon
print(latitude_forurensning, latitude_vær, longitude_forurensning, longitude_vær)
#Forurensning dataframe
#pd.DataFrame({
        #'timestamp': [datetime.now()],
       # 'latitude': [air_model.meta.location.latitude],
       #'timestamp': [pd.to_datetime(air_model.data.time[1].from_)]

forurensning_df = pd.DataFrame({'timestamp' : [forurensning_valid.data.time[1].from_],
                                'latitude_for': [forurensning_valid.meta.location.latitude],
                                 'longitude_for': [forurensning_valid.meta.location.longitude],
                                  'stednavn' : forurensning_valid.meta.location.path,})
print(forurensning_df.dtypes)
