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
            (initial city, destination city, flight price, airline, departure info, arrival info)
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
        """Initialize a new vertex with the given location.

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

    def load_user_graph(self, start_date: str, recursive: bool = False) -> None:
        """Load a graph visualization mapping out the user's flight path according to the user's input.
        Print the info for the cheapest flights between these corresponding locations.
        The flight info is retrieved from Google Flights."""

        # Read locations from airport.csv
        with open('airport.csv', 'r') as file:
            reader = csv.reader(file)
            locations = [row[0] for row in reader]

        flights = get_connections(start_date, locations, recursive=recursive)
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


    def draw_graph_from_user_input(self, m, airport_file, initial_location, locations_coord):
        """Draw the flights on a map using matplotlib."""
        with open(airport_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == initial_location:
                    latitude = float(row[3])
                    longitude = float(row[4])
                    locations_coord.append((latitude, longitude))

                    if len(locations_coord) > 1:
                        prev_coord = locations_coord[-2]
                        prev_latitude = prev_coord[0]
                        prev_longitude = prev_coord[1]
                        m.drawgreatcircle(prev_longitude, prev_latitude, longitude, latitude)

                    location_vertex = self.vertices[initial_location]
                    for destination in location_vertex.destinations:
                        destination_city_name = destination[1]
                        price = str(destination[2])
                        airline = destination[3]
                        departure_date = destination[4]
                        arrival_info = destination[5]
                        label = ("Take $" + price + " " + airline + " flight to " + destination_city_name + ". \n"
                                                                                                            "Departure at " + departure_date + " and arrival at " + arrival_info + ".")
                        plt.text(longitude, latitude, label, fontsize=5, ha='left', va='center')

                        self.draw_graph_from_user_input(m, airport_file, destination_city_name, locations_coord)

        plt.show()














if __name__ == '__main__':
    import mpl_toolkits.basemap as bm
    import matplotlib.pyplot as plt

    # Create an instance of the Graph class
    g = Graph()

    # Load the user's graph with the specified start date
    start_date = input("Enter the start date (YYYY/MM/DD): ")
    g.load_user_graph(start_date)

    # Create a Basemap instance
    m = bm.Basemap(llcrnrlon=-180, llcrnrlat=-90, urcrnrlon=180, urcrnrlat=90, projection='mill')

    # Draw the graph on the Basemap instance
    g.draw_graph_from_user_input(m, "airport.csv", g.vertices.keys()[0], [])

    # Show the plot
    plt.show()

