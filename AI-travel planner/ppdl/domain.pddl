(define (domain travel-planner)
  (:requirements :strips)
  (:predicates
    (user_ready)
    (want_multi_city_route)
    (want_goa)
    (want_jaipur)
    (want_varanasi)
    (goal_relaxation)
    (prefer_train)
    (hotel_standard)
    (depart_chennai)
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
    :precondition (and (destination_selected) (goal_relaxation))
    :effect (and (beach_activity_booked))
  )

  (:action reserve_transport
    :precondition (and (destination_selected) (prefer_train) (depart_chennai))
    :effect (and (transport_reserved))
  )

  (:action reserve_hotel
    :precondition (and (destination_selected) (hotel_standard))
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
)