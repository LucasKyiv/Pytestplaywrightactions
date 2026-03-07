

from playwright.sync_api import expect, Page

def test_login_page(page: Page):
    page.goto("https://the-internet.herokuapp.com/login")
    page.locator("#username").fill("some_username")
    # clearing the field
    page.locator("#username").fill("")
    page.locator("#username").type("tomsmith", delay=100)
    page.locator("#password").fill("SuperSecretPassword!")
    page.locator("button[type='submit']").press("Enter")
    expect(page.get_by_role("link", name="Logout")).to_be_visible()