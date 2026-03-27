from playwright.sync_api import expect, Page

def test_refresh_page(page: Page):
    page.goto("https://ukr.net", wait_until="domcontentloaded")
    page.reload(wait_until="load")