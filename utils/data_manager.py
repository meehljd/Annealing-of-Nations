from pprint import pprint
import requests
import os

AUTHORIZATION = f"BASIC {os.environ['SHEETY_AUTH']}"
SHEETY_ENDPOINT = f"{os.environ['SHEETY_EP_ANNEALING']}"

class DataManager:

    def __init__(self):
        self.destination_data = {}
        self.__sheety_header = {
            "Authorization": AUTHORIZATION
        }

    def get_data(self, sheet):
        response = requests.get(url=f"{SHEETY_ENDPOINT}/{sheet}", headers=self.__sheety_header)
        data = response.json()
        sheet_data = data[sheet]
        return sheet_data

    def get_destination_data(self):
        return self.get_data("airports")

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "airports": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data,
                headers=self.__sheety_header
            )
            print(response.text)
