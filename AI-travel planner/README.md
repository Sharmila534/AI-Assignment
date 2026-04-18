# AI-Based Automated Travel Planner

This mini project is a concise Python website that acts like a professional India tourist guide using:

- `STRIPS`
- `Goal Stack Planning`
- `Knowledge-Based Planning`
- `PDDL`

## File Structure

```text
New project/
|-- app.py
|-- planner/
|   |-- __init__.py
|   |-- domain_knowledge.py
|   |-- goal_stack.py
|   `-- pddl_export.py
|-- pddl/
|   |-- domain.pddl
|   `-- problem.pddl
`-- README.md
```

## How To Run In VS Code

1. Open `New project` in VS Code.
2. Open the terminal.
3. Run:

```bash
python app.py
```

4. Open:

```text
http://127.0.0.1:8000
```

## User Inputs

- Multiple destinations in India
- Travel goal
- Budget
- Number of days
- Departure city
- Transport
- Hotel type

## Planning Actions Used

- `choose_destination`
- `book_beach_activity`
- `reserve_transport`
- `reserve_hotel`
- `prepare_itinerary`
- `confirm_trip`

## Output Shown

- Optimized multi-city route
- Total distance
- Total travel time
- Route transport cost
- Full trip budget estimate
- Recommended hotel areas
- Places to visit
- Day-wise trip schedule
- Must-try food
- Must-do experiences
- Generated `domain.pddl` and `problem.pddl`

## Short Viva Points

- `domain_knowledge.py` stores India destination facts, route distances, and budget rules.
- `goal_stack.py` generates the action sequence using Goal Stack Planning.
- `pddl_export.py` creates the PDDL domain and problem files.
- `app.py` runs the local website and shows the optimized tourist plan.
