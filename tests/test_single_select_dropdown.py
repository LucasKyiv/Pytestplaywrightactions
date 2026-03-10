import re
from playwright.sync_api import Page, expect


def test_example_dropdown(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/dropdown")
    dropdown = page.locator("#dropdown")
    expect(dropdown.locator("option:checked")).to_have_text("Please select an option")

def test_example_dropdown_one(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/dropdown")
    page.locator("#dropdown").select_option("2")
    page.locator("#dropdown").select_option("1")
    dropdown = page.locator("#dropdown")
    expect(dropdown).to_have_value("1")