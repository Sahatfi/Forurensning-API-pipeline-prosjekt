from pydantic import BaseModel, field_validator
from typing import Optional, List, Dict

class Details(BaseModel):
    # Data -> Properties -> Timeseries_Attributes -> Weatherdata -> Instant -> Details -> (data below)
    air_pressure_at_sea_level : float
    air_temperature : float
    cloud_area_fraction : float
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
    summary : Summary
class Weatherdata(BaseModel):
    #Data -> Properties -> Timeseries_Attributes -> Weatherdata ->(instant + next 12 hrs)
    instant : Instant
    next_12_hours : Next12Hrs | None = None

class Timeseries_Attributes(BaseModel):
    #Data -> Properties -> Timeseries_Attributes-> (time + data)
    time: str
    data: Weatherdata

class Units(BaseModel):
    #Data -> Properties -> Units -> (units below)
    air_pressure_at_sea_level: str
    air_temperature: str
    precipitation_amount: str
    relative_humidity: str
    wind_from_direction: str
    wind_speed: str

class Meta(BaseModel):
    #Data -> Properties -> Meta (updated_at + units)
    updated_at: str
    units: Units

class Properties(BaseModel):
    #Data -> Properties -> (meta + timeseries)
    meta: Meta
    timeseries: list[Timeseries_Attributes]

class Coordinates(BaseModel):
    #Geometry -> coordinates -> [lon, lat, alt]
    lon : float
    lat : float
    alt : float
    
class Geometry(BaseModel):
    #Geometry -> (type + coordinates)
    type: str
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
#class ForurensningsVariables(BaseModel):
     # Dataset -> data -> "location-> time -> variables -> 


class ForurensningsTimeseries(BaseModel):
     # Dataset -> data -> "location-> time -> (from', 'to', 'variables', 'reason')
    variables : Optional[str]
    


class ForurensningsData(BaseModel):
    # Dataset -> data -> location -> (time)
    time : list[ForurensningsTimeseries]

class  ForurensningsLokasjon(BaseModel):
    # dataset -> meta ->(location)
    longitude : float
    latitude : float


class ForurensningsSuperLokasjon(BaseModel):
    # dataset -> meta ->(superlocation)
    name : str
    

class  ForurensningsMeta(BaseModel):
# dataset -> meta ->(superlocation + location)
    superlocation: ForurensningsSuperLokasjon
    location : ForurensningsLokasjon

class ForurensningsModel(BaseModel):
    meta : ForurensningsMeta
    data : ForurensningsData





