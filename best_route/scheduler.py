from dataclasses import dataclass
from typing import Dict, List, Tuple, Set
from .geo import Location
from .models import InputData, Order
from .enums import ActionType, Notes
from .commands import Command
from .travel_strategy import TravelStrategy

@dataclass
class PlanResult:
    steps: List[Command]
    total_minutes: float

class BestRoutePlanner:
    def __init__(self, data: InputData, strategy: TravelStrategy):
        self.data = data
        self.strategy = strategy
        self.orders: Dict[str, Order] = data.orders
        self.pick_locs: Dict[str, Location] = {o.id: data.restaurants[o.restaurant_id].location for o in self.orders.values()}
        self.drop_locs: Dict[str, Location] = {o.id: data.consumers[o.consumer_id].location for o in self.orders.values()}
        self.ready_times: Dict[str, float] = {o.id: data.restaurants[o.restaurant_id].prep_time_min for o in self.orders.values()}

    def plan(self) -> PlanResult:
        order_ids = list(self.orders.keys())
        best: Tuple[float, List[Command]] = (float("inf"), [])
        from_loc = self.data.courier_start

        def lower_bound(curr_time: float, curr_loc: Location, picked: Set[str], delivered: Set[str]) -> float:
            targets = []
            for oid in order_ids:
                if oid not in picked:
                    targets.append(self.pick_locs[oid])
                if oid not in delivered and oid in picked:
                    targets.append(self.drop_locs[oid])
            if not targets:
                return curr_time
            best_first = min(self.strategy.time_minutes(curr_loc, t) for t in targets)
            return curr_time + best_first

        def dfs(curr_time: float, curr_loc: Location, picked: Set[str], delivered: Set[str], steps: List[Command]):
            nonlocal best
            if len(delivered) == len(order_ids):
                if curr_time < best[0]:
                    best = (curr_time, steps.copy())
                return

            if lower_bound(curr_time, curr_loc, picked, delivered) >= best[0]:
                return

            for oid in order_ids:
                if oid not in picked:
                    to = self.pick_locs[oid]
                    t_travel = self.strategy.time_minutes(curr_loc, to)
                    arrive = curr_time + t_travel
                    ready = self.ready_times[oid]
                    wait = max(0.0, ready - arrive)
                    depart = arrive + wait
                    cmd = Command(ActionType.PICK, oid, curr_loc, to, t_travel, wait, arrive, depart,
                                  Notes.WAITED.value if wait > 0 else Notes.ON_TIME.value)
                    picked.add(oid)
                    steps.append(cmd)
                    dfs(depart, to, picked, delivered, steps)
                    steps.pop()
                    picked.remove(oid)

            for oid in order_ids:
                if oid in picked and oid not in delivered:
                    to = self.drop_locs[oid]
                    t_travel = self.strategy.time_minutes(curr_loc, to)
                    arrive = curr_time + t_travel
                    cmd = Command(ActionType.DROP, oid, curr_loc, to, t_travel, 0.0, arrive, arrive, Notes.DELIVERED.value)
                    delivered.add(oid)
                    steps.append(cmd)
                    dfs(arrive, to, picked, delivered, steps)
                    steps.pop()
                    delivered.remove(oid)

        dfs(0.0, from_loc, set(), set(), [])
        return PlanResult(steps=best[1], total_minutes=best[0])
