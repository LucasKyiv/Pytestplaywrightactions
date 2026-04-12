from playwright.sync_api import Page, expect


def test_angular_web_table(page: Page) -> None:
    page.goto("https://primeng.org/")
    page.locator("div:nth-child(5) > .pi").click()
    # Click on a checkbox by customer name
    rows = page.get_by_role("table").locator("tr")
    checkbox = rows.filter(has_text="Brook Simmons").locator("input[type='checkbox']")
    checkbox.check()
    expect(checkbox).to_be_checked()

    # Print all data from the table

    index = 0

    while index < rows.count():
        print(rows.nth(index).inner_text())
        index += 1

    # Get the balance of a customer
    row = rows.filter(has_text="Brook Simmons")

    lead_source = row.locator("td").nth(5)  # adjust index based on column position

    print(lead_source.inner_text())

    expect(lead_source).to_contain_text("Linkedin")