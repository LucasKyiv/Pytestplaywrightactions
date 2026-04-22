from playwright.sync_api import Page, expect


def test_tool_tip(page: Page) -> None:
    page.goto("https://irq.ie/")
    page.get_by_role("button", name="Allow all cookies").click()
    page.get_by_role("link", name="Search Qualifications").click()
    page.get_by_role("slider", name="Minimum credit amount").click()
    page.get_by_role("slider", name="Minimum credit amount").press("ArrowRight")
    expect(page.get_by_role("spinbutton", name="From")).to_have_value("5")