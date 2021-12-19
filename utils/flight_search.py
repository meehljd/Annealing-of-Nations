import requests
from utils.flight_data import FlightData
import os
import pprint

TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"
TEQUILA_API_KEY = os.environ['TEQUILA_KEY']


def search_flights(query):
    headers = {"apikey": TEQUILA_API_KEY}
    return requests.get(
        url=f"{TEQUILA_ENDPOINT}/v2/search",
        headers=headers,
        params=query,
    )


class FlightSearch:

    def get_destination_code(self, city_name):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {"apikey": TEQUILA_API_KEY}
        query = {"term": city_name, "location_types": "city"}
        response = requests.get(url=location_endpoint, headers=headers, params=query)
        results = response.json()["locations"]
        code = results[0]["code"]
        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "flight_type": "oneway",
            "one_for_city": 1,
            "max_stopovers": 2,
            "curr": "USD"
        }

        response = search_flights(query)
        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"({origin_city_code}) to "
                  f"({destination_city_code}): "
                  f"No Flights Available")
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][-1]["cityTo"],
                destination_airport=data["route"][-1]["flyTo"],
                #out_date=data["route"][0]["local_departure"].split("T")[0],
                #return_date=data["route"][1]["local_departure"].split("T")[0]
                stop_overs=len(data['routes']),
                #via_city=data["route"][0]["cityTo"]
            )
            print(f"{flight_data.origin_city} ({flight_data.origin_airport}) to "
                  f"{flight_data.destination_city} ({flight_data.destination_airport}): "
                  f"${flight_data.price}")
            return flight_data
