import requests
import os

AUTHORIZATION = f"BASIC {os.environ['SHEETY_AUTH']}"
ENDPOINT = f"{os.environ['SHEETY_EP_FLIGHTS']}/prices"
print(ENDPOINT)
class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}
        self.__sheety_header = {
            "Authorization": AUTHORIZATION
        }

    def get_destination_data(self):
        result = requests.get(url=ENDPOINT, headers=self.__sheety_header)
        result.raise_for_status()
        prices = result.json()
        self.destination_data = prices["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            url = f"{ENDPOINT}/{city['id']}"
            result = requests.put(url=url, json=new_data, headers=self.__sheety_header)
            result.raise_for_status()
