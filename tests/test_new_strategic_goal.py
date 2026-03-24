import pytest
import random
from playwright.async_api import expect

from pages.login_page import LoginPage
from pages.strategic_goal_page import StrategicGoalPage
from pages.base_page import BasePage


@pytest.mark.asyncio
async def test_new_strategic_goal(page, config):
    """
    Test Objective:
    Verify that a user can successfully create a new Strategic Goal (SG)
    in CPMR (CPMR 2026-2028).
    """

    # Generate test data
    n = random.randint(1, 99)
    sg_code = f"Q{n}"
    sg_text = f"Strategic Goal Auto {n}"

    # Step 1: Navigate to CRM
    await page.goto(config["baseUrl"])

    base_page = BasePage(page)
    login_page = LoginPage(page)
    sg_page = StrategicGoalPage(page)

    # Step 2: Open CPMR App → Strategic Goals
    await login_page.open_cprm_app()
    await sg_page.go_to_strategic_goals()

    await expect(page.get_by_role("button", name="Active Strategic Goals")).to_be_visible()

    # Step 3: Click "New"
    await page.locator("button[aria-label='New']").click()

    # Step 4: Fill SG Code
    await page.get_by_label("SG Code").fill(sg_code)

    # Step 5: Fill Strategic Goal / Enabler
    await page.get_by_label("Strategic Goal / Enabler").fill(sg_text)

    # Step 6: Save
    await page.locator("xpath=(//button[contains(@title,'Save (CTRL+S)')])[1]").click()

    # Step 7: Go back to list
    await page.click("button[title='Go back']")

    # Step 8: Validate creation
    filter_box = page.get_by_placeholder("Filter by keyword")
    await filter_box.fill(sg_code)
    await filter_box.press("Enter")

    result = page.locator("[role='gridcell']").filter(has_text=sg_code).first
    await expect(result).to_be_visible()

    print(f"Strategic Goal created: SG Code={sg_code}, SG Text={sg_text}")
