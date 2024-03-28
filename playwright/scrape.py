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
    time.sleep(1)
    from_place_field.press_sequentially("Edmonton")
    time.sleep(1)
    page.keyboard.press('Enter')

    # type "To"
    to_place_field = page.locator('.e5F5td').nth(1)
    to_place_field.click()
    time.sleep(1)
    to_place_field.press_sequentially("Vancouver")
    time.sleep(1)
    page.keyboard.press('Enter')

    # Search

    page.locator(".xFFcie").first.click()
    # page.wait_for_load_state()
    time.sleep(1)   # NOTE: might not work if page requires more than 1 second of loading time??? fix later maybe
    return page.content()

def parse(page: Page):
    # init soup
    soup = BeautifulSoup(get_results_page(page), 'html.parser')

    # get info
    departures = soup.find_all('div', class_='wtdjmc YMlIz ogfYpf tPgKwe')
    arrivals = soup.find_all('div', class_='XWcVob YMlIz ogfYpf tPgKwe')
    airlines = soup.find_all('span', class_='h1fkLb')
    stops = soup.find_all('span', class_='VG3hNb')

    # return info (maybe split into separate function later)
    parsed = {}
    for i in range(0, len(departures)):
        parsed[i] = []

    for i in range(0, len(departures)):
        parsed[i].append(f'Departure: {departures[i].text}')
        parsed[i].append(f'Arrival: {arrivals[i].text}')
        parsed[i].append(f'Airline: {airlines[i].text}')
        parsed[i].append(f'# Stops: {stops[i].text}')
    
    return parsed


with sync_playwright() as playwright:
    context = playwright.chromium.launch(headless=False).new_context()
    page = context.new_page()
    page.goto('https://www.google.com/travel/flights?hl=en-US&curr=CAD')

    parsed = parse(page)

    print(parsed)
