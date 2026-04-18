import itertools
import math

from planner.goal_stack import Action


DEPARTURE_CITIES = ["Chennai", "Delhi", "Mumbai", "Bengaluru", "Hyderabad", "Kolkata"]

HOME_BASES = {
    "chennai": {"label": "Chennai", "coords": (13.0827, 80.2707)},
    "delhi": {"label": "Delhi", "coords": (28.6139, 77.2090)},
    "mumbai": {"label": "Mumbai", "coords": (19.0760, 72.8777)},
    "bengaluru": {"label": "Bengaluru", "coords": (12.9716, 77.5946)},
    "hyderabad": {"label": "Hyderabad", "coords": (17.3850, 78.4867)},
    "kolkata": {"label": "Kolkata", "coords": (22.5726, 88.3639)},
}


DESTINATIONS = {
    "goa": {
        "label": "Goa",
        "type": "beach",
        "coords": (15.2993, 74.1240),
        "hotel_areas": {"budget": "Anjuna", "standard": "Calangute", "premium": "Candolim"},
        "places": ["Baga Beach", "Fort Aguada", "Fontainhas", "Dudhsagar Falls"],
        "food": ["Goan fish curry", "bebinca", "prawn balchao", "poi bread"],
        "experiences": ["sunset beach walk", "water sports", "night market visit", "Latin quarter heritage stroll"],
        "featured_activity": "Baga Beach water sports session",
    },
    "jaipur": {
        "label": "Jaipur",
        "type": "heritage",
        "coords": (26.9124, 75.7873),
        "hotel_areas": {"budget": "Bani Park", "standard": "MI Road", "premium": "Civil Lines"},
        "places": ["Amber Fort", "City Palace", "Hawa Mahal", "Jantar Mantar"],
        "food": ["dal baati churma", "pyaaz kachori", "ghewar", "laal maas"],
        "experiences": ["folk dance evening", "bazaar shopping", "fort light show", "block print shopping"],
        "featured_activity": "Amber Fort cultural circuit",
    },
    "kerala": {
        "label": "Kerala",
        "type": "nature",
        "coords": (9.9312, 76.2673),
        "hotel_areas": {"budget": "Alleppey town", "standard": "Fort Kochi", "premium": "Munnar hills"},
        "places": ["Fort Kochi", "Alleppey Backwaters", "Munnar Tea Gardens", "Mattancherry Palace"],
        "food": ["appam with stew", "Kerala sadya", "karimeen pollichathu", "banana chips"],
        "experiences": ["houseboat cruise", "Kathakali show", "tea estate walk", "sunset by Chinese fishing nets"],
        "featured_activity": "Cherai Beach leisure session",
    },
    "manali": {
        "label": "Manali",
        "type": "mountain",
        "coords": (32.2432, 77.1892),
        "hotel_areas": {"budget": "Old Manali", "standard": "Mall Road", "premium": "Log Huts area"},
        "places": ["Solang Valley", "Hadimba Temple", "Old Manali", "Vashisht"],
        "food": ["siddu", "thukpa", "trout fish", "mittha"],
        "experiences": ["ropeway ride", "snow activities", "riverside cafe hopping", "hot spring stop"],
        "featured_activity": "Solang Valley adventure session",
    },
    "varanasi": {
        "label": "Varanasi",
        "type": "spiritual",
        "coords": (25.3176, 82.9739),
        "hotel_areas": {"budget": "Godowlia", "standard": "Assi Ghat", "premium": "Cantonment"},
        "places": ["Kashi Vishwanath Temple", "Dashashwamedh Ghat", "Sarnath", "Assi Ghat"],
        "food": ["kachori sabzi", "malaiyyo", "tamatar chaat", "banarasi paan"],
        "experiences": ["Ganga aarti", "sunrise boat ride", "temple trail", "silk weaving lane walk"],
        "featured_activity": "Ghat-side evening relaxation walk",
    },
}


STOPOVER_GUIDE = {
    "bengaluru": {
        "label": "Bengaluru",
        "places": ["Cubbon Park", "Bangalore Palace"],
        "food": ["masala dosa"],
        "experiences": ["brewery street evening"],
    },
    "mysuru": {
        "label": "Mysuru",
        "places": ["Mysore Palace", "Chamundi Hills"],
        "food": ["Mysore pak"],
        "experiences": ["palace illumination"],
    },
    "hampi": {
        "label": "Hampi",
        "places": ["Virupaksha Temple", "Stone Chariot"],
        "food": ["north Karnataka meals"],
        "experiences": ["sunset at Hemakuta Hill"],
    },
    "pune": {
        "label": "Pune",
        "places": ["Shaniwar Wada", "Aga Khan Palace"],
        "food": ["misal pav"],
        "experiences": ["old city food trail"],
    },
    "mumbai": {
        "label": "Mumbai",
        "places": ["Gateway of India", "Marine Drive"],
        "food": ["vada pav"],
        "experiences": ["sunset at Marine Drive"],
    },
    "udupi": {
        "label": "Udupi",
        "places": ["Malpe Beach", "Sri Krishna Temple"],
        "food": ["goli baje"],
        "experiences": ["coastal cafe stop"],
    },
    "madurai": {
        "label": "Madurai",
        "places": ["Meenakshi Temple", "Thirumalai Nayakkar Mahal"],
        "food": ["jigarthanda"],
        "experiences": ["night temple corridor walk"],
    },
    "kochi": {
        "label": "Kochi",
        "places": ["Fort Kochi waterfront", "Jew Town"],
        "food": ["fish pollichathu"],
        "experiences": ["harbour sunset"],
    },
    "hyderabad": {
        "label": "Hyderabad",
        "places": ["Charminar", "Golconda Fort"],
        "food": ["Hyderabadi biryani"],
        "experiences": ["night market visit"],
    },
    "nagpur": {
        "label": "Nagpur",
        "places": ["Deekshabhoomi", "Futala Lake"],
        "food": ["saoji curry"],
        "experiences": ["lakefront evening"],
    },
    "bhopal": {
        "label": "Bhopal",
        "places": ["Upper Lake", "Tribal Museum"],
        "food": ["poha jalebi"],
        "experiences": ["lakeside walk"],
    },
    "delhi": {
        "label": "Delhi",
        "places": ["India Gate", "Humayun's Tomb"],
        "food": ["chole bhature"],
        "experiences": ["Old Delhi food trail"],
    },
    "chandigarh": {
        "label": "Chandigarh",
        "places": ["Rock Garden", "Sukhna Lake"],
        "food": ["stuffed kulcha"],
        "experiences": ["lake promenade"],
    },
    "vijayawada": {
        "label": "Vijayawada",
        "places": ["Kanaka Durga Temple", "Bhavani Island"],
        "food": ["Andhra meals"],
        "experiences": ["riverfront stop"],
    },
}


ROUTE_CORRIDORS = {
    frozenset({"chennai", "goa"}): ["bengaluru", "hampi"],
    frozenset({"chennai", "jaipur"}): ["hyderabad", "bhopal"],
    frozenset({"chennai", "kerala"}): ["madurai", "kochi"],
    frozenset({"chennai", "manali"}): ["hyderabad", "delhi", "chandigarh"],
    frozenset({"chennai", "varanasi"}): ["vijayawada", "hyderabad"],
    frozenset({"goa", "jaipur"}): ["mumbai", "udaipur"],
    frozenset({"goa", "kerala"}): ["udupi", "kochi"],
    frozenset({"goa", "manali"}): ["mumbai", "delhi", "chandigarh"],
    frozenset({"goa", "varanasi"}): ["mumbai", "bhopal"],
    frozenset({"jaipur", "kerala"}): ["udaipur", "mumbai", "kochi"],
    frozenset({"jaipur", "manali"}): ["delhi", "chandigarh"],
    frozenset({"jaipur", "varanasi"}): ["agra", "prayagraj"],
    frozenset({"kerala", "manali"}): ["kochi", "delhi", "chandigarh"],
    frozenset({"kerala", "varanasi"}): ["hyderabad", "nagpur"],
    frozenset({"manali", "varanasi"}): ["delhi", "prayagraj"],
}


STOPOVER_GUIDE.update(
    {
        "udaipur": {
            "label": "Udaipur",
            "places": ["City Palace", "Lake Pichola"],
            "food": ["dal bati"],
            "experiences": ["boat ride"],
        },
        "agra": {
            "label": "Agra",
            "places": ["Taj Mahal", "Agra Fort"],
            "food": ["petha"],
            "experiences": ["sunrise monument view"],
        },
        "prayagraj": {
            "label": "Prayagraj",
            "places": ["Triveni Sangam", "Anand Bhavan"],
            "food": ["kachori"],
            "experiences": ["ghat boat stop"],
        },
    }
)


TRANSPORT_FACTORS = {
    "flight": {"speed": 620, "cost_per_km": 6.0, "fixed": 2200},
    "train": {"speed": 58, "cost_per_km": 1.4, "fixed": 400},
    "bus": {"speed": 42, "cost_per_km": 1.1, "fixed": 250},
}


def to_slug(city_name):
    return city_name.strip().lower().replace(" ", "_")


def haversine_km(a, b):
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    arc = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(arc))


def route_distance_km(start_key, end_key):
    coords = {**{key: value["coords"] for key, value in HOME_BASES.items()}, **{key: value["coords"] for key, value in DESTINATIONS.items()}}
    base = haversine_km(coords[start_key], coords[end_key])
    return round(base * 1.18)


def segment_stopovers(start_key, end_key):
    return ROUTE_CORRIDORS.get(frozenset({start_key, end_key}), [])


def estimate_segment(start_key, end_key, transport):
    distance = route_distance_km(start_key, end_key)
    factors = TRANSPORT_FACTORS[transport]
    stopover_penalty = len(segment_stopovers(start_key, end_key)) * 1.4
    time_hours = round(distance / factors["speed"] + stopover_penalty, 1)
    budget = round(distance * factors["cost_per_km"] + factors["fixed"])
    return distance, time_hours, budget


def choose_best_destinations(goal, budget):
    ranked = {
        ("relaxation", "low"): ["goa", "kerala"],
        ("relaxation", "medium"): ["goa", "kerala"],
        ("relaxation", "high"): ["kerala", "goa"],
        ("culture", "low"): ["varanasi", "jaipur"],
        ("culture", "medium"): ["jaipur", "varanasi"],
        ("culture", "high"): ["jaipur", "varanasi"],
        ("adventure", "low"): ["goa", "manali"],
        ("adventure", "medium"): ["manali", "goa"],
        ("adventure", "high"): ["manali", "goa"],
    }
    return ranked.get((goal, budget), ["goa", "jaipur"])


def pick_destinations(form):
    picked = form.get("destinations", [])
    if isinstance(picked, str):
        picked = [picked]
    picked = [item for item in picked if item in DESTINATIONS]
    if not picked:
        goal = form.get("goal", "relaxation")
        budget = form.get("budget", "medium")
        picked = choose_best_destinations(goal, budget)
    return picked[:3]


def optimize_route(home_key, selected_destinations, transport):
    best = None
    for perm in itertools.permutations(selected_destinations):
        route = [home_key, *perm, home_key]
        total_distance = 0
        total_time = 0
        total_budget = 0
        segments = []
        for start, end in zip(route, route[1:]):
            distance, time_hours, budget = estimate_segment(start, end, transport)
            total_distance += distance
            total_time += time_hours
            total_budget += budget
            segments.append(
                {
                    "from": HOME_BASES[start]["label"] if start in HOME_BASES else DESTINATIONS[start]["label"],
                    "to": HOME_BASES[end]["label"] if end in HOME_BASES else DESTINATIONS[end]["label"],
                    "from_key": start,
                    "to_key": end,
                    "distance_km": distance,
                    "time_hours": time_hours,
                    "budget_inr": budget,
                    "stopovers": segment_stopovers(start, end),
                }
            )
        score = total_distance + total_time * 12 + total_budget / 140
        candidate = {
            "ordered_destinations": list(perm),
            "segments": segments,
            "total_distance_km": total_distance,
            "total_time_hours": round(total_time, 1),
            "total_budget_inr": total_budget,
            "score": round(score, 2),
        }
        if best is None or candidate["score"] < best["score"]:
            best = candidate
    return best


def build_city_guides(destination_keys):
    guides = []
    for key in destination_keys:
        data = DESTINATIONS[key]
        guides.append(
            {
                "name": data["label"],
                "places": data["places"],
                "food": data["food"],
                "experiences": data["experiences"],
                "kind": "main_destination",
            }
        )
    return guides


def build_stopover_guides(segments):
    guides = []
    seen = set()
    for segment in segments:
        for stop_key in segment["stopovers"]:
            if stop_key in seen:
                continue
            seen.add(stop_key)
            data = STOPOVER_GUIDE[stop_key]
            guides.append(
                {
                    "name": data["label"],
                    "places": data["places"],
                    "food": data["food"],
                    "experiences": data["experiences"],
                    "kind": "route_stop",
                }
            )
    return guides


def build_itinerary(optimized_route, days):
    total_days = min(max(days, len(optimized_route["ordered_destinations"]) + 2), 10)
    main_destinations = optimized_route["ordered_destinations"]
    segments = optimized_route["segments"]
    destination_days = {key: 1 for key in main_destinations}
    remaining = max(0, total_days - len(main_destinations) - 1)
    order_index = 0
    while remaining > 0:
        key = main_destinations[order_index % len(main_destinations)]
        destination_days[key] += 1
        order_index += 1
        remaining -= 1

    itinerary = []
    day = 1
    for segment_index, segment in enumerate(segments):
        segment_stops = segment["stopovers"]
        travel_summary = " -> ".join(
            [segment["from"], *[STOPOVER_GUIDE[item]["label"] for item in segment_stops], segment["to"]]
        )
        itinerary.append(
            {
                "day": day,
                "title": f"Travel: {segment['from']} to {segment['to']}",
                "morning": f"Start from {segment['from']} and follow the optimized route: {travel_summary}.",
                "afternoon": (
                    "Stop at "
                    + ", ".join(STOPOVER_GUIDE[item]["label"] for item in segment_stops)
                    if segment_stops
                    else f"Continue directly to {segment['to']}."
                ),
                "evening": f"Reach {segment['to']} after about {segment['time_hours']} hours covering {segment['distance_km']} km.",
                "must_try_food": (
                    STOPOVER_GUIDE[segment_stops[0]]["food"][0]
                    if segment_stops
                    else (DESTINATIONS.get(segment["to_key"], {"food": ["local meal"]})["food"][0])
                ),
            }
        )
        day += 1

        if segment["to_key"] in DESTINATIONS and segment_index < len(segments) - 1:
            key = segment["to_key"]
            city = DESTINATIONS[key]
            for visit_day in range(destination_days[key]):
                itinerary.append(
                    {
                        "day": day,
                        "title": f"Explore {city['label']}",
                        "morning": f"Visit {city['places'][visit_day % len(city['places'])]}.",
                        "afternoon": (
                            f"Taste {city['food'][visit_day % len(city['food'])]} and continue to "
                            f"{city['places'][(visit_day + 1) % len(city['places'])]}."
                        ),
                        "evening": f"Enjoy {city['experiences'][visit_day % len(city['experiences'])]}.",
                        "must_try_food": city["food"][visit_day % len(city["food"])],
                    }
                )
                day += 1

    return itinerary[:total_days]


def build_problem_data(form):
    goal = form.get("goal", "relaxation")
    budget = form.get("budget", "medium")
    days = int(form.get("days", "5"))
    transport = form.get("transport", "train")
    hotel = form.get("hotel", "standard")
    departure_city = form.get("departure_city", "Chennai")
    home_key = to_slug(departure_city)
    if home_key not in HOME_BASES:
        home_key = "chennai"
        departure_city = "Chennai"
    destination_keys = pick_destinations(form)
    optimized = optimize_route(home_key, destination_keys, transport)
    itinerary = build_itinerary(optimized, days)
    primary_destination = DESTINATIONS[optimized["ordered_destinations"][0]]
    route_names = [departure_city, *[DESTINATIONS[key]["label"] for key in optimized["ordered_destinations"]], departure_city]
    route_label = " -> ".join(route_names)

    main_guides = build_city_guides(optimized["ordered_destinations"])
    stopover_guides = build_stopover_guides(optimized["segments"])
    all_guides = main_guides + stopover_guides

    initial_state = {
        "user_ready",
        f"goal_{goal}",
        f"budget_{budget}",
        f"prefer_{transport}",
        f"hotel_{hotel}",
        f"depart_{to_slug(departure_city)}",
        "want_multi_city_route",
    }
    for key in optimized["ordered_destinations"]:
        initial_state.add(f"want_{key}")

    goal_state = {
        "destination_selected",
        "beach_activity_booked",
        "transport_reserved",
        "hotel_reserved",
        "itinerary_ready",
        "trip_confirmed",
    }

    actions = [
        Action("choose_destination", {"user_ready", "want_multi_city_route"}, {"destination_selected"}, set()),
        Action(
            "book_beach_activity",
            {"destination_selected", f"goal_{goal}"},
            {"beach_activity_booked"},
            set(),
        ),
        Action(
            "reserve_transport",
            {"destination_selected", f"prefer_{transport}", f"depart_{to_slug(departure_city)}"},
            {"transport_reserved"},
            set(),
        ),
        Action("reserve_hotel", {"destination_selected", f"hotel_{hotel}"}, {"hotel_reserved"}, set()),
        Action(
            "prepare_itinerary",
            {"beach_activity_booked", "transport_reserved", "hotel_reserved"},
            {"itinerary_ready"},
            set(),
        ),
        Action("confirm_trip", {"itinerary_ready"}, {"trip_confirmed"}, set()),
    ]

    return {
        "goal": goal,
        "budget": budget,
        "days": days,
        "transport": transport,
        "hotel": hotel,
        "departure_city": departure_city,
        "destination_key": optimized["ordered_destinations"][0],
        "destination": primary_destination["label"],
        "selected_destinations": optimized["ordered_destinations"],
        "route_label": route_label,
        "route_segments": optimized["segments"],
        "total_distance_km": optimized["total_distance_km"],
        "total_time_hours": optimized["total_time_hours"],
        "total_budget_inr": optimized["total_budget_inr"],
        "beach_activity": primary_destination["featured_activity"],
        "hotel_area": primary_destination["hotel_areas"].get(hotel, primary_destination["hotel_areas"]["standard"]),
        "initial_state": initial_state,
        "goal_state": goal_state,
        "actions": actions,
        "itinerary": itinerary,
        "guide_cards": all_guides,
        "places": primary_destination["places"],
        "food": primary_destination["food"],
        "experiences": primary_destination["experiences"],
    }
