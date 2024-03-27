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
    print(new_page.title())
    context.close()

"""running it (move to main eventually?)"""
with sync_playwright() as playwright:
    run(playwright)