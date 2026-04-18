from pathlib import Path


def export_domain_pddl(problem):
    goal = problem["goal"]
    transport = problem["transport"]
    hotel = problem["hotel"]
    departure = problem["departure_city"].lower()
    selected = "\n".join(f"    (want_{key})" for key in problem["selected_destinations"])

    return f"""(define (domain travel-planner)
  (:requirements :strips)
  (:predicates
    (user_ready)
    (want_multi_city_route)
{selected}
    (goal_{goal})
    (prefer_{transport})
    (hotel_{hotel})
    (depart_{departure})
    (destination_selected)
    (beach_activity_booked)
    (transport_reserved)
    (hotel_reserved)
    (itinerary_ready)
    (trip_confirmed)
  )

  (:action choose_destination
    :precondition (and (user_ready) (want_multi_city_route))
    :effect (and (destination_selected))
  )

  (:action book_beach_activity
    :precondition (and (destination_selected) (goal_{goal}))
    :effect (and (beach_activity_booked))
  )

  (:action reserve_transport
    :precondition (and (destination_selected) (prefer_{transport}) (depart_{departure}))
    :effect (and (transport_reserved))
  )

  (:action reserve_hotel
    :precondition (and (destination_selected) (hotel_{hotel}))
    :effect (and (hotel_reserved))
  )

  (:action prepare_itinerary
    :precondition (and (beach_activity_booked) (transport_reserved) (hotel_reserved))
    :effect (and (itinerary_ready))
  )

  (:action confirm_trip
    :precondition (and (itinerary_ready))
    :effect (and (trip_confirmed))
  )
)"""


def export_problem_pddl(problem):
    goal = problem["goal"]
    transport = problem["transport"]
    hotel = problem["hotel"]
    departure = problem["departure_city"].lower()
    selected = "\n".join(f"    (want_{key})" for key in problem["selected_destinations"])

    return f"""(define (problem india-tour-plan)
  (:domain travel-planner)
  (:init
    (user_ready)
    (want_multi_city_route)
{selected}
    (goal_{goal})
    (prefer_{transport})
    (hotel_{hotel})
    (depart_{departure})
  )
  (:goal
    (and
      (destination_selected)
      (beach_activity_booked)
      (transport_reserved)
      (hotel_reserved)
      (itinerary_ready)
      (trip_confirmed)
    )
  )
)"""


def write_pddl_files(problem, folder="pddl"):
    path = Path(folder)
    path.mkdir(exist_ok=True)
    domain_text = export_domain_pddl(problem)
    problem_text = export_problem_pddl(problem)
    (path / "domain.pddl").write_text(domain_text, encoding="utf-8")
    (path / "problem.pddl").write_text(problem_text, encoding="utf-8")
    return domain_text, problem_text
