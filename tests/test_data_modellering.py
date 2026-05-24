# test_insert.py
from src.modeling import Data, ForurensningsModel, Coordinates
import pandas as pd
from datetime import datetime
from src.storage import get_db_path
import sqlite3
import pytest
from pydantic import ValidationError



def test_happy_path_vær():
    mock_json = {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [18.9556, 69.651, 9]},
              'properties': {'meta': {'updated_at': '2026-05-20T14:28:00Z', 
                                      'units': {'air_pressure_at_sea_level': 'hPa', 'air_temperature': 'celsius', 'cloud_area_fraction': '%', 'precipitation_amount': 'mm', 'relative_humidity': '%', 'wind_from_direction': 'degrees', 'wind_speed': 'm/s'}},
                                        'timeseries': [{'time': '2026-05-20T15:00:00Z', 
                                                        'data': 
                                                        {'instant': 
                                                         {'details': 
                                                          { 'air_temperature': 2,'relative_humidity' : 3.2, 'air_pressure_at_sea_level': 1015.5, 'wind_speed' : 2.2, 'wind_from_direction': 225.0}}}}]}}
    validated = Data(**mock_json)
    assert validated is not None
    assert validated.properties.timeseries[0].data.instant.details.air_pressure_at_sea_level == 1015.5
    assert validated.properties.timeseries[0].data.instant.details.air_temperature == 2
    assert validated.properties.timeseries[0].data.instant.details.relative_humidity == 3.2
    assert validated.properties.timeseries[0].data.instant.details.wind_speed == 2.2
    assert validated.properties.timeseries[0].data.instant.details.wind_from_direction == 225.0

def test_location_list_vær():
    mock_json = {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [18.9556, 69.651, 9]}, 
                 'properties': {'meta': {'updated_at': '2026-05-20T14:28:00Z', ''
                 'units': {'air_pressure_at_sea_level': 'hPa', 
                           'air_temperature': 'celsius', 'cloud_area_fraction': '%', 
                           'precipitation_amount': 'mm', 'relative_humidity': '%', 
                           'wind_from_direction': 'degrees', 
                           'wind_speed': 'm/s'}}, 
                           'timeseries': [{'time': '2026-05-20T15:00:00Z', 
                                           'data': {'instant': {'details': {'air_pressure_at_sea_level': 1015.5, 
                                                                            'air_temperature': 11.3, 
                                                                            'cloud_area_fraction': 100.0, 
                                                                            'relative_humidity': 74.9, 
                                                                            'wind_from_direction': 225.0, 
                                                                            'wind_speed': 2.1}}, 
                                                                            'next_12_hours': {'summary': {'symbol_code': 'lightrain'}, 'details': {}}, 
                                                                            'next_1_hours': {'summary': {'symbol_code': 'cloudy'}, 
                                                                                             'details': {'precipitation_amount': 0.0}}, 
                                                                                             'next_6_hours': {'summary': {'symbol_code': 'cloudy'}, 
                                                                                                              'details': {'precipitation_amount': 0.0}}}}]}}
    validated = Data(**mock_json)
    assert isinstance(validated.geometry.coordinates, Coordinates)
    assert validated.geometry.coordinates.lon == 18.9556
    assert validated.geometry.coordinates.lat == 69.651
    assert validated.geometry.coordinates.alt == 9

def test_location_ist_vær():
    invalid_data = {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': ['mockedcoordinates']}, 
                 'properties': {'meta': {'updated_at': '2026-05-20T14:28:00Z', ''
                 'units': {'air_pressure_at_sea_level': 'hPa', 
                           'air_temperature': 'celsius', 'cloud_area_fraction': '%', 
                           'precipitation_amount': 'mm', 'relative_humidity': '%', 
                           'wind_from_direction': 'degrees'}}}}
    invalid_data2 = {'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [3, 8, 5]}, 
                 'properties': {'meta': {'updated_at': '2026-05-20T14:28:00Z', ''
                 'units': {'air_pressure_at_sea_level': 'hPa', 
                           'air_temperature': 'celsius', 'cloud_area_fraction': '%', 
                           'precipitation_amount': 'mm', 'relative_humidity': '%', 
                           'wind_from_direction': 'degrees'}}}}
    with pytest.raises(IndexError):
        Data(**invalid_data)
        
    with pytest.raises(ValidationError):
        Data(**invalid_data2)


#Forurensningstester:
def test_happy_path_forurensning():
    mock_json = {'meta': {'reftime': '2026-05-20T06:00:00Z', 
                'location': {'name': 'Rådhuskretsen', 'path': 'Troms - Romsa - Tromssa/Tromsø/Tromsø/Rådhuskretsen', 'areacode': '55010114', 'longitude': '18.95560', 'latitude': '69.65100', 'areaclass': 'grunnkrets', 'superareacode': '55010100'}, 
                'superlocation': {'name': 'Tromsø', 'path': 'Troms - Romsa - Tromssa/Tromsø/Tromsø', 'areacode': '55010100', 'longitude': '18.95656', 'latitude': '69.64913', 'areaclass': 'delomrade', 'superareacode': '5501'},
                'sublocations': []}, 
                'data': {'time': [{'from': '2026-05-20T12:00:00Z', 'to': '2026-05-20T12:00:00Z', 
                'variables': {'AQI': {'value': 1.8, 'units': '1'}}}]}}
    validated = ForurensningsModel(**mock_json)
    assert validated.data.time[0].variables.AQI.value == 1.8

def test_from_forurensning():
    mock_json = {'meta': {'reftime': '2026-05-20T06:00:00Z', 
                 'location': {'name': 'Rådhuskretsen', 'path': 'Troms - Romsa - Tromssa/Tromsø/Tromsø/Rådhuskretsen', 'areacode': '55010114', 'longitude': '18.95560', 'latitude': '69.65100', 'areaclass': 'grunnkrets', 'superareacode': '55010100'}, 
                 'superlocation': {'name': 'Tromsø', 'path': 'Troms - Romsa - Tromssa/Tromsø/Tromsø', 'areacode': '55010100', 'longitude': '18.95656', 'latitude': '69.64913', 'areaclass': 'delomrade', 'superareacode': '5501'},
                 'sublocations': []}, 
                 'data': {'time': [{'from': '2026-05-20T12:00:00Z', 'to': '2026-05-20T12:00:00Z', 
                 'variables': {'AQI': {'value': 1.8, 'units': '1'}}}]}}
    validated = ForurensningsModel(**mock_json)
    assert validated.data.time[0].from_ is not None
    assert isinstance(validated.data.time[0].from_, datetime)


def test_invalid_json():
    invalid_data = {'meta': {'location': {'latitude': '25'}},'data': {'time': []}}
    with pytest.raises(ValidationError):
        ForurensningsModel(**invalid_data)


# python -m pytest tests/test_data_modellering.py -v
