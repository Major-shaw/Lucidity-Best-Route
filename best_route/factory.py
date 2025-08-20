from .scheduler import BestRoutePlanner
from .travel_strategy import HaversineTravelStrategy

class PlannerFactory:
    @staticmethod
    def get_planner(kind: str, data, speed: float = 20.0):
        if kind == "exact":
            return BestRoutePlanner(data, HaversineTravelStrategy(speed))
        else:
            raise ValueError(f"Unknown planner kind: {kind}")
