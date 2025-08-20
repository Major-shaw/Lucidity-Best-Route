from dataclasses import dataclass
from .enums import ActionType
from .geo import Location

@dataclass
class Command:
    kind: ActionType
    order_id: str
    from_loc: Location
    to_loc: Location
    travel_min: float
    wait_min: float
    arrive_time: float
    depart_time: float
    notes: str

    def execute(self):
        # For extensibility: log, audit, simulate, etc.
        return {
            "action": self.kind.value,
            "order_id": self.order_id,
            "from": {"name": self.from_loc.name, "lat": self.from_loc.lat, "lon": self.from_loc.lon},
            "to": {"name": self.to_loc.name, "lat": self.to_loc.lat, "lon": self.to_loc.lon},
            "travel_min": self.travel_min,
            "wait_min": self.wait_min,
            "arrive_time": self.arrive_time,
            "depart_time": self.depart_time,
            "notes": self.notes,
        }
