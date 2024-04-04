""" CSC111 Project 2: Flight Path Finder
============================================
The Python module contains the code for functions that retrieve the cheapest flights for Project 2.

Copyright and Usage Information
============================================
This file is Copyright (c) Ashley Bi, Zhuoyi Jin, Elizabeth Liu, and Kerri Wei.
"""
from datetime import datetime, timedelta
from scrape import get_results


def get_connections(date: str, stops: list, recursive: bool = False, days: int = 0) -> list[dict]:
    """Returns cheapest sequence of flights between the cities in stops with at least a 1-day
    layover between flights.
       Calls either get_connections_iterative or get_connections_recursive, depending on `recursive` parameter.
        - date takes on the form YYYY/DD/MM.
        - stops is a list of city names. The first str is the starting city, the last str is the ending city.
        - recursive determines whether the recrusive or iterative version of the function is called.
        - days represents the number of days between arrival and departure, non-inclusive. Default 0.

        Preconditions:
        - len(stops) >= 2
        - days >= 0

         Returned dictionary's keys:
        - Departure: str (time)
        - Arrival: str (time)
        - Airline: str
        - Price: int
        - From: str (XYZ airport code)
        - To: str (XYZ airport code)
        - Date of Departure: str (YYYY/DD/MM)
    """
    if recursive:
        return _get_connections_recursive(date, stops, days)
    else:
        return _get_connections_iterative(date, stops, days)


def _get_connections_iterative(date: str, stops: list, days: int = 0) -> list[dict]:
    """
    Iteratively returns the "cheapest" sequence of flights between the cities in stops with at least a
    1-day layover between flights. Less accurate than the recursive implementation, but much faster.
        - date takes on the form YYYY/DD/MM.
        - stops is a list of city names. The first str is the starting city, the last str is the ending city.
        - days represents the number of days between arrival and departure, non-inclusive. Default 0.

        Preconditions:
        - len(stops) >= 2
        - days >= 0
    """
    flight_path = []

    curr_date = date
    curr_start = stops[0]
    i = 1
    curr_stop = stops[i]

    while i != len(stops):
        flights = get_results(curr_start, curr_stop, date)
        if len(flights) == 0:
            return []
        cheapest = get_cheapest_flight(flights)
        cheapest['Date of Departure'] = curr_date

        flight_path.append(cheapest)

        curr_date = _get_departure_date(curr_date, cheapest["Arrival"], days)
        i += 1
        if i < len(stops):
            curr_start, curr_stop = curr_stop, stops[i]

    return flight_path


def _get_connections_recursive(date: str, stops: list, days: int = 0) -> list:
    """
    Recursively returns the cheapest sequence of flights between the cities in stops with at least a
    1-day layover between flights. ACCURATE, but MUCH SLOWER than the iterative implemenation.
        - date takes on the form YYYY/DD/MM.
        - stops is a list of city names. The first str is the starting city, the last str is the ending city.
        - days represents the number of days between arrival and departure, non-inclusive. Default 0.

        Preconditions:
        - len(stops) >= 2
        - days >= 0
    """
    if len(stops) == 1:
        return []

    itinerary = [{"Price": 10**10}]
    for results in get_results(stops[0], stops[1], date):
        results['Date of Departure'] = date
        departure = _get_departure_date(date, results['Arrival'], days)

        possible_itinerary = [results] + _get_connections_recursive(departure, stops[1:], days)
        if sum((f["Price"] for f in possible_itinerary)) < sum((f["Price"] for f in itinerary)):
            itinerary = possible_itinerary

    if itinerary == [{"Price": 10**10}]:
        return []
    return itinerary


def _get_departure_date(arrival_date: str, arrival_time: str, days: int = 0) -> str:
    """
    Returns the expected date of departure of a flight following one with given
    `arrival_date` and `arrival_time`, with `days` in between the flights
    (default 0; i.e. returned date will be the day after initial arrival)
    Precondition:
        - days >= 0
    """
    stay = 1 + days
    if '+' in arrival_time:
        stay += int(arrival_time[-1])
    temp_date = datetime.strptime(arrival_date, "%Y/%d/%m")
    temp_date += timedelta(days=stay)

    return f'{temp_date.year}/{temp_date.day}/{temp_date.month}'


def get_cheapest_flight(flights: list[dict]) -> dict:
    """Returns the cheapest flight from a given list of flight results.
    Precondition:
        - len(flights) != 0
    """
    cheapest = {"Price": 10000}
    for flight in flights:
        if flight["Price"] < cheapest["Price"]:
            cheapest = flight

    return cheapest


# Testing!!
if __name__ == "__main__":
    # res = get_connections("2024/20/04", ["Vancouver", "Beijing", "San Francisco"], recursive=True)
    # if res:
    #     print(res)
    # else:
    #     print("No flights found!")

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ["datetime", "scrape"],  # the names (strs) of imported modules
        'allowed-io': [],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
