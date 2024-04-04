""" CSC111 Project 2: Flight Path Finder
============================================
The Python module contains the user input and visualization code for for Project 2.

Copyright and Usage Information
============================================
This file is Copyright (c) Ashley Bi, Zhuoyi Jin, Elizabeth Liu, and Kerri Wei.
"""

import networkx as nx
import matplotlib.pyplot as plt
import math
from typing import Any, Union
from Flight_Graph_User import Graph

from flight_network_graph import Graph_all

from mpl_toolkits.basemap import Basemap





if __name__ == "__main__":
    print("What city are you currently in?")
    locations = [str.capitalize(input())]

    print("How many cities do you want to visit (not including your current location)")
    number = int(input())

    print("Please type the names of all cities you want to visit and hit \"enter\" after each one.")
    for i in range(number):
        locations.append(str.capitalize(input()))

    print("Please type your desired leaving date\n"
          "type the format in yyyy/dd/mm):")
    start_date = input()

    # Draw the graph after user input
    user_flight_graph = Graph()
    user_flight_graph.load_viewed_user_graph(locations, start_date)
    user_flight_graph.draw_graph_matplot("airport.csv", locations)
    flight_graph = Graph_all()
    flight_graph.load_viewed_graph(start_date, "airport.csv", locations)
    flight_graph.draw_graph_matplot_all("airport.csv", locations)



    #print the graph of user input



    # # Creating the graph with airline data
    # flight_graph = Graph('Airline_Data.csv')
    #
    # matching_flights = []
    # for edge in flight_graph.edges[location]:
    #     if edge.desfor initial, vertex in self.vertices.items():
    #         for dest_tuple in vertex.destinations:
    #             dest, price, airline, date = dest_tuple
    #             G.add_edge(initial, dest, weight=price, airline=airline, date=date)tination.name == destination and edge.baggage == ('yes' if bag_check else 'no') and 0 <= edge.price <= upper_price:
    #         matching_flights.append(edge)
    #
    # # Print out the matching flights
    # if matching_flights:
    #     print("\nMatching flights:")
    #     for flight in matching_flights:
    #         print(flight)
    # else:
    #     print("\nNo matching flights found.")
