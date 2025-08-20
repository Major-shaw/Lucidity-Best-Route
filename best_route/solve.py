import json, argparse, sys
from typing import Dict, Any
from .geo import Location
from .models import Restaurant, Consumer, Order, InputData
from .factory import PlannerFactory

def load_input(d: Dict[str, Any]) -> InputData:
    courier = Location(**d["courier_start"])
    restaurants = {r["id"]: Restaurant(r["id"], Location(**r["location"]), float(r["prep_time_min"])) for r in d["restaurants"]}
    consumers = {c["id"]: Consumer(c["id"], Location(**c["location"])) for c in d["consumers"]}
    orders = {o["id"]: Order(o["id"], o["restaurant_id"], o["consumer_id"]) for o in d["orders"]}
    return InputData(courier, restaurants, consumers, orders)

def solve(payload: Dict[str, Any]) -> Dict[str, Any]:
    data = load_input(payload)
    speed = float(payload.get("avg_speed_kmph", 20.0))
    planner = PlannerFactory.get_planner("exact", data, speed)
    result = planner.plan()
    return {
        "total_minutes": result.total_minutes,
        "steps": [cmd.execute() for cmd in result.steps]
    }

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output")
    p.add_argument("--speed", type=float, default=20.0)
    args = p.parse_args()
    with open(args.input) as f:
        payload = json.load(f)
    payload["avg_speed_kmph"] = args.speed
    out = solve(payload)
    if args.output:
        with open(args.output, "w") as f:
            json.dump(out, f, indent=2)
    else:
        json.dump(out, sys.stdout, indent=2)
        print()
