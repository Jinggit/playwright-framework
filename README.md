# Playwright POM Automation Framework

This project is an end-to-end automation testing framework built with Playwright + Pytest + Page Object Model (POM), designed specifically for Dynamics 365 CRM.

Since CRM often uses MFA (Multi-Factor Authentication) (e.g., SMS, Authenticator app), direct username/password login automation is not feasible.
Instead, this framework uses Playwright’s storage state mechanism to persist a logged-in session (crm_state_qa.json, crm_state_stage.json, …).
The browser session is saved once (after completing MFA manually) and then reused for all automated test runs.

---

## Features
- **UI Testing for Dynamics 365 CRM**
- **MFA-friendly login (via storage_state JSON)**
- **Page Object Model (POM) for maintainable design**
- **API Testing with requests**
- **Database Validation with MySQL**
- **Multi-environment support (--env=qa/staging/prod)**
- **Reports: JUnit XML, pytest-html, Allure, Playwright trace**

## How MFA Login is Handled

**1. Run once manually with MFA**
```
python save_login.py --env=qa
```

This script launches a headed browser (--headed), opens Dynamics 365 CRM, you log in manually with MFA.
After successful login, Playwright saves cookies + storage into crm_state_qa.json.

**2. Subsequent test runs reuse session**

In tests, the page fixture loads this saved state:

```
context = await browser.new_context(storage_state="crm_state_qa.json")
```

This bypasses MFA and allows automation to run in a logged-in session.



## Project Structure
```bash
playwright-framework/
│── configs/ # Environment configs
│ ├── qa.json
│ ├── staging.json
│ └── prod.json
│── conftest.py # Pytest fixtures
│── pages/                  # Page Object Model classes
│   ├── base_page.py        # BasePage (common actions)
│   ├── login_page.py       # Login page / Sales App actions
│   └── dashboard_page.py   # Dashboard + assertions
│── tests/                  # Test suites
│   └── test_edit_opportunity_success.py       # Example CRM login + validation
│── utils/                  # Helpers
│   ├── config_loader.py    # Loads configs (qa/staging/prod)
│   ├── db_utils.py         # Database helper
│   └── api_utils.py        # API helper
│── reports/                # HTML/XML reports
│── crm_state_qa.json       # Saved login session (MFA passed)
│── crm_state_stage.json    # Saved login session (MFA passed)
│── conftest.py             # Pytest fixtures (env, page, config)
│── requirements.txt        # Dependencies
│── save_login.py           # Script to save login state after MFA
│── pytest.ini              # Pytest config
│── README.md               # Documentation

```
## Install dependencies

pip install -r requirements.txt

playwright install

## Running Tests

pytest -v --env=qa

pytest --headed

# Locator Comparison Across Frameworks

## Framework Differences

| Framework | Locator methods | Key features | Example |
|-----------|----------------|--------------|---------|
| ***Cypress*** | `cy.get()`, `cy.contains()`, `cy.xpath()` (via plugin) | Chainable, auto-retry, best with CSS selectors | `cy.get('input[name="username"]')`<br>`cy.contains('Login')` |
| ***Robot Framework SeleniumLibrary*** | Keyword + locator strategy (`id=`, `name=`, `css=`, `xpath=`) | Human-readable, supports multiple locator types | `Input Text    id=username    jingghster`<br>`Click Button   xpath=//button[@id="login"]` |
| ***Playwright*** | `page.locator()`, `page.get_by_*` | Built-in ***strict mode*** (unique matches), powerful selector API, auto-waiting | `page.locator('#username').fill('jingghster')`<br>`page.get_by_role("button", name="Login").click()` |

## Example: Fill username + password + click login

### Cypress
```javascript
cy.get('input[name="name"]').type('jingghster')
cy.get('input[name="user_pin"]').type('2566')
cy.contains('Login').click()

```
### Robot Framework
```bash
Input Text    name=username    jingghster
Input Text    name=user_pin    2566
Click Button  xpath=//button[@name="commit"]

```
### Playwright (Python)
```python
page.locator('input[name="name"]').fill("jingghster")
page.locator('input[name="user_pin"]').fill("2566")
page.get_by_role("button", name="commit").click()