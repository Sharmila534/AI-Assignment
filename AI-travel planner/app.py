from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

from planner.domain_knowledge import DEPARTURE_CITIES, DESTINATIONS, build_problem_data
from planner.goal_stack import GoalStackPlanner
from planner.pddl_export import write_pddl_files


def render_page(result=None, values=None):
    values = values or {}
    selected_destinations = values.get("destinations", ["goa", "jaipur"])
    if isinstance(selected_destinations, str):
        selected_destinations = [selected_destinations]
    selected_goal = values.get("goal", "relaxation")
    selected_budget = values.get("budget", "medium")
    selected_days = values.get("days", "6")
    selected_transport = values.get("transport", "train")
    selected_hotel = values.get("hotel", "standard")
    selected_departure = values.get("departure_city", "Chennai")

    options = {
        "goal": ["relaxation", "culture", "adventure"],
        "budget": ["low", "medium", "high"],
        "transport": ["train", "flight", "bus"],
        "hotel": ["budget", "standard", "premium"],
        "departure_city": DEPARTURE_CITIES,
    }

    def select(name, current):
        return "".join(
            f'<option value="{item}" {"selected" if item == current else ""}>{item}</option>'
            for item in options[name]
        )

    destination_boxes = "".join(
        f"""
        <label class="check-card">
          <input type="checkbox" name="destinations" value="{key}" {"checked" if key in selected_destinations else ""}>
          <span>{value["label"]}</span>
          <small>{value["type"].title()}</small>
        </label>
        """
        for key, value in DESTINATIONS.items()
    )

    result_html = ""
    if result:
        plan_items = "".join(f"<li>{step}</li>" for step in result["plan"])
        route_items = "".join(
            f"""
            <div class="mini-card">
              <h4>{segment["from"]} to {segment["to"]}</h4>
              <p><strong>Distance:</strong> {segment["distance_km"]} km</p>
              <p><strong>Time:</strong> {segment["time_hours"]} hours</p>
              <p><strong>Budget:</strong> Rs. {segment["budget_inr"]}</p>
              <p><strong>Route Stops:</strong> {", ".join(item.replace("_", " ").title() for item in segment["stopovers"]) if segment["stopovers"] else "Direct segment"}</p>
            </div>
            """
            for segment in result["route_segments"]
        )
        day_cards = "".join(
            f"""
            <div class="mini-card">
              <h4>Day {item["day"]}: {item["title"]}</h4>
              <p><strong>Morning:</strong> {item["morning"]}</p>
              <p><strong>Afternoon:</strong> {item["afternoon"]}</p>
              <p><strong>Evening:</strong> {item["evening"]}</p>
              <p><strong>Must Taste:</strong> {item["must_try_food"]}</p>
            </div>
            """
            for item in result["itinerary"]
        )
        guide_cards = "".join(
            f"""
            <div class="mini-card">
              <h4>{guide["name"]}</h4>
              <p><strong>Type:</strong> {guide["kind"].replace("_", " ").title()}</p>
              <p><strong>Places:</strong> {", ".join(guide["places"])}</p>
              <p><strong>Food:</strong> {", ".join(guide["food"])}</p>
              <p><strong>Experiences:</strong> {", ".join(guide["experiences"])}</p>
            </div>
            """
            for guide in result["guide_cards"]
        )
        result_html = f"""
        <section class="card">
          <h2>Professional Tourist Guide Plan</h2>
          <p><strong>Optimized Route:</strong> {result["route_label"]}</p>
          <p><strong>Total Distance:</strong> {result["total_distance_km"]} km</p>
          <p><strong>Total Time:</strong> {result["total_time_hours"]} hours</p>
          <p><strong>Estimated Budget:</strong> Rs. {result["total_budget_inr"]}</p>
          <p><strong>Featured Activity:</strong> {result["beach_activity"]}</p>
          <p><strong>Suggested First Hotel Area:</strong> {result["hotel_area"]}</p>
          <h3>Planner Actions</h3>
          <ol>{plan_items}</ol>
          <h3>Best Route Segments</h3>
          <div class="days-grid">{route_items}</div>
          <h3>Day-Wise Itinerary</h3>
          <div class="days-grid">{day_cards}</div>
          <h3>Places To Visit Across Main Destinations And Route Stops</h3>
          <div class="days-grid">{guide_cards}</div>
          <h3>Planning Model Used</h3>
          <ul>
            <li><strong>STRIPS:</strong> Planning actions use preconditions and effects.</li>
            <li><strong>Goal Stack Planning:</strong> The planner creates the required action sequence.</li>
            <li><strong>Knowledge-Based Planning:</strong> India travel facts drive routing and sightseeing advice.</li>
          </ul>
          <h3>PDDL Output</h3>
          <pre>{result["domain_pddl"]}</pre>
          <pre>{result["problem_pddl"]}</pre>
        </section>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AI Travel Planner</title>
  <style>
    :root {{
      --panel: #fff9f1;
      --line: #dfd0bb;
      --ink: #23313b;
      --accent: #0f766e;
      --accent-dark: #0a4d48;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Georgia, "Trebuchet MS", sans-serif;
      color: var(--ink);
      background:
        radial-gradient(circle at top right, rgba(15, 118, 110, 0.18), transparent 30%),
        linear-gradient(135deg, #fcf7ef, #efdfc6);
    }}
    .wrap {{
      max-width: 1160px;
      margin: 0 auto;
      padding: 28px 18px 40px;
    }}
    .hero, .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 22px;
      padding: 24px;
      box-shadow: 0 16px 34px rgba(35, 49, 59, 0.08);
    }}
    .card {{ margin-top: 22px; }}
    .grid, .days-grid, .checks {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 14px;
    }}
    .days-grid, .checks {{ margin-top: 16px; }}
    .mini-card, .check-card {{
      background: #fff;
      border: 1px solid #eadfce;
      border-radius: 16px;
      padding: 14px;
    }}
    .check-card {{
      display: block;
      cursor: pointer;
    }}
    .check-card input {{
      width: auto;
      margin-right: 8px;
    }}
    .check-card span {{
      font-weight: 700;
    }}
    .check-card small {{
      display: block;
      margin-top: 6px;
      color: #52606d;
    }}
    label.field {{
      display: block;
      margin-bottom: 6px;
      font-weight: 700;
    }}
    input, select, button {{
      width: 100%;
      border-radius: 12px;
      border: 1px solid #cebda7;
      padding: 11px 12px;
      font-size: 15px;
    }}
    button {{
      background: var(--accent);
      color: #fff;
      border: 0;
      font-weight: 700;
      cursor: pointer;
      margin-top: 10px;
    }}
    button:hover {{ background: var(--accent-dark); }}
    pre {{
      white-space: pre-wrap;
      background: #1f262c;
      color: #f8f5ef;
      border-radius: 14px;
      padding: 14px;
      overflow-x: auto;
    }}
    .pill {{
      display: inline-block;
      background: #dcefe9;
      padding: 6px 10px;
      border-radius: 999px;
      margin-right: 6px;
      font-size: 13px;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <h1>India Tourist Guide Planner</h1>
      <p>Select multiple destinations and the planner will produce the best circular route from Chennai with sightseeing stops, itinerary, food, and experiences.</p>
      <p>
        <span class="pill">Python</span>
        <span class="pill">PDDL</span>
        <span class="pill">STRIPS</span>
        <span class="pill">Goal Stack Planning</span>
      </p>
      <form method="post">
        <label class="field">Choose One Or More Main Destinations</label>
        <div class="checks">{destination_boxes}</div>
        <div class="grid">
          <div>
            <label class="field" for="goal">Travel Goal</label>
            <select id="goal" name="goal">{select("goal", selected_goal)}</select>
          </div>
          <div>
            <label class="field" for="budget">Budget</label>
            <select id="budget" name="budget">{select("budget", selected_budget)}</select>
          </div>
          <div>
            <label class="field" for="days">Days</label>
            <input id="days" name="days" type="number" min="3" max="10" value="{selected_days}">
          </div>
          <div>
            <label class="field" for="departure_city">Departure City</label>
            <select id="departure_city" name="departure_city">{select("departure_city", selected_departure)}</select>
          </div>
          <div>
            <label class="field" for="transport">Transport</label>
            <select id="transport" name="transport">{select("transport", selected_transport)}</select>
          </div>
          <div>
            <label class="field" for="hotel">Hotel Type</label>
            <select id="hotel" name="hotel">{select("hotel", selected_hotel)}</select>
          </div>
          <div style="align-self:end;">
            <button type="submit">Generate Professional Travel Plan</button>
          </div>
        </div>
      </form>
    </section>
    {result_html}
  </div>
</body>
</html>
"""


class TravelPlannerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.respond(render_page())

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        raw_data = self.rfile.read(content_length).decode("utf-8")
        parsed = parse_qs(raw_data)
        form = {key: values[0] if len(values) == 1 else values for key, values in parsed.items()}

        problem = build_problem_data(form)
        planner = GoalStackPlanner(problem["actions"])
        plan = planner.plan(problem["initial_state"], problem["goal_state"])
        domain_pddl, problem_pddl = write_pddl_files(problem)

        result = {
            "plan": plan,
            "route_label": problem["route_label"],
            "route_segments": problem["route_segments"],
            "total_distance_km": problem["total_distance_km"],
            "total_time_hours": problem["total_time_hours"],
            "total_budget_inr": problem["total_budget_inr"],
            "beach_activity": problem["beach_activity"],
            "hotel_area": problem["hotel_area"],
            "guide_cards": problem["guide_cards"],
            "itinerary": problem["itinerary"],
            "domain_pddl": domain_pddl,
            "problem_pddl": problem_pddl,
        }
        self.respond(render_page(result=result, values=form))

    def respond(self, html):
        body = html.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8000), TravelPlannerHandler)
    print("Open http://127.0.0.1:8000 in your browser")
    server.serve_forever()
