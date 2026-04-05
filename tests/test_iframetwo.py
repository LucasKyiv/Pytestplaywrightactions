from playwright.sync_api import Page, expect

def test_handle_iframe_by_name(page: Page) -> None:
    page.goto("https://www.rediff.com/")

    # Wait for iframe to appear
    page.wait_for_selector("iframe[name='moneyiframe']")

    # Now get the frame
    iframe_locator = page.frame(name="moneyiframe")
    assert iframe_locator is not None, "Iframe not found!"

    # Locate NSE index
    nse_index = iframe_locator.locator("span#nseindex")
    nse_value = nse_index.inner_text()

    # Assertions
    assert isinstance(nse_value, str)
    nse_value_float = float(nse_value.replace(",", ""))
    assert isinstance(nse_value_float, float)