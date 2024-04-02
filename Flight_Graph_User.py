""" CSC111 Project 2: Flight Path Finder
============================================
This Python module contains the code for modified Vertex and Graph data classes. This will be used to represent a
a network of flights with the price and airline of each flight as well.

Copyright and Usage Information
============================================
This file is Copyright (c) Ashley Bi, Zhuoyi Jin, Elizabeth Liu, and Kerri Wei.
"""

from __future__ import annotations
from connections import get_connections
from typing import Union, Any, Optional
from datetime import datetime
from scrape import get_results
import networkx as nx
import matplotlib.pyplot as plt


class Vertex:
    """A vertex is a city that either has arriving or departing flights.

    Instance Attributes:
        - location: The name of the city
        - destinations: A set of tuples. Only add a tuple to this set if there exists a flight from self.location
            to another city. Each tuple stores the following information: (destination city, price of flights, airline, date).

    Representation Invariants:
        - all({self.location != destination[0] for destination in destinations})
        - len(self.destinations) != 0
    """
    location: Any
    destinations: set[tuple[str, Union[int, float], str, datetime]]

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


class Graph:
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

    def add_edge_date(self, initial: str, destination: str, price: Union[float, int], airline: str, date: str):
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
            edge_tuple = (initial, destination, price, airline, date)

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

    def load_viewed_user_graph(self, locations: list[str], start_date: str):
        """Initialize the graph with flights between the canadian airports."""
        flight = get_connections(start_date, locations)
        self.add_vertex(locations[0])

        for i in range(0, len(locations) - 1):
            self.add_vertex(locations[i + 1])
            self.add_edge_date(locations[i],locations[i + 1], flight[i]["Price"], flight[i]["Airline"], flight[i]["Date of Departure"]) #TODO, CHECK THIS THING

    def draw_graph(self):
        """Draw the graph using NetworkX and Matplotlib."""
        G = nx.Graph()

        #TODO: add a forloop here
        for initial, vertex in self.vertices.items():
            G.add_node(initial)

        for initial, vertex in self.vertices.items():
            for dest_tuple in vertex.destinations:
                dest, price, airline, date = dest_tuple
                G.add_edge(initial, dest, weight=price, airline=airline, date=date)

        # for initial, vertex in self.vertices.items():
        #     for dest_tuple in vertex.destinations:
        #         dest, price, airline, date = dest_tuple
        #         G.add_edge(initial, dest, weight=price, airline=airline, date=date)

        pos = nx.spring_layout(G)
        labels = {(start, end): f"{airline}\n${price}\n{date}" for start, end, price, airline, date in
                  G.edges.data('weight', 'airline', 'date')}
        nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.title('Graph of Cities with Flights')
        plt.show()


