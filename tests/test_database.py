
import pytest
from src.data_loader import load_config, param_config_forecast, load_data
from unittest.mock import MagicMock
import responses
import requests
from requests.exceptions import HTTPError
from unittest.mock import patch, Mock

from src.storage import get_db_path

db_path = get_db_path()
print(f"Database will be at: {db_path}")
