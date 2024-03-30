# IT KINDA WORKS!!
from playwright.sync_api import sync_playwright, Page
import time
from bs4 import BeautifulSoup

def get_results_page(page: Page) -> str:
    # dates
    page.get_by_role("textbox", name="Departure").fill("2024/04/05")
    page.get_by_role("textbox", name="Return").fill("2024/04/28")

    # type "From"
    from_place_field = page.locator('.e5F5td').first
    from_place_field.click()
    time.sleep(0.5)
    from_place_field.press_sequentially("Edmonton")
    time.sleep(1)
    page.keyboard.press('Enter')

    # type "To"
    to_place_field = page.locator('.e5F5td').nth(1)
    to_place_field.click()
    time.sleep(0.5)
    to_place_field.press_sequentially("Beijing")
    time.sleep(1)
    page.keyboard.press('Enter')

    # Search

    page.locator(".xFFcie").first.click()

    # page.wait_for_event("framenavigated")     # don't think this is needed but im not sure
    # page.wait_for_load_state('networkidle')     # discouraged apparently, but idk if this is better/worse than time.sleep

    time.sleep(5)   # bc none of the wait for load states work ToT

    # page.locator(".zISZ5c").and_(page.locator(".QB2Jof")).click()   # get more flights
    # page.wait_for_load_state('networkidle')
    # time.sleep(1)
    return page.content()

def parse(page: Page) -> dict:
    # init soup
    soup = BeautifulSoup(get_results_page(page), 'html.parser')

    # get info
    departures = soup.find_all('div', class_='wtdjmc YMlIz ogfYpf tPgKwe')
    arrivals = soup.find_all('div', class_='XWcVob YMlIz ogfYpf tPgKwe')
    airlines = soup.find_all('span', class_='h1fkLb')
    # stops = soup.find_all('span', class_='VG3hNb')
    airport_stops = soup.find_all('span', class_="rGRiKd")      # format: either "X stops in XYZ, ABC" or "Nonstop"
    prices = soup.find_all('div', class_="BVAVmf I11szd POX3ye")
    airport_from = soup.find_all('div', class_="G2WY5c sSHqwe ogfYpf tPgKwe")
    airport_to = soup.find_all('div', class_="c8rWCd sSHqwe ogfYpf tPgKwe")
    durations = soup.find_all('span', class_="EzfXjb")
    # baggage: get by aria label ("This price for this flight doesn't include...")


    # return info as list of dictionaries (maybe split into separate function later)
    results = []
    for i in range(0, len(departures)):
        results.append({'Departure' : None,
                        'Arrival' : None,
                        'Airline' : None,
                        'Price' : None,
                        'Duration' : None,
                        'From' : None,
                        'To' : None,
                        'Stops' : None})

    for i in range(0, len(departures)):
        results[i]['Departure'] = departures[i].text.replace("\u202f", " ")
        results[i]['Arrival'] = arrivals[i].text.replace("\u202f", " ")
        results[i]['Airline'] = airlines[i].text
        # results[i].append(f'# Stops: {stops[i].text}')
        results[i]['Price'] = [p for p in prices[i].descendants][-1]
        results[i]['Duration'] = durations[i].find_previous_sibling().text
        results[i]['From'] = airport_from[i].text
        results[i]['To'] = airport_to[i].text
        results[i]['Stops'] = airport_stops[i].text
    
    return results

def get_results():
    with sync_playwright() as playwright:
        context = playwright.chromium.launch(headless=False).new_context()
        page = context.new_page()
        page.goto('https://www.google.com/travel/flights?hl=en-US&curr=CAD')
        # could probably get currency customization by changing curr=   ^

        results = parse(page)
        if results:
            print(results)
        else:
            print("No flights found!")
        return results