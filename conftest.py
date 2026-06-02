import pytest
import os
from playwright.sync_api import expect
from dotenv import load_dotenv
from slugify import slugify
import allure
from pathlib import Path

load_dotenv()

@pytest.fixture(scope="session")
def auth_state(browser):
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://the-internet.herokuapp.com/login")
    page.fill("#username", os.getenv("ADMIN_USERNAME"))
    page.fill("#password", os.getenv("ADMIN_PASSWORD"))
    page.click("button[type='submit']")

    page.wait_for_url("**/secure")

    context.storage_state(path="auth/auth.json")
    context.close()

    return "auth/auth.json"

@pytest.fixture()
def logged_page(browser, auth_state):
    context = browser.new_context(storage_state=auth_state)
    page = context.new_page()

    page.goto("https://the-internet.herokuapp.com/secure")

    yield page

    context.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    screen_file = ''
    report = outcome.get_result()
    extras = getattr(report, "extras", [])
    if report.when == "call":
        xfail = hasattr(report, "wasxfail")
        if (report.failed or xfail) and "page" in item.funcargs:
            page = item.funcargs["page"]
            screenshot_dir = Path("screenshots")
            screenshot_dir.mkdir(exist_ok=True)
            screen_file = str(screenshot_dir / f"{slugify(item.nodeid)}.png")
            page.screenshot(path=screen_file)

        if screen_file and ((report.skipped and xfail) or (report.failed and not xfail)):
            if pytest_html is not None:
                extras.append(pytest_html.extras.png(screen_file))

            allure.attach.file(
                screen_file,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )

        report.extras = extras