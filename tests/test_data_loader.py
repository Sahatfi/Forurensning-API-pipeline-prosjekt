
import pytest
from src.data_loader import load_config, param_config_forecast

#Test av config path
def test_load_config_returns_dict():
    config = load_config()
    assert isinstance(config, dict)

#test av config struktur
def test_param_config_forecast_returns_correct_values():
#lagring av mock-config for api1
    mock_config = {"api1":
    {"url" : "https://eksempel.no/api", "headers" : {"User-Agent" :"www.mockurl. com" },
    "params" : {"lon": 10, "lat" : 5}, 
    "headers" : {"User-Agent" : "email.email.com"}}}
  #Testing
    url, headers, params = param_config_forecast(mock_config)
    assert url == "https://eksempel.no/api"
    assert headers == {"User-Agent" : "email.email.com"}
    assert params == {"lat" : 5, "lon": 10}


