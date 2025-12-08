import pytest
import random
from playwright.async_api import expect

from pages.login_page import LoginPage
from pages.outcome_page import OutcomePage
from pages.base_page import BasePage


@pytest.mark.asyncio
async def test_new_outcome(page, config):
    """
    Test Objective:
    Verify that a user can successfully create a new Outcome
    in CPMR (CPMR 2026–2028).
    """

    # --- Test Data ---------------------------------------------------------
    outcome_code = f"A{random.randint(1, 999)}"
    outcome_name = f"QA-Outcome-{random.randint(1, 999)}"
    strategic_goal = "Q5"

    # --- Step 1: Navigate to CRM -------------------------------------------
    await page.goto(config["baseUrl"])
    base_page = BasePage(page)
    login_page = LoginPage(page)
    outcome_page = OutcomePage(page)

    # --- Step 2: Open CPMR App → Outcomes ----------------------------------
    await login_page.open_cprm_app()
    await outcome_page.go_to_outcomes()

    await expect(
        page.get_by_role("button", name="Active Outcome")
    ).to_be_visible()

    # --- Step 3: Click New --------------------------------------------------
    await page.locator("button[aria-label='New']").click()

    # --- Step 4: Select Strategic Goal (lookup) -----------------------------
    await page.get_by_role(
        "button",
        name="Search records for Strategic Goal, Lookup field"
    ).click()

    # Select first available strategic goal
    await page.get_by_role("treeitem").filter(has_text=strategic_goal).click()

    # --- Step 5: Fill Outcome Code ------------------------------------------
    await page.get_by_label("Outcome Code").fill(outcome_code)

    # --- Step 6: Fill Outcome Name -----------------------------------------
    await page.locator("textarea[aria-label='Outcome']").fill(outcome_name)

    # --- Step 7: Save -------------------------------------------------------
    await page.locator("xpath=(//button[contains(@title,'Save')])[1]").click()

    # --- Step 8: Go back to list -------------------------------------------
    await page.click("button[title='Go back']")

    # --- Step 9: Validate created outcome ----------------------------------
    filter_box = page.get_by_placeholder("Filter by keyword")
    await filter_box.fill(outcome_code)
    await filter_box.press("Enter")

    created_row = page.get_by_text(outcome_code, exact=True)
    await expect(created_row.first).to_be_visible()

    print(f"Outcome created: Code={outcome_code}, Name={outcome_name}")
