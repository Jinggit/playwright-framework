import pytest
import random
from playwright.async_api import expect

from pages.login_page import LoginPage
from pages.output_page import OutputPage
from pages.base_page import BasePage


@pytest.mark.asyncio
async def test_new_output(page, config):
    """
    Test Objective:
    Verify that a user can successfully create a new Output in CPMR (2026–2028).
    """
    outcome = "A1"
    output_manager = "# 1T Everaldo (ICA)"
    officer_in_charge = "# 1T Everaldo (ICA)"

    def generate_xyz_code():
        x = random.randint(1, 9)
        y = random.randint(1, 9)
        z = random.randint(1, 9)
        return f"{x}.{y}.{z}"

    n = generate_xyz_code()
    # Generate test data
    output_code = f"A{n}"
    output_name = f"QA Output {n}"

    # Step 1: Navigate to the CRM login page
    await page.goto(config["baseUrl"])
    base_page = BasePage(page)
    login_page = LoginPage(page)
    output_page = OutputPage(page)

    # Step 2: Open CPMR app and navigate to Outputs
    await login_page.open_cprm_app()
    await output_page.go_to_outputs()
    await expect(page.get_by_role("button", name="Active Outputs")).to_be_visible()

    # Step 3: Click "New"
    await page.locator("button[aria-label='New']").click()

    # Step 4: Select Outcome
    await page.get_by_role("button", name="Search records for Outcome, Lookup field").click()
    await page.get_by_role("treeitem").filter(has_text=outcome).click()

    # Step 5: Fill Output Code
    await page.get_by_label("Output Code").fill(output_code)

    # Step 6: Fill Output
    await page.locator("textarea[aria-label='Output']").fill(output_name)

    # Step 7: Select Output Manager
    await page.get_by_role("button", name="Search records for Output Manager, Lookup field").click()
    await page.get_by_role("treeitem").filter(has_text=output_manager).click()

    # Step 8: Select Officer in Charge
    await page.get_by_role("button", name="Search records for Officer In Charge, Lookup field").click()
    await page.get_by_role("treeitem").filter(has_text=officer_in_charge).click()

    # Step 9: Save
    await page.locator("xpath=(//button[contains(@title,'Save (CTRL+S)')])[1]").click()

    # Step 10: Go back to list
    await page.click("button[title='Go back']")

    # Step 11: Validate creation
    filter_box = page.get_by_placeholder("Filter by keyword")
    await filter_box.fill(output_code)
    await filter_box.press("Enter")

    result = page.get_by_text(output_code, exact=True)
    await expect(result.first).to_be_visible()

    print(f"Output created successfully: {output_code} | {output_name}")
