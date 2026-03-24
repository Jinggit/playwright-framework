import re

import pytest
from playwright.async_api import expect

from pages.login_page import LoginPage
from pages.activities_projects_page import ActivitiesPage
from pages.base_page import BasePage


@pytest.mark.asyncio
async def test_edit_activity_project(page, config):
    """
    Test Objective:
    Verify that a user can successfully log in to CPRM and perform the following steps:
    Modify Active Activities (Origin of Decision, Cost Center)
    """

    # test data
    output_code = "A1.1.1"

    # Step 1: Navigate to the CRM login page
    await page.goto(config["baseUrl"])
    base_page = BasePage(page)
    login_page = LoginPage(page)
    activities_page = ActivitiesPage(page)

    # Step 2: Open CPMR 2026-2028 App and navigate to Activities / Projects
    await login_page.open_cprm_app()
    await activities_page.go_to_activities()
    await expect(
        page.get_by_role("button", name="Active Activities & Projects")
    ).to_be_visible()

    filter_box = page.get_by_placeholder("Filter by keyword")
    await filter_box.fill(output_code)
    await filter_box.press("Enter")

    # Step 3: Double-click the first row to open Activity/project details
    first_row = page.locator("div[role='row']").nth(1)
    await first_row.dblclick()

    # Step 4: Modify the Origin of Decision
    await page.get_by_role("combobox", name="Origin of Decision").click()
    await page.get_by_role("option", name=re.compile(r"^Council$")).click(force=True)
    await page.get_by_label("Decision Ref").fill("QA")

    # Open lookup search popup and modify Cost Center
    await page.get_by_role("button", name="Search records for Cost Center, Lookup field").click()
    await page.locator("div[role='presentation']").filter(has_text="C1011").first.click()
    await page.keyboard.press("Escape")
    await page.wait_for_timeout(3000)

    # Step 5: Save the record and return to the Activities list
    await page.locator("xpath=(//button[contains(@title,'Save (CTRL+S)')])[1]").click()
    await page.click("button[title='Go back']")

    # Step 6: Re-open the same record and verify the change
    await page.keyboard.press("Escape")
    first_row = page.locator("div[role='row']").nth(1)
    await first_row.dblclick()
    field = page.get_by_role("combobox", name="Origin of Decision")
    await expect(field).to_have_text("Council")

    # Step 7: Reset the data back to its original state.
    await page.get_by_role("combobox", name="Origin of Decision").click()
    await page.get_by_role("option", name=re.compile(r"^Assembly$")).click(force=True)
    await page.get_by_label("Assembly").fill("QA")
    await page.get_by_role("button", name="Search records for Cost Center, Lookup field").click()
    await page.locator("div[role='presentation']").filter(has_text="C1010").first.click()
    await page.keyboard.press("Escape")
    await page.locator("xpath=(//button[contains(@title,'Save (CTRL+S)')])[1]").click()
    await page.click("button[title='Go back']")
