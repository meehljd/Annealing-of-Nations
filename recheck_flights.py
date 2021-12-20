# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import json
from datetime import datetime, timedelta
from utils.data_manager import DataManager
from utils.flight_search import FlightSearch

def save_json(object, flight_file):
    with open(flight_file, 'w') as outfile:
        json.dump(object, outfile, indent=2)

def recheck_flights(flight_file, geo_file):
    data_manager = DataManager()
    flight_search = FlightSearch()

    sheet_data = data_manager.get_destination_data()

    geo_data = {"country": [data["country"] for data in sheet_data],
                "city": [data["city"] for data in sheet_data],
                "airport": [data["iataCode"] for data in sheet_data],
                "latitude": [data["lat"] for data in sheet_data],
                "longitude": [data["long"] for data in sheet_data]}
    save_json(geo_data, geo_file)

    destinations = {
        data["iataCode"]: {
            "id": data["id"],
            "city": data["city"],
        } for data in sheet_data}

    origins = {data["iataCode"]: {} for data in sheet_data}
    print(origins)

    tomorrow = datetime.now() + timedelta(days=1)
    six_month_from_today = datetime.now() + timedelta(days=(3 * 30))

    for origination_code in origins:
        print(f'Starting {origination_code}')
        for destination_code in destinations:
            flight = flight_search.check_flights(
                origination_code,
                destination_code,
                from_time=tomorrow,
                to_time=six_month_from_today
            )
            if flight is None:
                continue

            origins[origination_code][destination_code] = flight.price
        print(origins)

    save_json(origins, flight_file)
    print(f'saved to {flight_file}')
    return origins
