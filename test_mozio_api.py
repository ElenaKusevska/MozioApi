# Program to test the mozio API integration
# And solve the exercise

import time

from mozio_api import Search, Reservation


# Start a search:
search_data = {"start_address": "44 Tehama Street, San Francisco, CA, USA", 
        "end_address": "SFO",
        "mode": "one_way",
        "pickup_datetime": "2023-12-01 15:30",
        "num_passengers": 2,
        "currency": "USD",
        "campaign": "{your full name}"
        }

my_search = Search(search_data)
my_search.begin()

# Find desired result:
if my_search.started:
    my_search.get_search_results()

    if my_search.results:
        prices = []
        result_ids = []
        for poll in my_search.results:
            for step in poll["steps"]:
                if step["details"]["provider_name"] == "Dummy External Provider":
                    prices.append(float(poll["total_price"]["total_price"]["value"]))
                    result_ids.append(poll["result_id"])

        min_price_index = prices.index(min(prices))
        result_id = result_ids[min_price_index]

        # make_reservation:
        booking_payload = {
                "search_id": my_search.search_id,
                "result_id": result_id,
                "email": "elena@google.com",
                "airline": "AA",
                "flight_number": "123",
                "phone_number": "+14126545542",
                "first_name": "Elena",
                "last_name": "K"}

        my_reservation = Reservation(booking_payload)
        my_reservation.book()

        # Check that reservation has been completed:
        nchecks = 0
        while my_reservation.status != "completed" and nchecks < 20:
            my_reservation.check_details()
            nchecks = nchecks + 1
            time.sleep(1)
            

        print("booking id", my_reservation.booking_id)

        # Cancel rwawrvation:
        my_reservation.cancel()
        print(my_reservation.status)

    else:
        print("Error with search results")

else:
    print("Error, search not started")


