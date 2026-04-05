from playwright.sync_api import Page, expect

def get_subject_autosuggestion(subject):
    return f"//div[contains(@class, 'subjects-auto-complete__menu-list')]//div[text()='{subject}']"


def select_subject2(page, subject):
    subject_autosuggestion = page.locator(get_subject_autosuggestion(subject))
    subject_autosuggestion.click()


def test_possible_to_click_autosuggestion(page: Page) -> None:
    page.goto("https://demoqa.com/automation-practice-form")
    subject_input = page.locator("#subjectsInput")
    subject_input.fill("E")
    select_subject2(page, "English")
    subject_input.fill("G")
    select_subject2(page, "Accounting")
    expect(page.get_by_text("English")).to_be_visible()
    expect(page.locator(".subjects-auto-complete__multi-value__label", has_text="Accounting")).to_be_visible()