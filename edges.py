"""
This is the Classes and Function for Vertex and graph
"""

from __future__ import annotations
from typing import Any, Optional
from scrape import get_results

class Vertex:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.name}"


class Edge:
    def __init__(self, start, destination, airline, baggage, price):
        self.start = start
        self.destination = destination
        self.airline = airline
        self.baggage = baggage
        self.price = price

    def __repr__(self):
        return f"({self.start} -> {self.destination}, Airline: {self.airline}, Baggage: {self.baggage}, Price: {self.price})"


class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = {}

    def add_vertex(self, vertex):
        if isinstance(vertex, Vertex) and vertex.name not in self.vertices:
            self.vertices[vertex.name] = vertex
            self.edges[vertex.name] = []

    def add_edge(self, edge):
        if isinstance(edge, Edge):
            if edge.start in self.vertices and edge.destination in self.vertices:
                self.edges[edge.start].append(edge)
            else:
                raise ValueError

    def get_vertex(self, name):
        if name in self.vertices:
            return self.vertices[name]
        else:
            raise ValueError

    def get_edges(self, vertex):
        if isinstance(vertex, Vertex):
            return self.edges[vertex.name]
        else:
            raise ValueError("Invalid vertex")


# Creating graph
graph = Graph()

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

res = get_results()
for flight in res:
    start = Vertex(flight['To'])
    destination = Vertex(flight['From'])
    airline = flight['Airline']
    price = flight['Price']
    baggage = flight['Carry-on']

    graph.add_vertex(start)
    graph.add_vertex(destination)
    graph.add_edge(Edge(start, destination, airline, baggage, price))