#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData, SearchData
from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

sheet_data = data_manager.get_destination_data()

if sheet_data[0]["iataCode"] == '':
    print("Adding IATA Codes")
    for row in sheet_data:
        row["iataCode"] = flight_search.get_iata_codes(row["city"])

    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

for row in sheet_data:
    search_data = SearchData(row)
    flight_data = flight_search.get_price(search_data)
    print(f"{search_data.arrival_city}: £{flight_data.act_price}")

    is_price_cheaper = flight_data.act_price < row["lowestPrice"]
    if is_price_cheaper:
        alert_message = f"Low price alert!" \
                        f"Only £{flight_data.act_price} to fly from " \
                        f"{flight_data.act_depart_city}-{flight_data.act_depart_code} to " \
                        f"{flight_data.act_arrival_city}-{flight_data.act_arrival_code}, from " \
                        f"{flight_data.act_depart_date} to {flight_data.act_return_date}."
        notification_manager.send_sms(alert_message)

