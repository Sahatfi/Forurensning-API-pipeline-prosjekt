
import pytest
from src.data_loader import load_config, param_config_forecast, load_data
from unittest.mock import MagicMock
import responses
import requests
from requests.exceptions import HTTPError
from unittest.mock import patch, Mock

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


# data loading

@responses.activate
def test_load_data_failure():
    url = "http://test.com"
    responses.add("GET", url, status=500)
    with pytest.raises(requests.exceptions.HTTPError):
        load_data(url, {}, {})

@responses.activate
def test_load_data_success():
    url = "http://test.com"
    responses.add( "GET", url, json={"ok": True}, status=200)
    result = load_data(url, {}, {})
    assert result == {"ok": True}
    
# python -m pytest tests/test_data_loader.py