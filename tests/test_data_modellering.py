# test_insert.py
from src.modeling import Data, ForurensningsModel
import pandas as pd
from datetime import datetime
from src.storage import get_db_path
import sqlite3


#.  
def test_happy_path_forurensning():
    mock_json = forurensningsdataset = {'meta': {'reftime': '2026-05-20T06:00:00Z', 
                                    'location': {'name': 'Rådhuskretsen', 'path': 'Troms - Romsa - Tromssa/Tromsø/Tromsø/Rådhuskretsen', 'areacode': '55010114', 'longitude': '18.95560', 'latitude': '69.65100', 'areaclass': 'grunnkrets', 'superareacode': '55010100'}, 
                                    'superlocation': {'name': 'Tromsø', 'path': 'Troms - Romsa - Tromssa/Tromsø/Tromsø', 'areacode': '55010100', 'longitude': '18.95656', 'latitude': '69.64913', 'areaclass': 'delomrade', 'superareacode': '5501'},
                                      'sublocations': []}, 
                                      'data': {'time': [{'from': '2026-05-20T12:00:00Z', 'to': '2026-05-20T12:00:00Z', 
                                                         'variables': {'AQI': {'value': 1.8, 'units': '1'}}}]}}
    validated = ForurensningsModel(**mock_json)
    assert validated.data.time[0].variables.AQI.value == 1.8

#python -m pytest tests/test_data_loader.py -v
#python -m pytest tests/test_data_modellering.py -v
