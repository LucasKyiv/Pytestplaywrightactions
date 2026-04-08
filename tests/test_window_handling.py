from playwright.sync_api import Playwright, sync_playwright, expect


def test_run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch()
    context = browser.new_context()
    # Open new page
    page = context.new_page()

    # Go to https://the-internet.herokuapp.com/windows
    page.goto("https://the-internet.herokuapp.com/windows", timeout=60000)
    with page.expect_popup() as popup_info:
        page.locator("text=Click Here").click()
    page1 = popup_info.value

    new_window_txt = page1.locator(".example h3")
    print(new_window_txt.inner_text())
    expect(new_window_txt).to_have_text('New Window')
    print(page1.title())
    print(page.title())
    expect(page).to_have_title('The Internet')
    expect(page1).to_have_title('New Window')
    page.bring_to_front()