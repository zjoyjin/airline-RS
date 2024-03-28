from playwright.sync_api import sync_playwright
import time


""" Test """
# def run(playwright):
#     firefox = playwright.firefox
#     browser = firefox.launch()
#     page = browser.new_page()
#     page.goto("https://example.com")
#     print(page.get_by_text('world'))
#     browser.close()

##YYYY/MM/DD
def run(playwright):
    s = "VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-Bz112c-M1Soyc nCP5yc AjY5Oe LQeN7 TUT4y zlyfOd"
    context = playwright.chromium.launch(headless=False).new_context()
    page = context.new_page()
    page.goto('https://www.google.com/travel/flights?hl=en-US&curr=CAD')

    page.get_by_role("textbox", name="Departure").fill("2024/04/05")
    page.get_by_role("textbox", name="Return").fill("2024/04/28")
    # page.get_by_role("combobox", name="Where to?").fill("Vancouver")
    # page.get_by_role("combobox", name="Where to?").press("Enter")
    # page.get_by_role("combobox", name="Where from?").fill("Edmonton")
    # page.get_by_role("combobox", name="Where from?").press("Enter")
    # time.sleep(1)


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


    # # page.get_by_role("textbox", name="Return").press("Enter")
    # # page.get_by_role("textbox", name="Return").press("Enter")

    with context.expect_page() as new_page_info:

        page.locator(".xFFcie").first.click() # Opens a new tab

        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    new_page = new_page_info.value
    new_page.wait_for_load_state()
    context.close()

"""running it (move to main eventually?)"""
with sync_playwright() as playwright:
    run(playwright)


# IT KINDA WORKS!!
# from playwright.sync_api import sync_playwright
# import time
# from bs4 import BeautifulSoup
#
# with sync_playwright() as playwright:
#     context = playwright.chromium.launch(headless=False).new_context()
#     page = context.new_page()
#     page.goto('https://www.google.com/travel/flights?hl=en-US&curr=CAD')
#
#     page.get_by_role("textbox", name="Departure").fill("2024/04/05")
#     page.get_by_role("textbox", name="Return").fill("2024/04/28")
#
#     # type "From"
#     from_place_field = page.locator('.e5F5td').first
#     from_place_field.click()
#     time.sleep(1)
#     from_place_field.press_sequentially("Edmonton")
#     time.sleep(1)
#     page.keyboard.press('Enter')
#
#     # type "To"
#     to_place_field = page.locator('.e5F5td').nth(1)
#     to_place_field.click()
#     time.sleep(1)
#     to_place_field.press_sequentially("Vancouver")
#     time.sleep(1)
#     page.keyboard.press('Enter')
#
#     page.locator(".xFFcie").first.click()
#
#     time.sleep(1)
#     soup = BeautifulSoup(page.content(), 'html.parser')
#
#     departures = soup.find_all('div', class_='wtdjmc YMlIz ogfYpf tPgKwe')
#     arrivals = soup.find_all('div', class_='XWcVob YMlIz ogfYpf tPgKwe')
#     airlines = soup.find_all('span', class_='h1fkLb')
#     stops = soup.find_all('span', class_='VG3hNb')
#
#     parsed = {}
#     for i in range(0, len(departures)):
#         parsed[i] = []
#
#     for i in range(0, len(departures)):
#         parsed[i].append(f'Departure: {departures[i].text}')
#         parsed[i].append(f'Arrival: {arrivals[i].text}')
#         parsed[i].append(f'Airline: {airlines[i].text}')
#         parsed[i].append(f'# Stops: {stops[i].text}')
#
#     print(parsed)
