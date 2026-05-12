# Pytest Playwright Actions

End-to-end UI test suite written in Python using **Playwright** + **pytest**, covering common web interaction patterns (alerts, drag & drop, iframes, dropdowns, dynamic tables, file uploads, sliders, tooltips, window handling, etc.). Tests run against public demo sites (`the-internet.herokuapp.com`, `jqueryui.com`, and similar) and are wired up for CI on both **GitHub Actions** and **Azure Pipelines**.

## Tech Stack

- Python 3.12
- [Playwright](https://playwright.dev/python/) `1.58.0` (sync API)
- [pytest](https://docs.pytest.org/) `9.0.2`
- `pytest-playwright` — Playwright fixtures for pytest
- `pytest-xdist` — parallel test execution (`-n auto`)
- `pytest-check` — soft assertions
- `pytest-base-url` — base URL config
- `python-dotenv` — loads credentials from `.env`

## Project Structure

```
.
├── .github/workflows/playwright.yml   # GitHub Actions CI
├── azure-pipelines.yml                # Azure DevOps CI
├── auth/auth.json                     # Saved browser storage state (login session)
├── reuse_auth/                        # Helpers for reusing stored auth
├── tests/                             # All test modules (test_*.py)
├── Artifacts/                         # Local trace/video/screenshot output
├── conftest.py                        # Shared fixtures (auth_state, logged_page)
├── pytest.ini                         # Pytest config
├── requirements.txt
└── .env                               # ADMIN_USERNAME / ADMIN_PASSWORD (gitignored)
```

## Fixtures (`conftest.py`)

- **`auth_state`** (session-scoped) — logs into `the-internet.herokuapp.com/login` once using `ADMIN_USERNAME` / `ADMIN_PASSWORD` from `.env`, then dumps the storage state to `auth/auth.json`.
- **`logged_page`** — builds a fresh browser context from the saved storage state and navigates to the `/secure` page, so individual tests start already authenticated.

This pattern (login-once-then-reuse-state) avoids paying the login cost on every test.

## Test Coverage

The `tests/` directory contains ~28 test modules, each focused on a specific UI interaction:

| Area | File(s) |
|---|---|
| Alerts / dialogs | `test_alert_popups.py`, `test_sweet_alert.py` |
| Dropdowns | `test_single_select_dropdown.py`, `test_multiselect_dropdown.py`, `test_dynamic_dropdown.py`, `test_angular_dropdown.py` |
| Tables | `test_dynamic_angular_table.py` |
| Inputs / forms | `test_checkbox.py`, `test_radiobutton.py`, `test_file_upload.py`, `test_slider.py` |
| Mouse actions | `test_double_click.py`, `test_right_click.py`, `test_hover.py`, `test_drag_and_drop.py` |
| Frames & windows | `test_iframe.py`, `test_iframetwo.py`, `test_iframe_nested.py`, `test_window_handling.py` |
| Locators | `test_locator_through_other.py`, `test_multiobject.py`, `test_elements_contains.py` |
| Misc | `test_tooltip.py`, `test_toast_message.py`, `test_refresh.py`, `test_remove_focus.py`, `test_enabled_button.py`, `test_file.py` |
| Auth reuse | `test_reuse_login.py` (uses `logged_page` fixture) |
| Soft assertions | `test_soft_assertion.py` (uses `pytest-check`) |

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows
pip install -r requirements.txt
playwright install --with-deps
```

Create a `.env` file at the repo root:

```
ADMIN_USERNAME=tomsmith
ADMIN_PASSWORD=SuperSecretPassword!
```

## Running Tests

```bash
pytest                                  # all tests, verbose (per pytest.ini)
pytest -n auto                          # parallel
pytest tests/test_alert_popups.py       # single file
pytest -k "tooltip"                     # by name pattern
pytest --browser firefox                # switch browser (chromium/firefox/webkit)
pytest --headed                         # see the browser
pytest --tracing retain-on-failure \
       --video retain-on-failure \
       --screenshot only-on-failure     # CI-style artifacts
```

## CI

### GitHub Actions — `.github/workflows/playwright.yml`
Triggers on push to `main` and on PRs. Installs deps, runs Playwright browsers, executes `pytest -n auto`, and uploads `test-results/` on failure. Credentials come from `ADMIN_USERNAME` / `ADMIN_PASSWORD` repo secrets.

### Azure Pipelines — `azure-pipelines.yml`
Triggers on `main`. Runs the same flow but publishes JUnit results (`test-results/results.xml`) and the full `test-results` directory as a `playwright-results` build artifact, with traces/videos/screenshots retained on failure.

## Notes

- `pytest.ini` keeps test discovery scoped to `tests/` and enables verbose output by default.
- `.env`, `__pycache__/`, `.idea/`, and `.claude/worktrees/` are gitignored.
- Storage-state-based auth (`auth/auth.json`) is the canonical pattern here — prefer the `logged_page` fixture over logging in inside individual tests.