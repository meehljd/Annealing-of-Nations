from datetime import datetime, timedelta

HOME_CODE = "LON"
HOME_CITY = "London"
DATE_FORMAT = "%d/%m/%Y"


def get_from_date():
    today = datetime.today()
    from_date = today + timedelta(days=1)
    return from_date.strftime(DATE_FORMAT)


def get_to_date():
    today = datetime.today()
    from_date = today + timedelta(days=6*30)
    return from_date.strftime(DATE_FORMAT)


# TODO I should split into two classes: SearchData and FlightData
class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self):
        self.act_depart_date = ""
        self.act_return_date = ""
        self.act_depart_city = ""
        self.act_return_city = ""
        self.act_depart_code = ""
        self.act_return_code = ""


class SearchData:
    # This class is responsible for structuring the flight data.
    def __init__(self, city_data):
        self.departure_airport_code = HOME_CODE
        self.departure_city = HOME_CITY
        self.arrival_airport_code = city_data["iataCode"]
        self.arrival_city = city_data["city"]
        self.date_from = get_from_date()
        self.date_to = get_to_date()
        self.min_duration = 7
        self.max_duration = 28
        self.flight_type = "round"
        self.adults = 1
        self.currency = "GBP"
        self.max_stopovers = 0
        self.sort_by = "price"
        self.cheapest_first = 1
