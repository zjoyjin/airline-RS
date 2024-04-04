""" CSC111 Project 2: Flight Path Finder
============================================
The Python module contains the code used to web-scrap the Google Flights API for flight information for Project 2.

Copyright and Usage Information
============================================
This file is Copyright (c) Ashley Bi, Zhuoyi Jin, Elizabeth Liu, and Kerri Wei.
"""
from time import sleep
from playwright.sync_api import sync_playwright, Page
from bs4 import BeautifulSoup


def _get_results_page(page: Page, start: str, end: str, departure: str) -> str:
    """ Gets the HTML content of the google flights results page according to user input.
    Parameters:
        - page: initial google flights page
        - start: city of departure
        - end: city of arrival
        - departure: date of departure (YYYY/DD/MM)
    """

    # change filter to one-way trips
    page.locator('.hqBSCb').first.click()   # click "Round Trip" dropdown
    sleep(0.5)
    page.get_by_role('option', name="One way").click()  # click "One way"

    # type "From"
    from_place_field = page.locator('.e5F5td').first
    from_place_field.click()
    sleep(0.5)
    from_place_field.press_sequentially(start)
    sleep(1)
    page.keyboard.press('Enter')

    # type "To"
    to_place_field = page.locator('.e5F5td').nth(1)
    to_place_field.click()
    sleep(0.5)
    to_place_field.press_sequentially(end)
    sleep(1)
    page.keyboard.press('Enter')

    # dates
    departure_field = page.get_by_role("textbox", name="Departure")
    departure_field.first.click()
    sleep(0.7)
    departure_field.press_sequentially(departure)
    for _ in range(3):
        sleep(0.5)
        departure_field.press("Enter")

    # Search
    page.locator(".xFFcie").first.click()
    sleep(2.5)

    return page.content()


def _parse(soup: BeautifulSoup) -> list[dict]:
    """
    Parse the HTML page and return the data as a list of dictionaries.
    Data obtained per flight (str unless otherwise stated) -- 6 total:
        departure time, arrival time, airline, price (float),
        departure airport code, arrival airport code,
    """
    # Get the required info
    departures = soup.find_all('div', class_='wtdjmc YMlIz ogfYpf tPgKwe')
    arrivals = soup.find_all('div', class_='XWcVob YMlIz ogfYpf tPgKwe')
    airlines = soup.find_all('span', class_='h1fkLb')
    prices = soup.find_all('div', class_="BVAVmf I11szd POX3ye")
    airportstart = soup.find_all('div', class_="G2WY5c sSHqwe ogfYpf tPgKwe")
    airportend = soup.find_all('div', class_="c8rWCd sSHqwe ogfYpf tPgKwe")

    # Return info as list of dictionaries
    results = []
    for i in range(0, len(prices)):
        results.append({'Departure': None,
                        'Arrival': None,
                        'Airline': None,
                        'Price': None,
                        'From': None,
                        'To': None
                        })

    for i in range(0, len(prices)):
        results[i]['Departure'] = departures[i].text.replace("\u202f", " ")
        results[i]['Arrival'] = arrivals[i].text.replace("\u202f", " ")
        results[i]['Airline'] = airlines[i].text
        results[i]['Price'] = float(tuple(p for p in prices[i].descendants)[-1][3:].replace(',', ''))  # int
        results[i]['From'] = airportstart[i].text
        results[i]['To'] = airportend[i].text

    return results


def get_results(start: str, end: str, departure: str) -> list[dict]:
    """ Inits scraping and returns a list of flight search results. Calls the above two functions.
    Probably takes ~8 sec to run.
    Returned dictionary's keys:
        - Departure: str (time)
        - Arrival: str (time)
        - Airline: str
        - Price: int
        - From: str (XYZ airport code)
        - To: str (XYZ airport code)
    Parameters:
        - start: city of departure
        - end: city of arrival
        - departure: departing date in YYYY/DD/MM format
    Preconditions:
        - start != '' and end != '' and departure != ''
    """

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)  # Set to False to see Chromium pop-up
        page = browser.new_page()
        page.goto('https://www.google.com/travel/flights?hl=en-US&curr=CAD')

        print("Getting results...")

        try:
            # init soup
            soup = BeautifulSoup(_get_results_page(page, start, end, departure), 'html.parser')
            return _parse(soup)
        except TimeoutError:
            print("ERROR WHILE GETTING RESULTS! Please ensure your Internet connection is decent \
                  and cities are spelled correctly!")
            return []


# For testing purposes
if __name__ == "__main__":
    # res = get_results("Vancouver", "Edmonton", "2024/20/04")
    # if res:
    #     print(res)
    # else:
    #     print("No flights found!")

    import python_ta

    python_ta.check_all(config={
        'extra-imports': ["playwright.sync_api", "bs4", "time"],  # the names (strs) of imported modules
        'allowed-io': ["get_results"],  # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
