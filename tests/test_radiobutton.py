from playwright.sync_api import Page, expect

def test_select_radio_button(page: Page):
   page.goto("https://demoqa.com/radio-button")

   radio = page.get_by_label("Yes")
   radio.check()

   expect(radio).to_be_checked()
