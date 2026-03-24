import pytest
from playwright.async_api import expect
import time
import random
import re

from pages.login_page import LoginPage
from pages.base_page import BasePage
from pages.programme_page import ProgrammePage

@pytest.mark.asyncio
async def test_new_programme(page, config):
    """
    Test Objective:
    Verify that a user can successfully create a new Programme
    in the CPMR System.
    """

    # ------------ Test Data ------------
    programme_code = f"QA-CODE-{int(time.time())}"
    # unique programme name
    programme_name = f"QA-NAME-{int(time.time())}"

    start = "12/1/2025"
    end = "12/31/2025"

    # ------------- Step 1: Open CRM -------------
    await page.goto(config["baseUrl"])
    base_page = BasePage(page)
    login_page = LoginPage(page)


    # ------------- Step 2: Open CPMR App -------------
    await login_page.open_cprm_app()

    # ------------- Step 3: Navigate to Programmes -------------
    programme_page = ProgrammePage(page)
    await programme_page.go_to_programmes()
    await expect(
        page.get_by_role("button", name=re.compile(r"^Active Program"))
    ).to_be_visible()

    # ------------- Step 4: New Programme -------------
    await page.locator("button[aria-label='New']").click()

    # Programme code (text)
    await page.get_by_label("Programme Code").fill(programme_code)

    # Programme (text)
    await page.locator("textarea[aria-label='Programme']").fill(programme_name)

    # Start Date
    await page.get_by_label("Start Date").fill(start)
    await page.get_by_label("Start Date").press("Tab")

    # End Date
    await page.get_by_label("End Date").fill(end)
    await page.get_by_label("End Date").press("Tab")

    # Save
    await page.locator("xpath=(//button[contains(@title,'Save')])[1]").click()

    # Wait for auto code generation
    await page.wait_for_timeout(3000)

    # ------------- Step 5: Go back to Programme list -------------
    await page.click("button[title='Go back']")

    # ------------- Step 6: Validate programme exists -------------
    filter_box = page.get_by_placeholder("Filter by keyword")
    await filter_box.fill(programme_code)
    await filter_box.press("Enter")

    # Expected: programme name appears exactly once
    result = page.locator("[role='gridcell']").filter(has_text=programme_code).first
    await expect(result).to_be_visible()

    print(f"Programme created successfully: {programme_code}")
