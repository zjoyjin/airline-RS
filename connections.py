from datetime import datetime
from scrape import get_results

def get_connections(first: dict, last: str, stops = list[set]):
    """ Takes in first, last, and in-between stops. Returns cheapest sequence of flights.
    """
    curr_date = datetime.strptime(first["Arrival"], '%m/%d/%y')
    a = first
    b = stops[1]
    while b != last:


def get_cheapest_flight(res: list[dict]) -> dict:
    """ Gets the cheapest flight from a given list of flight results. """
    cheapest = {"Price": 0}
    for flight in res:
        if flight["Price"] < cheapest["Price"]:
            cheapest = flight

    return flight