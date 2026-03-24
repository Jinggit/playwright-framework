import pytest
from playwright.async_api import expect
import time

from pages.login_page import LoginPage
from pages.base_page import BasePage
from pages.costcenter_page import CostCenterPage
import random



@pytest.mark.asyncio
async def test_new_cost_center(page, config):
    """
    Test Objective:
    Verify that a user can successfully create a new Cost Center
    in the CPMR System.
    """

    # ------------ Test Data ------------
    timestamp = int(time.time())
    four_digits = random.randint(1000, 9999)
    cost_center_code = f"QA{four_digits}"
    cost_center_name = f"QA-CostCenter-{timestamp}"

    # ------------- Step 1: Open CRM -------------
    await page.goto(config["baseUrl"])
    base_page = BasePage(page)
    login_page = LoginPage(page)

    # ------------- Step 2: Open CPMR App -------------
    await login_page.open_cprm_app()

    # ------------- Step 3: Navigate to Cost Centers -------------
    costcenters_page = CostCenterPage(page)
    await costcenters_page.go_to_cost_centers()
    await expect(
        page.get_by_role("button", name="Active Cost Centers")
    ).to_be_visible()

    await expect(
        page.get_by_role("button", name="Active Cost Centers")
    ).to_be_visible()

    # ------------- Step 4: New Cost Center -------------
    await page.locator("button[aria-label='New']").click()

    # ----- Fill Fields -----
    await page.get_by_label("Cost Center Code").fill(cost_center_code)

    await page.locator("input[aria-label='Cost Center']").fill(cost_center_name)

    # ------------- Step 5: Save record -------------
    await page.locator("xpath=(//button[contains(@title,'Save')])[1]").click()

    await page.wait_for_timeout(2000)

    # ------------- Step 6: Go back to list view -------------
    await page.click("button[title='Go back']")

    # ------------- Step 7: Validate record exists -------------
    filter_box = page.get_by_placeholder("Filter by keyword")
    await filter_box.fill(cost_center_code)
    await filter_box.press("Enter")

    # --- Acceptable validation: Count ≥ 1 ---
    result = page.locator("[role='gridcell']").filter(has_text=cost_center_code).first
    await expect(result).to_be_visible()

    print(f"Cost Center created successfully: {cost_center_code}")
