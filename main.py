""" CSC111 Project 2: Flight Path Finder
============================================
The Python module contains the user input and visualization code for for Project 2. 

Copyright and Usage Information
============================================
This file is Copyright (c) Ashley Bi, Zhuoyi Jin, Elizabeth Liu, and Kerri Wei.
"""

from flight_network_graph import Graph, Vertex
import networkx as nx
import matplotlib.pyplot as plt
import geoplotlib
import math
from typing import Any, Union


if __name__ == "__main__":
    #print cheap graph here
    graph = Graph()
    print("Please type your desired leaving date\n, in yy/dd/mm")

    start_date = input()
    graph.load_viewed_graph(start_date)


    #read airport

    print("Please type all of the airport city you want to go into\n"
          "letter and type the city name in full):")
    locations = input()


    print("Please type your desired leaving date\n"
          "type the format in yy/dd/mm):")
    start_date = input()

    #Draw the graph after user input
    G = nx.DiGraph()
    for vertex in G.vertices.values():
        for dest, price, airline, date in vertex.destinations:
            G.add_edge(vertex.location, dest, weight=price, airline=airline, date=date)

    pos = nx.spring_layout(G)
    labels = {(start, end): f"{airline}\n${price}\n{date}" for start, end, price, airline, date in
              G.edges.data('weight', 'airline', 'date')}
    nx.draw(G, pos, with_labels=True, node_size=1000, node_color='skyblue')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

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



    
      
