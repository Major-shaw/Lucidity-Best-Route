# Best Route Planner

Computes the fastest route for a courier to pick up and deliver N orders.  
The solution respects restaurant preparation times, enforces pickup-before-drop constraints, and models travel time using Haversine distance with a configurable courier speed.

The package is designed with extensibility in mind and applies key low-level design patterns: **Strategy**, **Command**, **Factory**, and **Enums**.

---

## Features

- Haversine distance with configurable courier speed (default: 20 km/h)
- Restaurant preparation times respected (courier may wait if arriving early)
- Pickup-before-drop enforced for all orders
- Optimal planning using branch-and-bound with admissible lower bound
- Travel time calculation implemented as a pluggable Strategy
- Courier actions encapsulated as Commands
- Planner selection abstracted with a Factory
- Unit tests included

---

## Project Structure

```bash
best\_route/
├── enums.py             # Enums for ActionType, Notes
├── geo.py               # Location model and Haversine distance
├── models.py            # Restaurant, Consumer, Order, InputData
├── travel\_strategy.py   # Strategy Pattern for travel-time calculation
├── commands.py          # Command Pattern for courier actions
├── scheduler.py         # Exact DFS + branch-and-bound planner
├── factory.py           # Factory Pattern for planner selection
├── solve.py             # CLI entrypoint
tests/
└── test\_scheduler.py    # Unit tests
sample.json               # Example input
README.md                 # Project documentation
```

---

## Installation

```bash
# Clone or unzip the repository
cd lucidity_best_route

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\\Scripts\\activate    # Windows

# Install dependencies (none required beyond standard library)
pip install -U pip
```

---

## Usage

### Command Line Interface

```bash
python -m best_route.solve --input sample.json --speed 20
```

### Input JSON Schema

```json
{
  "avg_speed_kmph": 20,
  "courier_start": {"name": "Start", "lat": 12.935, "lon": 77.61},
  "restaurants": [
    {"id": "R1", "location": {"name": "R1", "lat": 12.94, "lon": 77.62}, "prep_time_min": 12},
    {"id": "R2", "location": {"name": "R2", "lat": 12.93, "lon": 77.60}, "prep_time_min": 8}
  ],
  "consumers": [
    {"id": "C1", "location": {"name": "C1", "lat": 12.945, "lon": 77.625}},
    {"id": "C2", "location": {"name": "C2", "lat": 12.925, "lon": 77.605}}
  ],
  "orders": [
    {"id": "O1", "restaurant_id": "R1", "consumer_id": "C1"},
    {"id": "O2", "restaurant_id": "R2", "consumer_id": "C2"}
  ]
}
```

### Output JSON Example

```json
{
  "total_minutes": 42.5,
  "steps": [
    {
      "action": "PICK",
      "order_id": "O1",
      "from": {"name": "Start", "lat": 12.935, "lon": 77.61},
      "to": {"name": "R1", "lat": 12.94, "lon": 77.62},
      "travel_min": 5.2,
      "wait_min": 3.0,
      "arrive_time": 5.2,
      "depart_time": 8.2,
      "notes": "Arrived early, waited"
    },
    {
      "action": "DROP",
      "order_id": "O1",
      "from": {"name": "R1", "lat": 12.94, "lon": 77.62},
      "to": {"name": "C1", "lat": 12.945, "lon": 77.625},
      "travel_min": 4.0,
      "wait_min": 0.0,
      "arrive_time": 12.2,
      "depart_time": 12.2,
      "notes": "Delivered"
    }
  ]
}
```

---

## Testing

Run all unit tests:

```bash
python -m unittest -v
```

---

## Design Patterns

* **Enums**: Centralized string constants (`ActionType`, `Notes`) for type safety and maintainability.
* **Strategy Pattern**: `TravelStrategy` abstraction allows different travel-time calculators (e.g., Haversine, API-based).
* **Command Pattern**: Encapsulates courier actions (pickup/drop) with execution and serialization.
* **Factory Pattern**: `PlannerFactory` enables switching between planning algorithms (e.g., exact, greedy).

---

## Complexity Notes

This problem is a variant of the **Pickup and Delivery Problem**, which is NP-hard.

* The provided solver uses **branch-and-bound DFS** with pruning, which is exact and suitable for small to medium problem sizes (2–10 orders depending on geometry and prep times).
* For larger problem instances, heuristic or approximation algorithms are recommended:

  * Greedy insertion heuristic
  * Metaheuristics such as Simulated Annealing or Large Neighborhood Search
  * Mixed-Integer Linear Programming (MILP) formulations
