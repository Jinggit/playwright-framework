import pytest
from playwright.async_api import expect

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

@pytest.mark.asyncio
async def test_login_success(page, config):
    await page.goto(config["baseUrl"])

    login_page = LoginPage(page)
    dashboard = DashboardPage(page)

    await login_page.open_sales_app()
    await dashboard.go_to_opportunities()


    # assert
    await expect(page.locator("h1:has-text('My Open Opportunities')")).to_be_visible()