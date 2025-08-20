
import unittest
from best_route.geo import Location
from best_route.models import Restaurant, Consumer, Order, InputData
from best_route.factory import PlannerFactory

class TestPlanner(unittest.TestCase):
    def sample(self):
        start = Location("Start", 12.935, 77.61)
        r1 = Restaurant("R1", Location("R1", 12.94, 77.62), 12.0)
        r2 = Restaurant("R2", Location("R2", 12.93, 77.60), 8.0)
        c1 = Consumer("C1", Location("C1", 12.945, 77.625))
        c2 = Consumer("C2", Location("C2", 12.925, 77.605))
        orders = {"O1": Order("O1", "R1", "C1"), "O2": Order("O2", "R2", "C2")}
        return InputData(start, {"R1": r1, "R2": r2}, {"C1": c1, "C2": c2}, orders)

    def test_plan(self):
        data = self.sample()
        planner = PlannerFactory.get_planner("exact", data, 20.0)
        result = planner.plan()
        self.assertGreater(len(result.steps), 0)
        picked = [s for s in result.steps if s.kind.value == "PICK"]
        dropped = [s for s in result.steps if s.kind.value == "DROP"]
        self.assertEqual(len(picked), 2)
        self.assertEqual(len(dropped), 2)
        self.assertAlmostEqual(result.steps[-1].depart_time, result.total_minutes, places=6)
