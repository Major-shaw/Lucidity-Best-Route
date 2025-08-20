from dataclasses import dataclass
from typing import Dict
from .geo import Location

@dataclass(frozen=True)
class Restaurant:
    id: str
    location: Location
    prep_time_min: float

@dataclass(frozen=True)
class Consumer:
    id: str
    location: Location

@dataclass(frozen=True)
class Order:
    id: str
    restaurant_id: str
    consumer_id: str

@dataclass
class InputData:
    courier_start: Location
    restaurants: Dict[str, Restaurant]
    consumers: Dict[str, Consumer]
    orders: Dict[str, Order]
