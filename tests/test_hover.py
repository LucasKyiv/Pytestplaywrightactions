from playwright.sync_api import Page, expect


def test_hover_example(page: Page) -> None:
    page.goto("https://www.globalsqa.com/demo-site/")
    # Accept cookies (adjust selector if needed)
    page.locator("button:has-text('Consent')").click()
    header_menu = page.locator("#menu-item-7128", has_text="Free Ebooks")

    # print(header_menu.text_content())
    # print(header_menu.inner_text())
    # print(header_menu.count())

    header_menu.hover()
    print(header_menu.text_content())
    assert header_menu.count() == 1