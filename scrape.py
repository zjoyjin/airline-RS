from playwright.sync_api import sync_playwright, Page
from bs4 import BeautifulSoup
from time import sleep

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
    departure_field.press_sequentially(departure)
    for i in range(3):
        sleep(0.5)
        departure_field.press("Enter")

    # Search
    page.locator(".xFFcie").first.click()
    sleep(2.5)

    # page.locator(".zISZ5c").and_(page.locator(".QB2Jof")).click()   # get more flights
    # sleep(2)    # if this doesn't work, then it'll just be as if this wasn't clicked

    return page.content()


def _parse(soup: BeautifulSoup) -> list[dict]:
    """
    Parse the HTML page and return the data as a list of dictionaries.
    Data obtained per flight (str unless otherwise stated) -- 6 total:
        departure time, arrival time, airline, price (float),
        departure airport code, arrival airport code,
    """
    # get info
    departures = soup.find_all('div', class_='wtdjmc YMlIz ogfYpf tPgKwe')
    arrivals = soup.find_all('div', class_='XWcVob YMlIz ogfYpf tPgKwe')
    airlines = soup.find_all('span', class_='h1fkLb')
    # stops = soup.find_all('span', class_='VG3hNb')
    # airport_stops = soup.find_all('span', class_="rGRiKd")      # format: either "X stops in XYZ, ABC" or "Nonstop"
    prices = soup.find_all('div', class_="BVAVmf I11szd POX3ye")
    airportstart = soup.find_all('div', class_="G2WY5c sSHqwe ogfYpf tPgKwe")
    airportend = soup.find_all('div', class_="c8rWCd sSHqwe ogfYpf tPgKwe")
    # durations = soup.find_all('span', class_="EzfXjb")
    # baggage = soup.find_all('div', class_='BVAVmf I11szd POX3ye')

    # return info as list of dictionaries
    results = []
    for i in range(0, len(departures)):
        results.append({'Departure': None,
                        'Arrival': None,
                        'Airline': None,
                        'Price': None,
                        # 'Duration': None,
                        'From': None,
                        'To': None,
                        # 'Stops': None,
                        # 'Overhead': None
                        })

    for i in range(0, len(departures)):
        results[i]['Departure'] = departures[i].text.replace("\u202f", " ")
        results[i]['Arrival'] = arrivals[i].text.replace("\u202f", " ")
        results[i]['Airline'] = airlines[i].text
        # results[i].append(f'# Stops: {stops[i].text}')
        results[i]['Price'] = float([p for p in prices[i].descendants][-1][3:].replace(',', ''))  # int
        # results[i]['Duration'] = durations[i].find_previous_sibling().text
        results[i]['From'] = airportstart[i].text
        results[i]['To'] = airportend[i].text
        # results[i]['Stops'] = airport_stops[i].text
        # results[i]['Overhead'] = baggage[i].find('svg') is None     # bool

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
    """

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)     # Set to False to see Chromium pop-up
        page = browser.new_page()
        page.goto('https://www.google.com/travel/flights?hl=en-US&curr=CAD')
        # could probably get currency customization by changing curr=   ^
        # but then would need to alter how price str -> int is done

        print("Getting results...")

        # init soup
        soup = BeautifulSoup(_get_results_page(page, start, end, departure), 'html.parser')

        return _parse(soup)


# For testing purposes
if __name__ == "__main__":
    res = get_results("Vancouver", "Edmonton", "2024/04/20")
    if res:
        print(res)
    else:
        print("No flights found!")
