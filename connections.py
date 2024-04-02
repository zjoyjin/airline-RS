from datetime import datetime
from datetime import timedelta
from scrape import get_results

def get_connections(first: str, last: str, date: str, stops: list):
    """ Takes in first, last, and in-between stops. Returns cheapest sequence of flights.
    - date: yyyy/mm/dd
    """
    flight_path = []

    curr_date = date
    curr_start = first
    i = 1
    curr_stop = stops[i]

    while i != len(stops):
        flights = get_results(curr_start, curr_stop, date)
        flight_path.append(get_cheapest_flight(flights))

        # Add one day to the current date using datetime
        year = int(date[:4])
        month = int(date[5:7])
        day = int(date[8:])
        temp_date = datetime(year, month, day)
        temp_date += timedelta(days=1)
        curr_date = f'{temp_date.year}/{temp_date.month}/{temp_date.day}'

        i += 1
        curr_start, curr_stop = curr_stop, stops[i]

    return flight_path

def get_cheapest_flight(res: list[dict]) -> dict:
    """ Gets the cheapest flight from a given list of flight results. """
    cheapest = {"Price": 0}
    for flight in res:
        if flight["Price"] < cheapest["Price"]:
            cheapest = flight

    return cheapest
