from playwright.sync_api import Page, expect

def test_locator_example(page: Page) -> None:
    page.goto("https://git-scm.com/docs/git-push")

    page.locator("a", has_text="Tools").click()

    # get the individual links inside the expanded tools menu
    elements = page.locator("ul.expanded a")

    texts = elements.all_inner_texts()
    print(texts)
    assert texts == ['Command Line', 'GUIs', 'Hosting']


def test_countries_dropdown(page: Page):
    page.goto("https://selenium08.blogspot.com/2019/11/dropdown.html")
    try:
        page.get_by_role("link", name="OK").click(timeout=3000)
    except:
        pass


    countries_dropdown = page.locator("select:has(option[value='AF'])")
    countries_dropdown.scroll_into_view_if_needed()
    # print(countries_dropdown.text_content())
    # Check dropdown is visible
    expect(countries_dropdown).to_be_visible()

    # Get all options
    options = countries_dropdown.locator("option")
    country_texts = options.all_inner_texts()
    # print(country_texts)
    # Check some expected countries exist
    assert "Afghanistan" in country_texts
    assert "Albania" in country_texts
    assert "Algeria" in country_texts

    # Check the dropdown has many countries
    assert len(country_texts) > 100

    # Select a country and verify it was selected
    countries_dropdown.select_option(value="PT")  # Portugal
    expect(countries_dropdown).to_have_value("PT")