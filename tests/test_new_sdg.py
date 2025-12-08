import pytest
import random
from playwright.async_api import expect

from pages.login_page import LoginPage
from pages.sdg_page import SDGPage
from pages.base_page import BasePage


@pytest.mark.asyncio
async def test_new_sdg(page, config):
    """
    Test Objective:
    Verify that a user can successfully create a new SDG (Sustainable Development Goal)
    in CPMR (CPMR 2026-2028).
    """

    # Generate test data
    sdg_number = random.randint(1, 17)                # SDG Number (1–999)
    sdg_name = f"QA-SDG-{random.randint(1000, 9999)}"  # Random SDG Name

    # Step 1: Navigate to CRM
    await page.goto(config["baseUrl"])

    base_page = BasePage(page)
    login_page = LoginPage(page)
    sdg_page = SDGPage(page)

    # Step 2: Open CPMR App → SDGs
    await login_page.open_cprm_app()
    await sdg_page.go_to_sdgs()

    await expect(page.get_by_role("button", name="Active SDGs")).to_be_visible()

    # Step 3: Click "New"
    await page.locator("button[aria-label='New']").click()

    # Step 4: Fill SDG Number
    await page.get_by_label("SDG Number").fill(str(sdg_number))

    # Step 5: Fill Strategic Development Goal
    await page.get_by_label("Strategic Development Goal").fill(sdg_name)

    # Step 6: Save
    await page.locator("xpath=(//button[contains(@title,'Save (CTRL+S)')])[1]").click()

    # Step 7: Go back to list
    await page.click("button[title='Go back']")


    # Step 8: Validate creation
    filter_box = page.get_by_placeholder("Filter by keyword")
    await filter_box.fill(sdg_name)
    await filter_box.press("Enter")
    result = page.get_by_text(sdg_name, exact=True)
    await expect(result.first).to_be_visible()

    print(f"SDG created: Number={sdg_number}, Name={sdg_name}")
