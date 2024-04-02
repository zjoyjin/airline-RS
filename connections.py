from datetime import datetime, timedelta
from scrape import get_results

def get_connections(date: str, stops: list) -> list:
    """ Takes in first, last, and in-between stops. Returns cheapest sequence of flights.
    - date: yyyy/dd/mm
    """
    flight_path = []

    curr_date = date
    curr_start = stops[0]
    i = 1
    curr_stop = stops[i]

    while i != len(stops):
        flights = get_results(curr_start, curr_stop, date)
        cheapest = get_cheapest_flight(flights)
        cheapest['Date of Departure: '] = curr_date

        added_days = 0
        if '+' in cheapest['Arrival']:
            added_days = int(cheapest['Arrival'][-1])
        flight_path.append(cheapest)

        # Add one day to the current date using datetime
        year = int(date[:4])
        day = int(date[5:7])
        month = int(date[8:])
        temp_date = datetime(year, month, day)
        temp_date += timedelta(days=1 + added_days)
        curr_date = f'{temp_date.year}/{temp_date.day}/{temp_date.month}'

        i += 1
        if i < len(stops):
            curr_start, curr_stop = curr_stop, stops[i]

    return flight_path

def get_cheapest_flight(res: list[dict]) -> dict:
    """ Gets the cheapest flight from a given list of flight results. """
    cheapest = {"Price": 10000}
    for flight in res:
        if flight["Price"] < cheapest["Price"]:
            cheapest = flight

    return cheapest


# Testing!!
if __name__ == "__main__":
    res = get_connections("2024/20/04", ["Vancouver", "Toronto", "Edmonton"])
    if res:
        print(res)
    else:
        print("No flights found!")
