from playwright.sync_api import sync_playwright

""" Test """
# def run(playwright):
#     firefox = playwright.firefox
#     browser = firefox.launch()
#     page = browser.new_page()
#     page.goto("https://example.com")
#     print(page.get_by_text('world'))
#     browser.close()

with sync_playwright() as playwright:
    run(playwright)