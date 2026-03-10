from playwright.sync_api import Page, expect

def test_check_checkbox(page: Page) -> None:
    page.goto("https://the-internet.herokuapp.com/checkboxes")
    page.get_by_role("checkbox").first.check()
    page.get_by_role("checkbox").first.uncheck()
    page.get_by_role("checkbox").first.check()
    checkbox = page.get_by_role("checkbox").first
    expect(checkbox).to_be_checked()