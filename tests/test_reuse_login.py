def test_login_success(logged_page):
    logout = logged_page.locator("a:has-text('Logout')")
    assert logout.is_visible()


def test_login_logout(logged_page):
    logged_page.locator("a:has-text('Logout')").click()

    success_message = logged_page.locator("#flash").inner_text()

    assert "You logged out of the secure area!" in success_message