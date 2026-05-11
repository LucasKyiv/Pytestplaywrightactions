from playwright.sync_api import Page, expect


def test_google_search_input(page: Page) -> None:

    page.goto(
        "https://www.google.com/",
        wait_until="domcontentloaded"
    )

    # Handle cookie popup if present
    accept_buttons = [
        page.get_by_role("button", name="Aceitar tudo"),
        page.get_by_role("button", name="Accept all"),
        page.get_by_role("button", name="Alles accepteren")
    ]

    for button in accept_buttons:
        try:
            if button.is_visible(timeout=3000):
                button.click()
                break
        except:
            pass

    # Stable locator for Google search box
    search_input = page.locator("textarea[name='q']")

    expect(search_input).to_be_visible()

    search_input.click()

    # Type using keyboard
    page.keyboard.press("P")
    page.keyboard.press("l")
    page.keyboard.press("a")
    page.keyboard.press("y")

    # Remove focus
    search_input.blur()

    # These keys should not affect input now
    page.keyboard.press("W")
    page.keyboard.press("R")
    page.keyboard.press("I")
    page.keyboard.press("G")
    page.keyboard.press("H")

    # Assertion
    expect(search_input).to_have_value("Play")