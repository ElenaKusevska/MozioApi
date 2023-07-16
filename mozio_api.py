# Module that contains classes with methods integrating the Mozio API

import requests

API_KEY = ""

class Search:

    def __init__(self, request_payload):
        self.request_payload = request_payload
        self.search_id = None
        self.started = False 
        self.start_exception = None
        self.results = []
        self.results_exception = None 
        

    def begin(self):
        url = "https://api-testing.mozio.com/v2/search/"
        headers =  {"API-KEY": API_KEY, "Content-Type": "application/json"}
        try:
            r = requests.post(url, headers=headers, json=self.request_payload)
            search_id = r.json()["search_id"]
        except Exception as e:
            self.start_exception = e 
            return

        self.search_id = search_id
        self.started = True
        return 


    def get_search_results(self):
        results = []
        try:
            more_coming = True
            nchecks = 0
            while more_coming == True and nchecks < 1000:
                url = f"https://api-testing.mozio.com/v2/search/{self.search_id}/poll/"
                headers =  {"API-KEY": API_KEY, "Content-Type": "application/json"}
                r = requests.get(url, headers=headers)
                for result in r.json()["results"]:
                    results.append(result)
                if r.json()["more_coming"] == False:
                    more_coming = False  
                nchecks = nchecks + 1
        except Exception as e:
            self.results_exception = e
            return

        self.results = results
        return


class Reservation:

    def __init__(self, booking_payload):
        self.booking_payload = booking_payload
        self.booked = False
        self.booking_exception = None
        self.status = None
        self.booking_id = None
        self.check_details()


    def book(self):
        if not self.booked:
            url = "https://api-testing.mozio.com/v2/reservations/"
            headers =  {"API-KEY": API_KEY, "Content-Type": "application/json"}
            try:
                r = requests.post(url, headers=headers, json=self.booking_payload)
                print(r.json())
                self.status = r.json()["status"]
            except Exception as e:
                self.booking_exception = e 
                return


    def check_details(self):
        url = f"https://api-testing.mozio.com/v2/reservations/{self.booking_payload['search_id']}/poll/"
        headers =  {"API-KEY": API_KEY, "Content-Type": "application/json"}
        try:
            r = requests.get(url, headers=headers)
            self.status = r.json()["status"]
            if self.status == "completed":
                self.booking_id = r.json()["reservations"][0]["id"]
                self.booked = True
        except Exception as e:
            self.booking_exception = e 
            return


    def cancel(self):
        url = f"https://api-testing.mozio.com/v2/reservations/{self.booking_id}"
        headers =  {"API-KEY": API_KEY, "Content-Type": "application/json"}
        try:
            r = requests.delete(url, headers=headers)
            if r.json()["cancelled"] == 1:
                self.status = "cancelled"
        except Exception as e:
            self.booking_exception = e 
            return






