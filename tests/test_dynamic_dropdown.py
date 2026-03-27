from playwright.sync_api import Page, expect


def get_loc_city(page: Page, city: str):
    return page.locator(f"//div[text()='{city}']")


def test_dynamic_dropdown(page: Page) -> None:
    page.goto("https://www.spicejet.com/")

    from_input = page.locator("//div[@data-testid='to-testID-origin']//input")
    from_input.click()
    from_input.fill("ko")

    expect(get_loc_city(page, "Kolkata")).to_be_visible()