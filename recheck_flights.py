# This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
import json
from datetime import datetime, timedelta
from utils.data_manager import DataManager
from utils.flight_search import FlightSearch
from utils.notification_manager import NotificationManager

def save_json(object, flight_file):
    json_object = json.dumps(object)
    with open(flight_file, 'w') as outfile:
        outfile.write(json_object)

def recheck_flights(flight_file):
    data_manager = DataManager()
    flight_search = FlightSearch()
    notification_manager = NotificationManager()

    sheet_data = data_manager.get_destination_data()

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

    save_json(object, flight_file)
    return origins