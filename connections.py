""" CSC111 Project 2: Flight Path Finder
============================================
The Python module contains the code for functions that retrieve the cheapest flights for Project 2.

Copyright and Usage Information
============================================
This file is Copyright (c) Ashley Bi, Zhuoyi Jin, Elizabeth Liu, and Kerri Wei.
"""
from datetime import datetime, timedelta
from scrape import get_results


def get_connections(date: str, stops: list) -> list[dict]:
    """Returns cheapest sequence of flights between the cities in stops with a 1-day layover between flights.
        - date takes on the form YYYY/DD/MM.
        - stops is a list of city names. The first str is the starting city, the last str is the ending city.

        Representation Invariants:
        - len(stops) >= 2

         Returned dictionary's keys:
        - Departure: str (time)
        - Arrival: str (time)
        - Airline: str
        - Price: int
        - From: str (XYZ airport code)
        - To: str (XYZ airport code)
        - Date of Departure: str (YYYY/DD/MM)
    """
    flight_path = []

    curr_date = date
    curr_start = stops[0]
    i = 1
    curr_stop = stops[i]

    while i != len(stops):
        flights = get_results(curr_start, curr_stop, date)
        cheapest = get_cheapest_flight(flights)
        cheapest['Date of Departure'] = curr_date

        # Check if flight lands during the next day (from departure day)
        added_days = 0
        if '+' in cheapest['Arrival']:
            added_days = int(cheapest['Arrival'][-1])
        flight_path.append(cheapest)

        # Add one day to the current date using datetime (and any other additional days from last flight)
        temp_date = datetime.strptime(date, "%Y/%d/%m")
        temp_date += timedelta(days=1 + added_days)
        curr_date = f'{temp_date.year}/{temp_date.day}/{temp_date.month}'

        i += 1
        if i < len(stops):
            curr_start, curr_stop = curr_stop, stops[i]

    return flight_path


def get_cheapest_flight(flights: list[dict]) -> dict:
    """Returns the cheapest flight from a given list of flight results."""
    cheapest = {"Price": 10000}
    for flight in flights:
        if flight["Price"] < cheapest["Price"]:
            cheapest = flight

    return cheapest


# Testing!!
if __name__ == "__main__":
    res = get_connections("2024/20/04", ["Vancouver", "Hong Kong","Beijing", "San Francisco"])
    if res:
        print(res)
    else:
        print("No flights found!")
