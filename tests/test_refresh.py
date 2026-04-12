from playwright.sync_api import expect, Page

def test_refresh_page(page: Page):
    page.goto("https://www.thomann.pt/intl/index.html")
    page.reload(wait_until="load")
    expect(page).to_have_url("https://www.thomann.pt/intl/index.html")