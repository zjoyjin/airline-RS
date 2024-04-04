""" CSC111 Project 2: Flight Path Finder
============================================
This Python module contains the code for modified Vertex and Graph data classes. This will be used to represent a
a network of flights with the price and airline of each flight as well.

Copyright and Usage Information
============================================
This file is Copyright (c) Ashley Bi, Zhuoyi Jin, Elizabeth Liu, and Kerri Wei.
"""

from __future__ import annotations
from typing import Union, Any, Optional
from datetime import datetime
from scrape import get_results
import networkx as nx
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import csv


class Vertex:
    """A vertex is a city that either has arriving or departing flights.

    Instance Attributes:
        - location: The name of the city
        - destinations: A set of tuples. Only add a tuple to this set if there exists a flight from self.location
            to another city. Each tuple stores the following information: (destination city, price of flights, airline).

    Representation Invariants:
        - all({self.location != destination[0] for destination in destinations})
        - len(self.destinations) != 0
    """
    location: Any
    destinations: set[tuple[str, Union[int, float], str]]

    def __init__(self, location: str):
        """Initialize a new vertex with the given lcocation.

        This vertex is initialized with no neighbours.
        """
        self.location = location
        self.destinations = set()

    def __repr__(self):
        return f"{self.location}"

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.destinations)


class GraphAll:
    """A graph used to represent a network of flights. Each vertex is representative of a location and each edge is
    representative of a flights with initial location, destination, cheapest price, and airline.

    This is a directed graph, since we need to keep track of flights that occur in both directions (eg.
    Toronto to Vancouver versus Vancouver to Toronto). Finally, this graph is showing the cheapest flight available.

    Instance Attributes:
         - vertices:
             A collection of the vertices contained in this graph.
             Maps city name to Vertex object
    """
    vertices: dict[str, Vertex]

    def __init__(self):
        """Initialize an empty graph (no vertices or edges)."""
        self.vertices = {}

    def add_vertex(self, location: str):
        """Add a vertex with the given city name, price, and airline to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.
        """
        if location not in self.vertices:
            self.vertices[location] = Vertex(location)

    def add_edge(self, initial: str, destination: str, price: Union[float, int], airline: str):
        """Add an edge between the vertex for an initial location in this graph and a destination. Note that only
        self.vertices[initial].destinations will be modified, since vertex.destinations for any vertex only stores flights
        that depart from the location, and does not store flights that arrive at the location.

        Raise a ValueError if initial or destination do not appear as vertices in this graph.

        Do nothing if this edge already exists.

        Preconditions:
            - item1 != item2
        """
        if initial not in self.vertices or destination not in self.vertices:
            raise ValueError
        else:
            initial_vertex = self.vertices[initial]
            edge_tuple = (destination, price, airline)

            if edge_tuple not in initial_vertex.destinations:
                initial_vertex.destinations.add(edge_tuple)

    def get_vertex(self, location):
        """Return the Vertex object associated with the given location.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if location in self.vertices:
            return self.vertices[location]
        else:
            raise ValueError

    def check_existing_flight_any(self, flight_start: str, flight_destination: Any) -> bool:
        """Return whether there is a flight from the given intial loaction to the given destination. This flight may be
        of any price or airline and does not consider whether there is carry-on or no carry-on.

        Return False if initial or destination do not appear as vertices in this graph.
        """
        if flight_start in self.vertices and flight_destination in self.vertices:
            initial_vertex = self.vertices[flight_start]
            return any(
                flight_destination == initial_vertex_dest[0] for initial_vertex_dest in initial_vertex.destinations)
        else:
            return False

    # def airport_add_edge(self, start_city: str, start_date: datetime, destination: str):
    #     """Initialize the graph with flights between the canadian airports."""
    #     flights = get_results(start_city, destination, start_date)
    #     for flight in flights:
    #             self.add_vertex(start_city)
    #             self.add_vertex(destination)
    #             self.add_edge(start_city, destination, flight['Price'], flight['Airline'])

    def load_flights_graph(self, start_date: str, airport_file: str, locations: list[str]) -> None:
        """Initialize a graph with flights between the Canadian airports.
        """
        city_list = []
        with open(airport_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == locations[0]:
                    city_list += [row[0]]
                    break


        for initial_city in city_list:
            for destination_city in city_list:
                if initial_city != destination_city:
                    flight = get_results(destination_city, initial_city, start_date)
                    price = flight[initial_city]["Price"]
                    airline = flight[initial_city]["Airline"]  #
                    # reAD FLIGHT FOR THE PRICE AND AIRLINE

                    self.add_vertex(initial_city)
                    self.add_vertex(destination_city)

                    self.add_edge(initial_city, destination_city, price, airline)

    def draw_graph_matplot_all(self, airport_file: str, locations: list[str]):
        """Draw the flights on a map using matplotlib."""
        # set background and map colors
        bg_color = (1.0, 1.0, 1.0, 1.0)
        coast_color = (10.0 / 255.0, 10.0 / 255.0, 10 / 255.0, 0.8)
        m = Basemap(llcrnrlon=-139.808215, llcrnrlat=41.508585, urcrnrlon=-41.425033, urcrnrlat=83.335074)
        m.drawcoastlines(color=coast_color)
        m.fillcontinents(color=bg_color, lake_color=bg_color)
        m.drawmapboundary(fill_color=bg_color)
        locations_coord = []
        # find the coordinates for the first city in locations with airport_fill
        # find the coordinates for the first city in locations with airport_file
        with open(airport_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == locations[0]:
                    latitude = float(row[3])
                    longitude = float(row[4])
                    locations_coord += [(latitude, longitude)]
                    break

        for i in range(1, len(locations)):
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
                        break

        # airline = get_connections(locations[i]["Airline"])    # Draw nodes
        # money = get_connections(locations[i]["Price"])    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue', label=True)
        # date = get_connections(locations[i], locations[i])
        #     # Draw edges
        # plt.annotate(f"{airline}, {money}, {date}")    nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, arrows=True)


        plt.show()
        # edge_labels = {(u, v): f"{d['weight']}, {d['airline']}" for u, v, d in G.edges(data=True)}



#  # Load the weighted graph
#         graph = WeightedGraph()
#         graph.load_viewed_graph()
#
#         # Visualize the graph
#         graph.visualize_graph()


# def visualize_graph(self):
#     # Create a directed graph
#     G = nx.DiGraph()
#
#     # Add nodes (airports) to the graph
#     for airport in self.vertices:
#         G.add_node(airport)
#
#     # Add edges (flights) to the graph
#     for airport, vertex in self.vertices.items():
#         for destination, price, airline in vertex.destinations:
#             G.add_edge(airport, destination, price=price, airline=airline)
#
#     # Plot the graph
#     plt.figure(figsize=(12, 8))
#     pos = nx.spring_layout(G)  # Positions for all nodes
#
#     # Draw nodes
#     nx.draw_networkx_nodes(G, pos, node_size=700, node_color='skyblue')
#
#     # Draw edges
#     nx.draw_networkx_edges(G, pos, width=2, alpha=0.5, edge_color='gray')
#
#     # Draw labels (airport codes)
#     nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')
#
#     # Draw edge labels (prices)
#     edge_labels = {(u, v): f"${d['price']}" for u, v, d in G.edges(data=True)}
#     nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
#
#     # Set plot title and display the graph
#     plt.title('Flight Routes')
#     plt.axis('off')  # Turn off axis
#     plt.show()


# def get_edges(self, vertex):
#     if isinstance(vertex, Vertex):
#         return self.edges[vertex.name]
#     else:
#         raise ValueError("Invalid vertex")


# Creating graph
# graph = Graph()

# Reading data from CSV file
# with open('flights.csv', 'r') as file:
#     csv_reader = csv.reader(file)
#     next(csv_reader)  # Skip header
#     for row in csv_reader:
#         start = Vertex(row[0])
#         destination = Vertex(row[1])
#         airline = row[4]
#         baggage = row[2]
#         price = int(row[3])

#         graph.add_vertex(start)
#         graph.add_vertex(destination)
#         graph.add_edge(Edge(start, destination, airline, baggage, price))

# res = get_results()
# for flight in res:
#     start = flight['_to']
#     destination = flight['_from']
#     departure = flight['departure']
#     arrival = flight['arrival']
#     price = flight['Price']
#     airline = flight['Airline']

#     # baggage = flight['Carry-on']

#     graph.add_vertex(start)
#     graph.add_vertex(destination)
#     graph.add_edge(start, destination, price, airline)

#
# def get_similarity_score(self, flight_start: str, flight_destination: str, price: float) -> float:
#     """Return a similarity score between the user input (source and destination cities, price range)
#     and the given flight.
#
#     The similarity score is calculated based on the closeness of the flight's start city, end city,
#     and price to the user's input.
#
#     Preconditions:
#         - flight_start and flight_destination are valid city names.
#         - price is a non-negative float representing the flight's price.
#     """
#     similarity_score = 0.0
#
#     if flight_start.lower() == self.user_start.lower(): #doesn't even make sense uhhhhh
#         similarity_score += 1.0
#
#     if flight_destination.lower() == self.user_end.lower():
#         similarity_score += 1.0
#
#     price_difference = abs(price - self.user_price)
#     if price_difference <= self.price_range:
#         similarity_score += 1.0 - (price_difference / self.price_range)
#
#     return similarity_score
# #how do i get the user input here?


# #test
# CITIES = { "Toronto", "Vancouver", "Montreal","Calgary","Ottawa","Edmonton","Halifax","Winnipeg","Quebec City","Victoria"}
#
# graph = WeightedGraph()
# source_city = input("Enter the source city: ").strip().capitalize()
# destination_city = input("Enter the destination city: ").strip().capitalize()
# start_date = input("Enter the start date (YYYY/MM/DD): ").strip()
# end_date = input("Enter the end date (YYYY/MM/DD): ").strip()
#
# airline_preference = input("Enter airline preference (leave blank for all airlines): ").strip()
# carry_on_preference = input("Carry-on baggage preference (yes/no): ").strip().lower() == 'yes'
#
# # Initialize graph based on user input and flight results
# # for source_city in CITIES:
# #     for destination_city in CITIES:
# #         graph.initialize_with_airports(source_city, destination_city, start_date, end_date, airline=airline_preference, carry_on=carry_on_preference)
# graph.initialize_with_airports(source_city, destination_city, start_date, end_date, airline=airline_preference, carry_on=carry_on_preference)
# graph.visualize_graph(airline_preference, source_city, destination_city, start_date, end_date)
