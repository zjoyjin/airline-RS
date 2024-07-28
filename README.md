# csc111-project2-flight-path-finder
Project Introduction/ proposal:
Presently, airplanes stand as the most convenient and time-efficient form of
transit for long distance travel. This project is an attempt to aid those who
need to travel to different major cities in Canada in a short period of time. This
includes entrepreneurs and any others who work in business sectors and would
need to fly to different provinces within a span of a few days, staying only a
day at each location. Such travel undertakings could easily cost a lot of money.
Thus, it’s important for travellers to select the cheapest flights. To accomplish
this, our project gets real-time price and airline information from Google Flights
and produces an interactive visualization for users.


# OVERALL GOAL: To recommend travelers the cheapest possible
itinerary by comparing their desired flight route with the cheapest
options on Google Flights. Additionally, produce a geographic map
to visualize the cheapest flight paths they could take on a specific
date from locations all across Canada

Instruction:
1. Download the zip file from MarkUs
2. Install all Python libraries in requirements.txt
3. Run main.py in Python Console, you will prompted for inputs.
4. Enter a city name with correct spelling and hit enter. Note: you should
type in the city name that is inside of the airport.csv, try input bigger
cities, rather than small town.
5. Enter in a positive integer, representing the number of cities you would
like to visit.
6. Enter city names, hitting enter between each one. Again, use correct
spelling. The program will let you enter as many city names as you indi-
cated in step 5.
7. Enter the date you’d like to depart in the yyyy/dd/mm format, using
integers for yyyy, dd, and mm. Ensure that this is an actual date that is
at least tomorrow.
8. You can choose to be recursive or not, it will make sure you get the
cheapest by checking through google flights a couple times, but it will
take at least 5 mins to run. (only type in 2 cities for testing purpose for
a shorter time)
9. After, you will see web scraping of Google Flights and Chromnium will
pop up. Then, a visualization window will pop up, similar to Figure 2
above.

# 3 Datasets

airport.csv
This is a csv containing all airports in Canada. The data was initially taken
from Whereig.com, and then was put into a csv file and cleaned (correcting city
spelling, removing NULL values, reformatting longitude and latitude to be two
seperate columns). Each row contains a city name, airport name, airport code,
latitude, and longitude. The entire file is used in our project, since we have
to compare each location with each row of this file to find the longitude and
latitude of each city. After finding the longitude and latitude of a given city, we
then combine this information with basemap to plot flight paths and labels.

# 4 Computational Overview
Data representation:

Flights are represented by dictionaries Cities and Airports: Cities are rep-
resented as nodes in the graph. Each city is identified by its name, and airports
within each city may also be considered. These cities and airports form the
vertices of the graph.

# Flights: 
Flights between cities are represented as edges in the graph. Each
flight has associated information such as the initial location (departure city),
destination (arrival city), price, airline, and date. These flights establish con-
nections between cities and are stored as edges in the graph.

Flight Itineraries: Flight itineraries represent sequences of flights that con-
nect multiple cities. Each itinerary consists of a series of flights that a passenger
would take to travel from one city to another. These itineraries can be repre-
sented as paths in the graph, where each node along the path represents a city
and each edge represents a flight between cities

Graphs: Graphs play a central role in representing the relationships between
cities and flights. The flight itinerary data can be naturally modeled using a
graph data structure, where cities are represented as vertices and flights are rep-
resented as edges. This allows for efficient traversal and exploration of different
flight routes and connections.

1. Scraping from Google Flights
To accomplish this, we first imported the Playwright and Beautiful Soup li-
braries into scrape.py. Playwright is used to automate navigation of the Google
Flights page. Using Locators (e.g. Page.get by role() or Page.locator()), we
input the queries into their appropriate boxes by identifying the corresponding
HTML element. After executing the search, the Flights page navigates to the
results page, the HTML contents of which we pass to a BeautifulSoup object.
The BeautifulSoup library is then used to parse these contents and obtain the
data required for each search result given, including departure time, price, and
airline. This is done primarily by using BeautifulSoup.find all() to locate ele-
ments by HTML tag and class. time.sleep() from the time library is also used
to buffer actions during the Playwright automation, because the alternatives
(e.g. Page.wait for load state()) either did not work or were inconsistent. The
scraped data is returned as a list of dictionaries, where each dictionary contains
the relevant information of one flight.


3. User itinerary
   
Let’s say a user is planning a trip. They want to travel by plane from city A,
to city B, to city C, then finally to city D, and spend at least one day in each
intermediate city. The goal of this computation is to return the most economical
sequence of flights that the user should take to accomplish this plan–that is, a
list of the cheapest flights A to B, B to C, and C to D, where each flight occurs
a day after the previous one has landed. get connections() is implemented in
two ways: iteratively, and recursively. Both look through all flight options cor-
responding to the appropriate cities and departure times (based on the previous
flight’s arrival time) and return a chronological list of flights that will sum to the
“cheapest” price. The iterative implementation picks flights naively by simply
choosing the cheapest one on the page and basing the next flight off of it. While
this allows the computation to be relatively fast, it is not as accurate. In con-
trast, the recursive implementation looks through each possible itinerary, with
differences in departure time (due to differences in the previous flight’s arrival
time) taken into account. Thus, while yielding significantly more accurate (i.e.
cheaper) results, it is also much slower. The cheapest itinerary computation
was implemented in two ways: iteratively and recursively. The iterative version
queries a flight, gets the cheapest result from this query, then uses the arrival
time of this flight for the next query.

However, what if you have a cheap first flight with really expensive second
flights, versus a slightly more expensive first flight with really cheap second
flights? The iterative version then wouldn’t end up giving the cheapest flights.
Thus, the recursive implementation fixes this issue by going through each pos-
sible itinerary, guaranteeing a cheapest flight returned.

get connections() is implemented in two ways: iteratively, and recursively. Both
look through all flight options corresponding to the appropriate cities and depar-
ture times (based on the previous flight’s arrival time) and return a chronological
list of flights that will sum to the “cheapest” price. The iterative implemen-
tation picks flights naively by simply choosing the cheapest one on the page
and basing the next flight off of it. While this allows the computation to be
relatively fast, it is not as accurate. In contrast, the recursive implementation
looks through each possible itinerary, with differences in departure time (due to
differences in the previous flight’s arrival time) taken into account. Thus, while
yielding significantly more accurate (i.e. cheaper) results, it is also much slower.


3. Report Result
When main.py is run, the user is prompted to input their current city, how
many cities they plan on visiting, and the name of the cities they plan on vis-
iting. Then we will provide a cheapest itinerary that the user could have, with
vertices of the city, edges labeled in airline, dates, and price. This information
is printed in the console. Additionally, a map pops up with each flight path la-
belled with price, airline, departure time, arrival time, and arrival location. The
method responsible for this is user flight graph.draw graph from user input(m,
”airport.csv”, locations). The labels are made by extracting information from
each vertex and edge in the graph. To print each label in the correct loca-
tion, additional information is read from airport.csv to match each city with a
latitude and longitude.



