import pytest
import os
from playwright.sync_api import expect
from dotenv import load_dotenv

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