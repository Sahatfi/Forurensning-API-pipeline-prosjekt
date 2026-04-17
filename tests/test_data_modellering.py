

from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List, Dict, Any
import pytest
from src.modeling import Data

import pytest

# ---- TEST 1: Gyldig input ----
def test_data_model_valid_input():
    mock_json = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [10.0, 60.0, 5.0]
        },
        "properties": {
            "meta": {
                "updated_at": "2026-01-01",
                "units": {
                    "air_temperature": "celsius"
                }
            },
            "timeseries": [
                {
                    "time": "2026-01-01T10:00:00Z",
                    "data": {
                        "instant": {
                            "details": {
                                "air_temperature": 5.0,
                                "wind_speed": 3.2,
                                "relative_humidity": 80.0,
                                "wind_from_direction": 180.0
                            }
                        },
                        "next_12_hours": {
                            "summary": {
                                "symbol_code": "clearsky"
                            }
                        }
                    }
                }
            ]
        }
    }

    model = Data.model_validate(mock_json)

    assert model.type == "Feature"
    assert model.geometry.coordinates.lon == 10.0
    assert model.geometry.coordinates.lat == 60.0
    assert model.geometry.coordinates.alt == 5.0

    assert model.properties.meta.updated_at == "2026-01-01"
    assert model.properties.meta.units.air_temperature == "celsius"

    assert model.properties.timeseries[0].time == "2026-01-01T10:00:00Z"

    details = model.properties.timeseries[0].data.instant.details
    assert details.air_temperature == 5.0
    assert details.wind_speed == 3.2
    assert details.relative_humidity == 80.0
    assert details.wind_from_direction == 180.0


# ---- TEST 2: Validator (liste -> objekt) ----
def test_geometry_validator_list_to_object():
    model = Data.model_validate({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [10.0, 60.0, 5.0]
        },
        "properties": {
            "meta": {
                "updated_at": "2026-01-01",
                "units": {}
            },
            "timeseries": []
        }
    })

    assert model.geometry.coordinates.lon == 10.0
    assert model.geometry.coordinates.lat == 60.0
    assert model.geometry.coordinates.alt == 5.0


# ---- TEST 3: Manglende felt skal feile ----
def test_missing_fields_not_allowed():
    with pytest.raises(Exception):
        Data.model_validate({
            "type": "Feature",
            "geometry": None,
            "properties": None
        })


# ---- TEST 4: Feil datatype på coordinates ----
def test_invalid_coordinates_type():
    with pytest.raises(Exception):
        Data.model_validate({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": "not-a-list"
            },
            "properties": {
                "meta": {
                    "updated_at": "2026-01-01",
                    "units": {}
                },
                "timeseries": []
            }
        })


# ---- TEST 5: Mangler required fields i Details ----
def test_missing_required_details_fields():
    with pytest.raises(Exception):
        Data.model_validate({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [10.0, 60.0, 5.0]
            },
            "properties": {
                "meta": {
                    "updated_at": "2026-01-01",
                    "units": {}
                },
                "timeseries": [
                    {
                        "time": "2026-01-01T10:00:00Z",
                        "data": {
                            "instant": {
                                "details": {
                                    # mangler required fields
                                    "air_temperature": 5.0
                                }
                            }
                        }
                    }
                ]
            }
        })


# ---- TEST 6: instant kan ikke være None ----
def test_instant_cannot_be_none():
    with pytest.raises(Exception):
        Data.model_validate({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [10.0, 60.0, 5.0]
            },
            "properties": {
                "meta": {
                    "updated_at": "2026-01-01",
                    "units": {}
                },
                "timeseries": [
                    {
                        "time": "2026-01-01T10:00:00Z",
                        "data": {
                            "instant": None
                        }
                    }
                ]
            }
        })

#.  python -m pytest /tests/test_data_modellering.py