import requests
import os
from flight_data import FlightData, SearchData
from pprint import pprint

TEQUILA_API_KEY = os.environ['TEQUILA_KEY']
TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"


class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def get_iata_codes(self, name):
        tequila_ep_query = f"{TEQUILA_ENDPOINT}/locations/query"
        tequila_params = {
            "apikey": TEQUILA_API_KEY,
            "term": name,
            "limit": 1,
        }
        response = requests.get(url=tequila_ep_query, params=tequila_params)
        response.raise_for_status()
        response_data = response.json()
        city_data = response_data["locations"][0]
        city_code = city_data["code"]
        return city_code

    def get_price(self, search_data: SearchData):
        tequila_ep_query = f"{TEQUILA_ENDPOINT}/v2/search"
        tequila_params = {
            "apikey": TEQUILA_API_KEY,
            "fly_from": search_data.departure_airport_code,
            "fly_to": search_data.arrival_airport_code,
            "date_from": search_data.date_from,
            "date_to": search_data.date_to,
            "nights_in_dst_from": search_data.min_duration,
            "nights_in_dst_to": search_data.max_duration,
            "flight_type": search_data.flight_type,
            "adults": search_data.adults,
            "curr": search_data.currency,
            "max_stopovers": search_data.max_stopovers,
            "sort": search_data.sort_by,
            "asc": search_data.cheapest_first,
        }
        # print(tequila_params)
        response = requests.get(url=tequila_ep_query, params=tequila_params)
        response.raise_for_status()
        response_data = response.json()
        flight_data = FlightData()
        num_flights = len(response_data["data"])
        if num_flights > 0:
            # print(response_data["data"][0])
            flight_data.act_price = response_data["data"][0]["price"]
            flight_data.act_depart_date = response_data["data"][0]["local_arrival"][:10]
            flight_data.act_return_date = response_data["data"][0]["local_departure"][:10]
            flight_data.act_depart_city = response_data["data"][0]["cityFrom"]
            flight_data.act_arrival_city = response_data["data"][0]["cityTo"]
            flight_data.act_depart_code = response_data["data"][0]["flyFrom"]
            flight_data.act_arrival_code = response_data["data"][0]["flyTo"]
        else:
            flight_data.act_price = 9999
        return flight_data
