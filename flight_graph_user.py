""" CSC111 Project 2: Flight Path Finder
============================================
This Python module contains the code for modified Vertex and Graph data classes. This will be used to represent a
a network of flights with the price and airline of each flight as well.

Copyright and Usage Information
============================================
This file is Copyright (c) Ashley Bi, Zhuoyi Jin, Elizabeth Liu, and Kerri Wei.
"""

from __future__ import annotations
from typing import Any
import csv
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from connections import get_connections


class Vertex:
    """A vertex is a city that either has arriving or departing flights.

    Instance Attributes:
        - location: The name of the city
        - destinations: A set of tuples. Only add a tuple to this set if there exists a flight from self.location
            to another city. Each tuple stores the following information:
            (initial city, destination city, flight price, airline, depature info, arrival info)
            - departure info is a str in the form: "<YYYY/DD/MM> at <time of departure> from <XYZ>"
            - arrival info is a str in the form: "<time of arrival> at <XYZ>"
            - Note: XYZ is the airport code

    Representation Invariants:
        - all({self.location != destination[0] for destination in destinations})
        - len(self.destinations) != 0
    """
    location: Any
    destinations: set[tuple[str, str, Any, Any, str, str]]

    def __init__(self, location: str) -> None:
        """Initialize a new vertex with the given lcocation.

        This vertex is initialized with no neighbours.
        """
        self.location = location
        self.destinations = set()

    def __repr__(self) -> str:
        return f"{self.location}"

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.destinations)


class Graph:
    """A graph used to represent a collection of flights. Each vertex is representative of a location
    Each edge is representative of a flight, and contains the info about the flight. This includes the
    initial location, destination, departure info (date, time, airport code), arrival info (time, airport code),
    price, and airline.

    Instance Attributes:
         - vertices:
             A collection of the vertices contained in this graph.
             Maps city name to Vertex object
    """
    vertices: dict[str, Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self.vertices = {}

    def add_vertex_user(self, location: str) -> None:
        """Add a vertex with the given city name.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.
        """
        if location not in self.vertices:
            self.vertices[location] = Vertex(location)

    def add_edge_user(self, initial: str, destination: str, flight: dict) -> None:
        """Add an edge between the vertex for an initial location in this graph to one of the
        user's desired destinations. Note that only self.vertices[initial].destinations will be modified,
        since vertex.destinations for any vertex only stores flights that depart from the location,
        and does not store flights that arrive at the location.

        Raise a ValueError if initial or destination do not appear as vertices in this graph.

        Do nothing if this edge already exists.

        Preconditions:
            - item1 != item2
        """
        if initial not in self.vertices or destination not in self.vertices:
            raise ValueError
        else:
            initial_vertex = self.vertices[initial]
            price = flight["Price"]
            airline = flight["Airline"]
            departure = f'{flight["Date of Departure"]} at {flight["Departure"]} from {flight["From"]}'
            arrival = f'{flight["Arrival"]} at {flight["To"]}'
            flight_info = (initial, destination, price, airline, departure, arrival)

            if flight_info not in initial_vertex.destinations:
                initial_vertex.destinations.add(flight_info)

    def get_vertex(self, location: str) -> Vertex:
        """Return the Vertex object associated with the given location.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if location in self.vertices:
            return self.vertices[location]
        else:
            raise ValueError

    def load_user_graph(self, locations: list[str], start_date: str) -> None:
        """Load a graph visualization mapping out the user's flight path according to the user's input.
        Print the info for the cheapest flights between these corresponding locations.
        The flight info is retrieved from Google Flights."""
        flights = get_connections(start_date, locations)
        self.add_vertex_user(locations[0])

        for i in range(0, len(locations) - 1):
            self.add_vertex_user(locations[i + 1])

            price = flights[i]["Price"]
            airline = flights[i]["Airline"]
            departure_date = flights[i]["Date of Departure"]
            departure_time = flights[i]["Departure"]
            arrival_time = flights[i]["Arrival"]
            start_airport = flights[i]["From"]
            end_airport = flights[i]["To"]

            self.add_edge_user(locations[i], locations[i + 1], flights[i])

            # Print each flight's details
            print(f'Flight {i + 1}: Price: ${price}, Airline: {airline}')
            print(f'Departure: {departure_date} at {departure_time} from {start_airport}, '
                  f'Arrival: {arrival_time} at {end_airport} \n')

        def draw_graph_from_user_input(self, m: Basemap, airport_file: str, locations: list[str]):
            """Draw the flights on a map using matplotlib.
            >>> bg_color = (1.0, 1.0, 1.0, 1.0)
            >>> coast_color = (10.0 / 255.0, 10.0 / 255.0, 10 / 255.0, 0.8)
            >>> m = Basemap(llcrnrlon=-139.808215, llcrnrlat=41.508585, urcrnrlon=-41.425033, urcrnrlat=83.335074)
            >>> m.drawcoastlines(color=coast_color)
            >>> m.fillcontinents(color=bg_color, lake_color=bg_color)
            >>> m.drawmapboundary(fill_color=bg_color)
            >>> g = Graph()
            >>> g.add_vertex_user("Vancouver")
            >>> g.add_vertex_user("Calgary")
            >>> g.add_vertex_user("Fort Mcmurray")
            >>> g.add_vertex_user("Montreal")
            >>> g.add_vertex_user("Toronto")
            >>> g.vertices["Vancouver"].destinations.add(("V", "Calgary", "300", "Air Canada", "2024/04/04", "arrival"))
            >>> g.vertices["Calgary"].destinations.add(("C", "Fort Mcmurray", "400", "WestJet", "2024/05/04", "Arrival"))
            >>> g.vertices["Fort Mcmurray"].destinations.add(("FM", "Montreal", "300", "airline", "40404040", "arrival"))
            >>> g.vertices["Montreal"].destinations.add(("Montreal", "Toronto", "300", "airline", "40404040", "arrival"))
            >>> g.draw_graph_from_user_input(m, "airport.csv", ["Vancouver", "Calgary", "Fort Mcmurray", "Montreal", "Toronto"])"""

            locations_coord = []  # this is a list that keeps tracks of coordinates

            with open(airport_file, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == locations[0]:
                        latitude = float(row[3])
                        longitude = float(row[4])
                        locations_coord += [(latitude, longitude)]
                        break

            location_vertex = self.vertices[locations[0]]
            for destination in location_vertex.destinations:
                price = str(destination[2])
                airline = destination[3]
                departure_date = destination[4]
                arrival_info = destination[5]
                label = ("$" + price + " " + airline + "\n"
                                                       " flight to " + locations[
                             1] + ". \nDeparture at " + departure_date + "\n"
                                                                         " and arrival at " + arrival_info + ".")
                plt.text(longitude, latitude, label, fontsize=5, ha='left', va='center')

            # find coordinates of each city (other than the first one) in locations with airport_file
            for i in range(1, len(locations) - 1):
                with open(airport_file, 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        if row[0] != locations[i]:
                            continue
                        else:
                            latitude = float(row[3])
                            longitude = float(row[4])
                            locations_coord += [(latitude, longitude)]

                            prev_latitude = locations_coord[i - 1][0]
                            prev_longitude = locations_coord[i - 1][1]
                            m.drawgreatcircle(prev_longitude, prev_latitude, longitude, latitude)

                            location_vertex = self.vertices[locations[i]]
                            for destination in location_vertex.destinations:
                                price = str(destination[2])
                                airline = destination[3]
                                departure_date = destination[4]
                                arrival_info = destination[5]
                                label = ("$" + price + " " + airline + "\n"
                                                                       " flight to " + locations[
                                             i + 1] + ". \nDeparture at " + departure_date + "\n"
                                                                                             " and arrival at " + arrival_info + ".")
                                plt.text(longitude, latitude, label, fontsize=5, ha='left', va='center')

            with open(airport_file, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == locations[len(locations) - 1]:
                        latitude = float(row[3])
                        longitude = float(row[4])
                        locations_coord += [(latitude, longitude)]

                        prev_latitude = locations_coord[len(locations) - 2][0]
                        prev_longitude = locations_coord[len(locations) - 2][1]
                        m.drawgreatcircle(prev_longitude, prev_latitude, longitude, latitude)

            plt.show()
    # def draw_graph_matplot(self, airport_file: str, locations: list[str]):
    #     """Draw the flights on a map using matplotlib."""
    #     # set background and map colors
    #     bg_color = (1.0, 1.0, 1.0, 1.0)
    #     coast_color = (10.0 / 255.0, 10.0 / 255.0, 10 / 255.0, 0.8)
    #
    #     m = Basemap(llcrnrlon=-139.808215, llcrnrlat=41.508585, urcrnrlon=-41.425033, urcrnrlat=83.335074)
    #     m.drawcoastlines(color=coast_color)
    #     m.fillcontinents(color=bg_color, lake_color=bg_color)
    #     m.drawmapboundary(fill_color=bg_color)
    #
    #     locations_coord = []  # this is a list that keeps tracks of coordinates
    #
    #     # find the coordinates for the first city in locations with airport_file
    #     with open(airport_file, 'r') as file:
    #         reader = csv.reader(file)
    #         for row in reader:
    #             if row[0] == locations[0]:
    #                 latitude = float(row[3])
    #                 longitude = float(row[4])
    #                 locations_coord += [(latitude, longitude)]
    #                 break
    #
    #     # find coordinates of each city (other than the first one) in locations with airport_file
    #     for i in range(1, len(locations)):
    #         with open(airport_file, 'r') as file:
    #             reader = csv.reader(file)
    #             for row in reader:
    #                 if row[0] != locations[i]:
    #                     continue
    #                 else:
    #                     latitude = float(row[3])
    #                     longitude = float(row[4])
    #                     locations_coord += [(latitude, longitude)]
    #
    #                     prev_latitude = locations_coord[i - 1][0]
    #                     prev_longitude = locations_coord[i - 1][1]
    #                     m.drawgreatcircle(prev_longitude, prev_latitude, longitude, latitude)
    #                     break

        plt.show()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['csv', 'mpl_toolkits.basemap', 'matplotlib.pyplot', 'connections'],
        'allowed-io': ['load_user_graph', 'draw_graph_from_user_input'],
        'max-line-length': 120
    })
