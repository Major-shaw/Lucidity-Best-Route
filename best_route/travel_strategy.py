
from abc import ABC, abstractmethod
from .geo import Location, travel_minutes

class TravelStrategy(ABC):
    @abstractmethod
    def time_minutes(self, a: Location, b: Location) -> float:
        ...

class HaversineTravelStrategy(TravelStrategy):
    def __init__(self, speed_kmph: float = 20.0):
        self.speed_kmph = speed_kmph

    def time_minutes(self, a: Location, b: Location) -> float:
        return travel_minutes(a, b, self.speed_kmph)
