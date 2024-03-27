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

if __name__ == "__main__":
    with open('Airline_Data.csv') as airline_file:
      flight_graph = Graph(airline_file)

    print("Please type your current city:")
    
      
