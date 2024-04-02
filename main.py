""" CSC111 Project 2: Flight Path Finder
============================================
The Python module contains the user input and visualization code for for Project 2. 

Copyright and Usage Information
============================================
This file is Copyright (c) Ashley Bi, Zhuoyi Jin, Elizabeth Liu, and Kerri Wei.
"""

from flight_network_graph import Graph, Vertex
from Flight_Graph_User import Graph, Vertex
import networkx as nx
import matplotlib.pyplot as plt
import math
from typing import Any, Union


if __name__ == "__main__":
    #print cheap graph here
    graph = Graph()
    print("Please type your desired leaving date\n, in yy/dd/mm")

    start_date = input()
    graph.load_viewed_graph(start_date)


    #read airport
    print("please type in the number of cities you wanto go in integer")
    number = int(input())
    print("Please type all of the airport city you want to go into\n"
          "letter and type the city name in full):")
    locations = []
    for i in range (number):
        locations.append(input())


    print("Please type your desired leaving date\n"
          "type the format in yy/dd/mm):")
    start_date = input()

    #Draw the graph after user input
    flight_graph = Graph()

    flight_graph.load_viewed_user_graph(locations, start_date)
    flight_graph.draw_graph()

    #print the graph of user input



    # # Creating the graph with airline data
    # flight_graph = Graph('Airline_Data.csv')
    #
    # matching_flights = []
    # for edge in flight_graph.edges[location]:
    #     if edge.destination.name == destination and edge.baggage == ('yes' if bag_check else 'no') and 0 <= edge.price <= upper_price:
    #         matching_flights.append(edge)
    #
    # # Print out the matching flights
    # if matching_flights:
    #     print("\nMatching flights:")
    #     for flight in matching_flights:
    #         print(flight)
    # else:
    #     print("\nNo matching flights found.")



    
      
