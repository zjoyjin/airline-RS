""" CSC111 Project 2: Airline Review System

Instructions
============================================
The Python module contains the user input and visualization
code for for Project 2. 

Copyright and Usage Information
============================================
This file is Copyright (c) Ashley Bi, Zhuoyi Jin, Elizabeth Liu, and Kerri Wei.
"""

from Module(Data_Classes) import _Vertex, 
from geoplotlib import
from math import inf

if __name__ == "__main__":
    with open('Airline_Data.csv') as airline_file:
      flight_graph = Graph(airline_file)

    print("Please type your current city (please capitalize the first\n"
          "letter and type the city name in full):")
    location = input()

    print("Please type your desired destination (please capitalize the first letter\n"
          "and type the city name in full):")
    destination = input()

    print("Would you like to check bags on your flight? (Yes/No)")
    bag_check = (input() == "Yes")

    lower_price = -math.inf
    while lower_price < 0:
        print("Please type your lower price bound in CAD (please use numbers only):")
        lower_price = int(input())
        if lower_price < 0:
            print("Please input a number that is greater than or equal to 0.")

    upper_price = -math.inf
     while upper_price < lower_price:
        print("Please type your upper price bound in CAD (please use numbers only):")
        upper_price = int(input())
        if upper_price < lower_price:
            print("Please input a number that is greater than or equal to your lower price bound.")


#Graph calculations

geoplotlib.graph(data,
                 src_lat=’lat_departure’,
                 src_lon=’lon_departure’,
                 dest_lat=’lat_arrival’,
                 dest_lon=’lon_arrival’,
                 color=’hot_r’,
                 alpha=16,
                 linewidth=2)
geoplotlib.show()
    
      
