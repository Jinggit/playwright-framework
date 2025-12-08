import contextlib
from prometheus_client import Counter, Histogram, start_http_server
import time
import pytest
import pytest_asyncio
from utils.config_loader import load_config
from playwright.async_api import async_playwright


# Prometheus metrics
TESTS_TOTAL = Counter("pytest_tests_total", "Total number of executed tests", ["result"])
TEST_DURATION = Histogram("pytest_test_duration_seconds", "Test duration in seconds", ["test"])

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="stage", help="Environment: qa/staging/prod")

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
        browser = await browser_launcher.launch(headless=headless, channel="msedge")
        context = await browser.new_context(storage_state=state_file, viewport={"width": 1920, "height": 1080})
        page = await context.new_page()
        await page.set_viewport_size({"width": 1920, "height": 1080})
        page.set_default_timeout(60000)
        page.set_default_navigation_timeout(60000)
        try:
            yield page
        finally:
            with contextlib.suppress(Exception):
                await context.close()
            with contextlib.suppress(Exception):
                await browser.close()

# ---- Prometheus hooks ----
def pytest_sessionstart(session):
    start_http_server(8000)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    start = time.time()
    outcome = yield
    duration = time.time() - start

    TEST_DURATION.labels(test=item.name).observe(duration)

    if outcome.excinfo is None:
        TESTS_TOTAL.labels(result="passed").inc()
    else:
        TESTS_TOTAL.labels(result="failed").inc()