"""
pydantic model for vehicles data coming from https://swapi.dev/api/vehicles
"""
from typing import Optional, List
from models.basemodel import Base


class Vehicles(Base):
    """
    Data model for passing the data of vehicles from `star_wars API`
    """

    name: str
    model: str
    manufacturer: str
    cost_in_credits: str
    length: str
    max_atmosphering_speed: str
    crew: str
    passengers: str
    cargo_capacity: str
    consumables: str
    vehicle_class: str

    pilots: Optional[List[str]]
    films: Optional[List[str]]


if __name__ == "__main__":
    data = {
        "name": "Sand Crawler",
        "model": "Digger Crawler",
        "manufacturer": "Corellia Mining Corporation",
        "cost_in_credits": "150000",
        "length": "36.8 ",
        "max_atmosphering_speed": "30",
        "crew": "46",
        "passengers": "30",
        "cargo_capacity": "50000",
        "consumables": "2 months",
        "vehicle_class": "wheeled",
        "pilots": [],
        "films": ["https://swapi.dev/api/films/1/", "https://swapi.dev/api/films/5/"],
        "created": "2014-12-10T15:36:25.724000Z",
        "edited": "2014-12-20T21:30:21.661000Z",
        "url": "https://swapi.dev/api/vehicles/4/",
    }

    obj = Vehicles(**data)
    print(obj)
