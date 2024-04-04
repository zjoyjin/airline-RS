""" CSC111 Project 2: Flight Path Finder
============================================
The Python module contains the user input and visualization code for Project 2.

Copyright and Usage Information
============================================
This file is Copyright (c) Ashley Bi, Zhuoyi Jin, Elizabeth Liu, and Kerri Wei.
"""
from Flight_Graph_User import Graph
from flight_network_graph import GraphAll


if __name__ == "__main__":
    print("What city are you currently in?")
    locations = [str.capitalize(input())]

    print("How many cities do you want to visit (not including your current location)")
    number = input()
    while not str.isdigit(number):
        print("Please enter a valid integer!")
        number = input()

    number = int(number)

    print("Please type the names of all cities you want to visit and hit \"enter\" after each one.")
    for i in range(number):
        locations.append(str.capitalize(input()))

    print("Please type your desired leaving date\n"
          "type the format in yyyy/dd/mm):")
    start_date = input()

    # Draw the graph after user input
    user_flight_graph = Graph()
    user_flight_graph.load_user_graph(locations, start_date)
    user_flight_graph.draw_graph_matplot("airport.csv", locations)
    flight_graph = GraphAll()
    flight_graph.load_flights_graph(start_date, "airport.csv", locations)
    flight_graph.draw_graph_matplot_all("airport.csv", locations)


