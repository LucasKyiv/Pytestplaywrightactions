import pytest
from playwright.sync_api import Page, expect

@pytest.fixture
def test_file(tmp_path):
    file_path = tmp_path / "MyTestUpload19.txt"
    file_path.write_text("This is a test file")
    return str(file_path)


def test_file_uploaded(page: Page, test_file: str) -> None:
    page.goto("https://davidwalsh.name/demo/multiple-file-upload.php")

    page.locator("#filesToUpload").set_input_files(test_file)
    uploaded_file = page.locator("#fileList li")
    expect(uploaded_file).to_have_text("MyTestUpload19.txt")