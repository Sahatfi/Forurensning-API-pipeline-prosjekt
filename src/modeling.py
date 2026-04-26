from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class Details(BaseModel):
    # Data -> Properties -> Timeseries_Attributes -> Weatherdata -> Instant -> Details -> (data below)
    air_pressure_at_sea_level : float | None = None
    air_temperature : float 
    cloud_area_fraction : float | None = None
    relative_humidity : float 
    wind_from_direction : float 
    wind_speed : float 

class Instant(BaseModel):
    #Data -> Properties -> Timeseries_Attributes -> Weatherdata -> Instant -> (Details)
    details : Details

class Summary(BaseModel):
    #Data -> Properties -> Timeseries_Attributes -> Weatherdata -> next 12 hrs -> Summary -> (symbol code)
    symbol_code : str | None = None
class Next12Hrs(BaseModel):
    #Data -> Properties -> Timeseries_Attributes -> Weatherdata -> next 12 hrs -> (Summary)
    summary : Summary | None = None
class Weatherdata(BaseModel):
    #Data -> Properties -> Timeseries_Attributes -> Weatherdata ->(instant + next 12 hrs)
    instant : Instant 
    next_12_hours : Next12Hrs | None = None

class Timeseries_Attributes(BaseModel):
    #Data -> Properties -> Timeseries_Attributes-> (time + data)
    time: datetime                                      
    data: Weatherdata | None = None

class Units(BaseModel):
    #Data -> Properties -> Units -> (units below)
    air_pressure_at_sea_level: str | None = None
    air_temperature: str | None = None
    precipitation_amount: str | None = None
    relative_humidity: str | None = None
    wind_from_direction: str | None = None
    wind_speed: str | None = None

class Meta(BaseModel):
    #Data -> Properties -> Meta (updated_at + units)
    updated_at: str               #VIKTIG    
    units: Units                  #VIKTIG 

class Properties(BaseModel):
    #Data -> Properties -> (meta + timeseries)
    meta: Meta 
    timeseries: list[Timeseries_Attributes]

class Coordinates(BaseModel):
    #Geometry -> coordinates -> [lon, lat, alt]
    lon : float 
    lat : float 
    alt : float | None = None
    
class Geometry(BaseModel):
    #Geometry -> (type + coordinates)
    type: str | None = None
    coordinates : Coordinates 
    @field_validator("coordinates", mode="before")
    @classmethod
    def parse_list(cls, v):
        if isinstance(v, list):
            return {"lon": v[0],
                    "lat": v[1],
                    "alt": v[2],}
        return v
    
class Data(BaseModel):
    type : str 
    geometry : Geometry 
    properties : Properties 
#__________________________
class Measurement(BaseModel):
    value : float | None = None
    units : str | None = None

class ForurensningsVariables(BaseModel):
    # Dataset -> data -> time -> variables -> 
    #No2
    AQI : Measurement | None = None
    no2_concentration : Measurement | None = None
    AQI_no2 : Measurement | None = None
    no2_nonlocal_fraction : Measurement | None = None
    no2_nonlocal_fraction_seasalt : Measurement | None = None
    no2_local_fraction_traffic_exhaust : Measurement | None = None
    no2_local_fraction_traffic_nonexhaust : Measurement | None = None
    no2_local_fraction_shipping : Measurement | None = None
    no2_local_fraction_heating : Measurement | None = None
    no2_local_fraction_industry : Measurement | None = None
    #Pm10
    pm10_concentration : Measurement | None = None
    AQI_pm10 : Measurement | None = None
    pm10_nonlocal_fraction : Measurement | None = None
    pm10_nonlocal_fraction_seasalt : Measurement | None = None
    pm10_local_fraction_traffic_exhaust : Measurement | None = None
    pm10_local_fraction_traffic_nonexhaust : Measurement | None = None
    pm10_local_fraction_shipping : Measurement | None = None
    pm10_local_fraction_heating : Measurement | None = None
    pm10_local_fraction_industry : Measurement | None = None
    pm25_concentration : Measurement | None = None
    #Pm25
    AQI_pm25 : Measurement | None = None
    pm25_nonlocal_fraction : Measurement | None = None
    pm25_nonlocal_fraction_seasalt : Measurement | None = None
    pm25_local_fraction_traffic_exhaust : Measurement | None = None
    pm25_local_fraction_traffic_nonexhaust : Measurement | None = None
    pm25_local_fraction_shipping : Measurement | None = None
    pm25_local_fraction_heating : Measurement | None = None
    pm25_local_fraction_industry : Measurement | None = None
    o3_concentration : Measurement | None = None
    AQI_o3 : Measurement | None = None
    o3_nonlocal_fraction : Measurement | None = None
    o3_nonlocal_fraction_seasalt : Measurement  | None = None
    o3_local_fraction_traffic_exhaust : Measurement | None = None
    o3_local_fraction_traffic_nonexhaust : Measurement | None = None
    o3_local_fraction_shipping : Measurement | None = None
    o3_local_fraction_heating : Measurement | None = None
    o3_local_fraction_industry : Measurement | None = None
     
class ForurensningsTimeseries(BaseModel):
     # Dataset -> data -> "-> time -> (from', 'to', 'variables', 'reason')
    #setter from_ som key siden from er reservert
    from_: datetime = Field(default=None, alias="from")
    variables : ForurensningsVariables| None = None


class ForurensningsData(BaseModel):
    # Dataset -> data -> location -> (time)
    time : list[ForurensningsTimeseries]| None = None


class ForurensningsLokasjon(BaseModel):
    # dataset -> meta -> location (['name', 'path', 'areacode', 'longitude', 'latitude', 'areaclass', 'superareacode']))
    path : str
    name : str | None = None
    longitude : float | None = None
    latitude : float | None = None
    

class  ForurensningsMeta(BaseModel):
# dataset -> meta ->(superlocation + location)
    location : ForurensningsLokasjon | None = None

class ForurensningsModel(BaseModel):
    meta : ForurensningsMeta | None = None
    data : ForurensningsData | None = None


