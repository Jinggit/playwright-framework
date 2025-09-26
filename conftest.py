import pytest
import pytest_asyncio
from utils.config_loader import load_config
from playwright.async_api import async_playwright

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="qa", help="Environment: qa/staging/prod")

@pytest.fixture(scope="session")
def config(request):
    env = request.config.getoption("--env")
    return load_config(env)

@pytest_asyncio.fixture
async def page(config, request):
    env = request.config.getoption("--env")
    state_file = f"crm_state_{env}.json"

    headed = request.config.getoption("--headed")
    headless = not headed
    browser_name = request.config.getoption("--browser") or "chromium"
    if isinstance(browser_name, list):
        browser_name = browser_name[0]

    async with async_playwright() as p:
        browser_launcher = getattr(p, browser_name)
        browser = await browser_launcher.launch(headless=headless)
        context = await browser.new_context(storage_state=state_file)
        page = await context.new_page()
        yield page
        await browser.close()
