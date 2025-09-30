import pytest
from playwright.async_api import expect

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.base_page import BasePage

@pytest.mark.asyncio
async def test_login_success(page, config):
    await page.goto(config["baseUrl"])
    base_page = BasePage(page)
    login_page = LoginPage(page)
    dashboard = DashboardPage(page)

    await login_page.open_sales_app()
    await dashboard.go_to_opportunities()

    # assert
    await expect(page.locator("h1:has-text('My Open Opportunities')")).to_be_visible()

    first_row = page.locator("div[role='row']").nth(1)
    await first_row.dblclick()

    await base_page.safe_scroll_into_view("div[role='tabpanel'][aria-label='Summary']")

    checkbox = page.get_by_label("Air Transport & Economic Planning")
    await checkbox.click(force=True)
    await page.locator("xpath=(//button[contains(@title,'Save (CTRL+S)')])[1]").click()
    await page.click("button[title='Go back']")

    # assert
    first_row = page.locator("div[role='row']").nth(1)
    await first_row.dblclick()


    await base_page.safe_scroll_into_view("div[role='tabpanel'][aria-label='Summary']")
    await expect(page.get_by_label("Air Transport & Economic Planning")).to_be_checked(timeout=60000)

    checkbox = page.get_by_label("Air Transport & Economic Planning")
    await checkbox.click(force=True)
    await page.locator("xpath=(//button[contains(@title,'Save (CTRL+S)')])[1]").click()