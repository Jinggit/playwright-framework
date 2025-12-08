import pytest
from playwright.async_api import expect

from pages.login_page import LoginPage
from pages.opportunity_page import OpportunityPage
from pages.base_page import BasePage


@pytest.mark.asyncio
async def test_edit_opportunity_success(page, config):
    """
    Test Objective:
    Verify that a user can successfully log in to CRM and perform the following steps:
      1. Open the Sales App and navigate to the Opportunities list
      2. Double-click the first Opportunity to open its detail page
      3. In the Summary tab, check the "Air Transport & Economic Planning" checkbox
      4. Select "Provision of Expertise" and "Procurement of Goods & Services" from the Subcategory dropdown
      5. Save the record and return to the Opportunities list
      6. Re-open the same Opportunity and verify the checkbox remains checked
      7. Clean testdata: Remove Subcategory and Uncheck the checkbox and save again
    """

    # Step 1: Navigate to the CRM login page
    await page.goto(config["baseUrl"])
    base_page = BasePage(page)
    login_page = LoginPage(page)
    opportunity = OpportunityPage(page)

    # Step 2: Open Sales App and navigate to Opportunities
    await login_page.open_sales_app()
    await opportunity.go_to_opportunities()
    await expect(page.locator("h1:has-text('My Open Opportunities')")).to_be_visible()

    # Step 3: Double-click the first row to open Opportunity details
    first_row = page.locator("div[role='row']").nth(1)
    await first_row.dblclick()

    # Step 4: Scroll into Summary tab and check the checkbox
    await base_page.safe_scroll_into_view("div[role='tabpanel'][aria-label='Summary']")
    checkbox = page.get_by_label("Air Transport & Economic Planning")
    await checkbox.click(force=True)

    # Step 5: Open Subcategory dropdown and select multiple options
    input_box = page.locator("#icao_subcategory_ledit")
    caret_button = input_box.locator("xpath=../../..").locator("button.msos-caret-button")
    await caret_button.click()
    options = ["Provision of Expertise", "Procurement of Goods & Services"]
    for opt in options:
        await page.get_by_role("option", name=opt).click()
        await page.wait_for_timeout(2000)
    await page.keyboard.press("Escape")

    # Step 6: Save the record and return to the Opportunities list
    await page.locator("xpath=(//button[contains(@title,'Save (CTRL+S)')])[1]").click()
    await page.click("button[title='Go back']")

    # Step 7: Re-open the same record and verify checkbox is checked
    first_row = page.locator("div[role='row']").nth(1)
    await first_row.dblclick()
    await base_page.safe_scroll_into_view("div[role='tabpanel'][aria-label='Summary']")
    await expect(page.get_by_label("Air Transport & Economic Planning")).to_be_checked()

    # Step 8: Clean test, Remove Subcategory and Uncheck the checkbox Air Transport & Economic Planning and save again
    sibling = page.locator("//div[@title='Subcategory']/following-sibling::div[@role='presentation']")
    await sibling.hover()
    for opt in options:
        delete_button = page.locator("button.msos-quick-delete[aria-label='Remove " +opt +"']")
        await delete_button.click()
        await page.wait_for_timeout(2000)
    checkbox = page.get_by_label("Air Transport & Economic Planning")
    await checkbox.click(force=True)
    await page.locator("xpath=(//button[contains(@title,'Save (CTRL+S)')])[1]").click()
