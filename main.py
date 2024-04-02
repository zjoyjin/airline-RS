""" CSC111 Project 2: Flight Path Finder
============================================
The Python module contains the user input and visualization code for for Project 2. 

Copyright and Usage Information
============================================
This file is Copyright (c) Ashley Bi, Zhuoyi Jin, Elizabeth Liu, and Kerri Wei.
"""

from flight_network_graph import Graph, Vertex
from datetime
import geoplotlib
import math
from typing import Any, Union


if __name__ == "__main__":
    #print cheap graph here
    graph = Graph()
    print("Please type your desired leaving date\n, in yyyy/mm/dd")

    start_date = input()
    graph.load_viewed_graph(start_date)


    #read airport

    print("Please type all of the airport city you want to go into\n"
          "letter and type the city name in full):")
    locations = input()
    if locations not in airport.csv:
        print("This is not a valid airport, retype")
        locations = input()

    print("Please type your desired leaving date\n"
          "type the format in yyyy/mm/dd):")
    start_date = input()


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



    
      
