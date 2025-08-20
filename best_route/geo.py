import math
from dataclasses import dataclass

EARTH_RADIUS_KM = 6371.0

@dataclass(frozen=True)
class Location:
    name: str
    lat: float
    lon: float

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS_KM * c

def travel_minutes(a: Location, b: Location, speed_kmph: float) -> float:
    dist_km = haversine_km(a.lat, a.lon, b.lat, b.lon)
    return (dist_km / speed_kmph) * 60.0 if speed_kmph > 0 else float("inf")
