""" CSC111 Project 2: Flight Path Finder
============================================
This Python module contains the code for modified Vertex and Graph data classes. This will be used to represent a
a network of flights with the price and airline of each flight as well.

Copyright and Usage Information
============================================
This file is Copyright (c) Ashley Bi, Zhuoyi Jin, Elizabeth Liu, and Kerri Wei.
"""

from __future__ import annotations
from typing import Any, Optional
from scrape import get_results
from geopy.exc import GeocoderTimedOut
import networkx as nx
import matplotlib.pyplot as plt

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


# class Edge:
#     def __init__(self, start, destination, airline, baggage, price):
#         self.start = start
#         self.destination = destination
#         self.airline = airline
#         self.baggage = baggage
#         self.price = price
#
#     def __repr__(self):
#         return f"({self.start} -> {self.destination}, Airline: {self.airline}, Baggage: {self.baggage}, Price: {self.price})"


class WeightedGraph:
    """A graph used to represent a network of flights. Each vertex is representative of a location and each edge is
    representative of a flights with a unique initial location, destination, price, and airline.

    This is a directed graph, since we need to keep track of flights that occur in both directions (eg.
    Toronto to Vancouver versus Vancouver to Toronto). This graph is also a multigraph, since there may be multiple
    flights with the same route but with a different price or airline. Finally, this graph is also weighted since we
    keep track of the price of each flight.

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
            return any(flight_destination == initial_vertex_dest[0] for initial_vertex_dest in initial_vertex.destinations)
        else:
            return False

    def check_existing_flight_strict(self, flight_start: str, flight_destination: str, carry_on: bool, airline: str) -> bool:
        """Return whether there is a flight with the specified carry-on and airline from the given intial loaction to
        the given destination. This flight may be of any price.

        Return False if initial or destination do not appear as vertices in this graph.
        """
        if flight_start in self.vertices and flight_destination in self.vertices:
            initial_vertex = self.vertices[flight_start]
            return any((flight_destination == dest[0] and carry_on == dest[2] and airline == dest[3]) for dest in initial_vertex.destinations)
        else:
            return False

    def find_paths_strict(self, start: str, destination: str, price_limit: int, carry_on: bool, airline: str) -> dict:
        """Return all possible paths between start and destination with the specified carry on and airline
        specifications, and a total price that is less than or equal to price_limit."""
        # TODO: FINISH THIS FUNCTION!


    def initialize_with_airports(self, source: str, destination: str, start_date: str, end_date: str, airline: str = None, carry_on: bool = None):
        """Initialize the graph with flights between the specified international airports."""
        flights = get_results(source, destination, start_date, end_date)
        for flight in flights:
            if (not airline or flight['Airline'] == airline) and (carry_on is None or flight.get('Overhead', carry_on)):
                self.add_vertex(source)
                self.add_vertex(destination)
                self.add_edge(source, destination, flight['Price'], flight['Airline'])

    def recommend_airline(self, airline: str, source: str, destination: str, start_date: str, end_date: str)-> list[list[str]]:
        """Return a list of up to <limit> recommended airlines, price and time based on user input
        The return value is a list airlines associated with its price and time """
        recommended_flights = []
        flights = get_results(source, destination, start_date, end_date)

        for flight in flights:
            if self.check_existing_flight_strict(source, destination, True, airline):
                recommended_flights.append([flight['Airline'], flight['Price'], flight['Time']])

        return recommended_flights
    # just thkning about this, it should work.... BUt is also need carry_on??? comparing with user input


    def load_viewed_graph(self,  source: str, destination: str, start_date: str, end_date: str, price_limit: int, airline: str = None, carry_on: bool = None)-> WeightedGraph:
        """Return a airline review WEIGHTED graph corresponding to the given user inputs and the scarping of the data set.
        """
        flights = get_results(source, destination, start_date, end_date)

        weighted_graph = WeightedGraph()

        # 3. Add vertices representing
        for flight in flights:
            airline_per = flight['Airline']
            start_city = flight['Source']
            des_city = flight['Destination']
            price = flight['Price']

            weighted_graph.add_vertex(airline)
            weighted_graph.add_vertex(start_city)
            weighted_graph.add_vertex(destination_city)

            # 4. Find the closest flights
            paths = self.find_paths_strict(start_city, destination_city, price_limit, carry_on, airline)
            if paths:
                closest_flight = paths[:5]  # Select the closest 5 or 10 flight??
                # review_score = get_similarity_score(closest_flight)  # why is there an error here!!!
                weighted_graph.add_edge(start_city, des_city, airline_per)

        return weighted_graph

    def visualize_graph(self):
        """Visualize the weighted graph with predefined international airports in Canada."""
        G = nx.Graph()

        airports = {
            "Toronto": (43.7, -79.42),
            "Vancouver": (49.19, -123.18),
            "Montreal": (45.47, -73.74),
            "Calgary": (51.13, -114.01),
            "Ottawa": (45.42, -75.69),
            "Edmonton": (53.55, -113.49),
            "Halifax": (44.65, -63.57),
            "Winnipeg": (49.9, -97.23),
            "Quebec City": (46.81, -71.21),
            "Victoria": (48.43, -123.37)
        }

        for city, coordinates in airports.items():
            G.add_node(city, pos=coordinates)

        for city, vertex in self.vertices.items():
            for destination, weight, _ in vertex.destinations:
                G.add_edge(city, destination, weight=weight)

        pos = nx.get_node_attributes(G, 'pos')
        edge_labels = {(city, destination): weight for city, vertex in self.vertices.items() for destination, weight, _ in vertex.destinations}

        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=12, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
        plt.title('International Airports with Flights')
        plt.show()


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


#test
graph = WeightedGraph()
source_city = input("Enter the source city: ").strip().capitalize()
destination_city = input("Enter the destination city: ").strip().capitalize()
start_date = input("Enter the start date (YYYY/MM/DD): ").strip()
end_date = input("Enter the end date (YYYY/MM/DD): ").strip()

airline_preference = input("Enter airline preference (leave blank for all airlines): ").strip()
carry_on_preference = input("Carry-on baggage preference (yes/no): ").strip().lower() == 'yes'

# Initialize graph based on user input and flight results
graph.initialize_with_airports(source_city, destination_city, start_date, end_date, airline=airline_preference, carry_on=carry_on_preference)

graph.visualize_graph()

