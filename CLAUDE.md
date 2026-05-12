# CLAUDE.md

Guidance file loaded automatically by Claude Code in this repository. Mirrors the structure of `README.md` but adds the conventions, gotchas, and "do this / don't do that" rules Claude should follow when editing or extending the suite.

---

## 1. Project at a Glance

End-to-end UI test suite written in Python using **Playwright (sync API)** + **pytest**. There is **no application under test in this repo** — tests target public demo sites:

- `https://the-internet.herokuapp.com` — alerts, login, file upload, iframes, drag & drop, dropdowns, etc.
- `https://jqueryui.com` — tooltips, sliders, draggables.
- A handful of other public Angular/JS demo pages.

Goal of the repo: showcase common Playwright + pytest interaction patterns, runnable in CI on GitHub Actions and Azure Pipelines.

## 2. Tech Stack

- **Python 3.12** (CI pins this exact version)
- **Playwright** `1.58.0` — sync API only
- **pytest** `9.0.2`
- `pytest-playwright` `0.7.2` — provides the `page`, `browser`, `context` fixtures
- `pytest-xdist` `3.8.0` — parallel execution (`-n auto`)
- `pytest-check` `2.8.0` — soft assertions
- `pytest-base-url` `2.1.0` — base URL config
- `python-dotenv` `1.2.2` — loads `.env`

All versions in `requirements.txt` are pinned with `==`. **Keep them pinned.**

## 3. Project Structure

```
.
├── .github/workflows/playwright.yml   # GitHub Actions CI (push/PR)
├── azure-pipelines.yml                # Azure DevOps CI (manual only: trigger: none / pr: none)
├── auth/auth.json                     # Saved browser storage state (login session)
├── reuse_auth/                        # Helpers for reusing stored auth
├── tests/                             # All test modules (test_*.py)
├── Artifacts/                         # Local trace/video/screenshot output
├── conftest.py                        # Shared fixtures: auth_state, logged_page
├── pytest.ini                         # Pytest config (testpaths=tests, addopts=-v)
├── requirements.txt                   # Pinned deps (UTF-16 encoded on disk)
├── README.md                          # Human-facing project overview
├── CLAUDE.md                          # This file
└── .env                               # ADMIN_USERNAME / ADMIN_PASSWORD (gitignored)
```

## 4. Fixtures (`conftest.py`)

Two fixtures power the login-once-reuse-state pattern. **Use them — don't reinvent login flows inside tests.**

- **`auth_state`** *(session-scoped)*
  - Logs in to `the-internet.herokuapp.com/login` using `ADMIN_USERNAME` / `ADMIN_PASSWORD` from `.env`.
  - Dumps storage state to `auth/auth.json`.
  - Returns the path to the storage-state file.
- **`logged_page`** *(per-test)*
  - Creates a new browser context from `auth/auth.json`.
  - Navigates to `/secure` and yields the page.
  - Cleans up the context after the test.

Canonical usage (see `tests/test_reuse_login.py`):

```python
def test_login_success(logged_page):
    assert logged_page.locator("a:has-text('Logout')").is_visible()
```

## 5. Test Coverage

`tests/` contains ~28 test modules, one per interaction concept. **When adding a new pattern, create a new `test_<feature>.py` file — don't bolt it onto an unrelated module.**

| Area | File(s) |
|---|---|
| Alerts / dialogs | `test_alert_popups.py`, `test_sweet_alert.py` |
| Dropdowns | `test_single_select_dropdown.py`, `test_multiselect_dropdown.py`, `test_dynamic_dropdown.py`, `test_angular_dropdown.py` |
| Tables | `test_dynamic_angular_table.py` |
| Inputs / forms | `test_checkbox.py`, `test_radiobutton.py`, `test_file_upload.py`, `test_slider.py` |
| Mouse actions | `test_double_click.py`, `test_right_click.py`, `test_hover.py`, `test_drag_and_drop.py` |
| Frames & windows | `test_iframe.py`, `test_iframetwo.py`, `test_iframe_nested.py`, `test_window_handling.py` |
| Locators | `test_locator_through_other.py`, `test_multiobject.py`, `test_elements_contains.py` |
| Misc UI | `test_tooltip.py`, `test_toast_message.py`, `test_refresh.py`, `test_remove_focus.py`, `test_enabled_button.py`, `test_file.py` |
| Auth reuse | `test_reuse_login.py` (uses `logged_page`) |
| Soft assertions | `test_soft_assertion.py` (uses `pytest-check`) |

## 6. Coding Conventions

Follow these so new code blends in with the existing suite.

### Required
- **Sync Playwright only.** All tests use `from playwright.sync_api import Page`. Do NOT introduce `async def` tests.
- **Type the `page` parameter** as `Page`: `def test_x(page: Page) -> None:`. Most existing files do this.
- **One concept per file.** New interaction → new file.
- **Use `logged_page` for authenticated flows.** Never call `page.goto("/login")` + fill credentials inside a test.
- **Credentials come from `.env`** via `os.getenv("ADMIN_USERNAME")` / `os.getenv("ADMIN_PASSWORD")`. Never hardcode.
- **Locator style** mirrors what's already in the suite:
  - `page.locator("#id")`, `page.locator("text=Foo")`, `page.locator("a:has-text('Logout')")`
  - `page.frame_locator("iframe.demo-frame").locator("#age")` for iframes
- **Assertions:** plain `assert` is fine for simple equality; use Playwright's `expect(locator).to_...()` for auto-waiting checks; use `pytest_check.equal(...)` only when a test must keep going after a failure (see `test_soft_assertion.py`).

### Forbidden / Avoid
- **No `time.sleep(...)` for sync.** Use Playwright's auto-waiting (`expect`, `wait_for`, `wait_for_url`). Note: `test_alert_popups.py` has a leftover `import time` that is unused — don't take it as a pattern.
- **No Page Object Model / framework abstractions** unless explicitly asked. The suite is intentionally flat and script-like.
- **No new top-level dependencies** without updating `requirements.txt` with an exact `==` pin.
- **No emojis** in code or test output.
- **No comments explaining what well-named code already says.** Existing tests use short docstrings to describe the *scenario* (e.g. `'''Handle javascript alert pop up'''`) — that style is fine, "what the next line does" comments are not.

## 7. Running Tests

```bash
pytest                                   # all tests, verbose (per pytest.ini)
pytest -n auto                           # parallel (what CI uses)
pytest tests/test_alert_popups.py        # single file
pytest tests/test_alert_popups.py::test_click_for_js_alert   # single test
pytest -k "tooltip"                      # by name pattern
pytest --browser firefox                 # or chromium / webkit
pytest --headed                          # see the browser
pytest --headed --slowmo 500             # slow motion for debugging
pytest --tracing retain-on-failure \
       --video retain-on-failure \
       --screenshot only-on-failure      # CI-style artifacts
```

**Don't run the entire suite to validate a one-file change.** Run the file (and obviously related ones) instead — full runs are slow and hit live demo sites.

## 8. CI

### GitHub Actions — `.github/workflows/playwright.yml`
- Triggers: push to `main`, all PRs.
- Steps: checkout → setup Python 3.12 → `pip install -r requirements.txt` → `playwright install --with-deps` → `pytest -n auto`.
- Secrets: `ADMIN_USERNAME`, `ADMIN_PASSWORD`.
- Uploads `test-results/` artifact only on failure.

### Azure Pipelines — `azure-pipelines.yml`
- **Triggers: `trigger: none` and `pr: none`** — pipeline only runs when manually invoked from the Azure DevOps UI. **Do not re-enable auto-triggers without being asked.**
- Same install flow as GH Actions; additionally publishes JUnit (`test-results/results.xml`) and a `playwright-results` build artifact (traces/videos/screenshots retained on failure).
- Secrets piped as `$(ADMIN_USERNAME)` / `$(ADMIN_PASSWORD)` pipeline variables.

## 9. Setup (Local)

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows
pip install -r requirements.txt
playwright install --with-deps
```

Create `.env` at the repo root:

```
ADMIN_USERNAME=tomsmith
ADMIN_PASSWORD=SuperSecretPassword!
```

(These are the public demo credentials for `the-internet.herokuapp.com`.)

## 10. Repo-Specific Gotchas

- **Platform mismatch.** The primary dev machine is **Windows** (`win32`), but CI runs on `ubuntu-latest`. Keep paths portable — use forward slashes or `pathlib`, not Windows backslashes, in any code that could run in CI.
- **`requirements.txt` is UTF-16 encoded on disk.** If you rewrite the file, preserve the encoding or `pip install` will fail on some setups. Prefer `Edit` over `Write` for changes.
- **`auth/auth.json` is generated.** A locally regenerated file will diff just because the session cookie changed — don't commit it as part of an unrelated change.
- **`__pycache__/` at the repo root is expected** (because `conftest.py` lives at the root). It's gitignored — leave it alone.
- **`Artifacts/`, `.idea/`, `.venv/`** — local-only, don't touch.
- **Tests hit live external sites.** Failures may be network/flakiness, not regressions. Before claiming a test is broken, run it again headed and look at what the site actually returned.

## 11. Things to Ask Before Doing

- Renaming or deleting any test file.
- Adding a new dependency.
- Re-enabling Azure Pipelines auto-triggers.
- Introducing a framework layer (POM, fixtures factory, base class).
- Switching to async Playwright.
- Changing CI triggers, runner OS, or Python version.