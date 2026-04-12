from playwright.sync_api import Page, expect


def test_sweet_alert(page: Page) -> None:
    page.goto("https://sweetalert2.github.io/")

    # Click the button
    page.locator("text=Show success message").click()

    # Locate alert title
    alert_msg = page.locator("#swal2-title")

    # Assert text (auto-waits)
    expect(alert_msg).to_have_text("Good job!")

    # Click OK
    page.locator("button", has_text="OK").click()

    # Wait for alert to disappear (auto-waits)
    expect(alert_msg).to_be_hidden()