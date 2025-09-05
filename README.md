# Playwright POM Automation Framework

This project is an **end-to-end automation framework** using **Playwright + Pytest + Page Object Model (POM)**.  
It demonstrates **UI, API, and DB validation** in one place, with support for multiple environments (qa, staging, prod).  

---

## Features

- **UI testing** with Playwright (auto-waiting, cross-browser)  
- **API testing** with Requests  
- **Database validation** with MySQL connector  
- **Page Object Model (POM)** for maintainable design  
- **Multi-environment support** (`--env=qa/staging/prod`)  
- **Reports**: JUnit XML, pytest-html, Allure, Playwright trace  

![Login page screenshot](demo.GIF)
---

## Project Structure
```bash
playwright-framework/
│── tests/ # Test suites
│ └── test_login.py # Example: UI + DB validation
│
│── pages/ # Page Object Model (POM)
│ ├── login_page.py # Login page actions
│ └── dashboard_page.py # Dashboard assertions + DB check
│
│── utils/ # Helpers
│ ├── api_utils.py # API requests
│ ├── db_utils.py # DB queries
│ └── config_loader.py # Load env configs
│
│── configs/ # Environment configs
│ ├── qa.json
│ ├── staging.json
│ └── prod.json
│
│── conftest.py # Pytest fixtures (env, page, config)
│── requirements.txt # Python dependencies
│── README.md


```
## Install dependencies

pip install -r requirements.txt

playwright install

## Running Tests

pytest -v --env=qa

pytest --headed

