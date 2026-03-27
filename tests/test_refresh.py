from playwright.sync_api import expect, Page

def test_refresh_page(page: Page):
    page.goto("https://www.thomann.pt/intl/index.html")
    page.reload(wait_until="load")