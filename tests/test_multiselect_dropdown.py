from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    # Go to https://selenium08.blogspot.com/2019/11/dropdown.html
    page.goto("https://selenium08.blogspot.com/2019/11/dropdown.html")
    try:
        page.get_by_role("link", name="OK").click(timeout=3000)
    except:
        pass
    # page.locator("select[name='Month']").select_option(['Sept', 'May', 'July'])
    # page.locator("select[name='Month']").select_option(value='Feb', index=6, label='January')
    # page.locator("select[name='Month']").select_option(index=[2, 4, 6])
    dropdown = page.locator("select[name='Month']")
    dropdown.scroll_into_view_if_needed()

    dropdown.select_option(index=[2, 4, 6])
    selected = page.locator("select[name='Month']").evaluate(
        "el => Array.from(el.selectedOptions).map(o => o.text)"
    )

    assert selected == ['February', 'April', 'June']
    page.wait_for_timeout(5000)

def test_select_option1(page: Page):
    page.goto("https://the-internet.herokuapp.com/dropdown")

    dropdown = page.locator("#dropdown")

    dropdown.select_option(label="Option 1")

    selected = page.locator("#dropdown option:checked")

    expect(selected).to_have_text("Option 1")

from playwright.sync_api import Page, expect


def test_multi_elements(page: Page) -> None:
    # Go to https://selenium08.blogspot.com/2019/11/dropdown.html
    page.goto("https://selenium08.blogspot.com/2019/11/dropdown.html")
    country_options = page.locator("select[name='country'] option")
    # print(type(country_options))
    # print(country_options.all_inner_texts())
    # print(country_options.count())
    #
    # print(country_options.first.inner_text())
    # print(country_options.last.inner_text())

    index = 0
    while index < country_options.count():
        # getting list of countries from dropdown
        # print(country_options.nth(index).inner_text())
        index = index + 1
    assert index > 240