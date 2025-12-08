import pytest
from playwright.async_api import expect

from pages.login_page import LoginPage
from pages.activities_projects_page import ActivitiesPage
from pages.base_page import BasePage
import re
import random
import time


@pytest.mark.asyncio
async def test_new_activity_project(page, config):
    """
    Test Objective:
    Verify that a user can successfully log in to CPRM and perform the following steps:
    Modify Active Activities (Origin of Decision, Cost Center)
    """
    #data
    output = "A1.1"
    cost_center = "C1010"
    origin_of_decision = "Council"
    sequence_number = "5"
    type = "Activity"
    start = "12/4/2025"
    end = "12/4/2026"
    activity = f"QA-{int(time.time())}"
    programme = "P1"
    SDG = "End poverty in all its forms everywhere"
    funding = "Unfunded"
    funding_source = "QA"
    schedule = "Must be scheduled in first"
    pillar = "Auditing"
    gender = "GEM 1 – Some gender elements"
    traceability_status = "Modified"
    traceability_ref_id = "QA"
    decision_ref = "QA"
    audit_recommendation = "Low"
    corporate_risk = "High"
    category = "Cat 2: Supporting Enablers: Secretariat operational ongoing support"

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

    # Step 3: New
    await page.locator("button[aria-label='New']").click()

    # set Output
    await page.get_by_role("button", name="Search records for Output, Lookup field").click()
    await page.locator("div[role='presentation']").filter(has_text=output).first.click()

    # input Sequence Number
    await page.get_by_label("Sequence Number").fill(sequence_number)

    # set type
    await page.wait_for_timeout(3000)
    await page.get_by_role("combobox", name="Type").click()
    await page.get_by_role("option", name=type).click()

    # input Activity/Project name
    await page.get_by_label("Activity/Project").fill(activity)

    # set start date
    await page.get_by_label("Start Date").fill(start)
    await page.get_by_label("Start Date").press("Tab")

    # set end date
    await page.get_by_label("End Date").fill(end)
    await page.get_by_label("End Date").press("Tab")

    # set Programme
    await page.get_by_role("button", name="Search records for Programme, Lookup field").click()
    await page.locator("div[role='presentation']").filter(has_text=programme).first.click()

    # set SDG
    await page.get_by_role("button", name="Search records for SDG, Lookup field").click()
    await page.locator("div[role='presentation']").filter(has_text=SDG).first.click()

    # Open lookup search popup and set Cost Center
    await page.get_by_role("button", name="Search records for Cost Center, Lookup field").click()
    await page.locator("div[role='presentation']").filter(has_text=cost_center).first.click()

    # set Funding
    await page.wait_for_timeout(3000)
    await page.get_by_role("combobox", name="Funding").click()
    await page.get_by_role("option", name=funding).click()

    # input Funding Source
    await page.get_by_label("Funding Source").fill(funding_source)

    # set Schedule
    await page.get_by_role("combobox", name="Schedule").click()
    dropdown = page.get_by_role("listbox")
    await expect(dropdown).to_be_visible()
    await page.get_by_role("option", name=schedule).click()

    # set Pillar
    await page.get_by_role("combobox", name="Pillar").click()
    dropdown = page.get_by_role("listbox")
    await expect(dropdown).to_be_visible()
    await page.get_by_role("option", name=pillar).click()

    # set Gender
    await page.get_by_role("combobox", name="Gender").click()
    dropdown = page.get_by_role("listbox")
    await expect(dropdown).to_be_visible()
    await page.get_by_role("option", name=gender).click()

    # set Traceability Status
    await page.get_by_role("combobox", name="Traceability Status").click()
    dropdown = page.get_by_role("listbox")
    await expect(dropdown).to_be_visible()
    await page.get_by_role("option", name=traceability_status).click()

    # input Traceability Ref ID
    await page.get_by_label("Traceability Ref ID").fill(traceability_ref_id)

    # set Origin of Decision
    await page.get_by_role("combobox", name="Origin of Decision").click()
    dropdown = page.get_by_role("listbox")
    await expect(dropdown).to_be_visible()
    await page.get_by_role("option", name=origin_of_decision).click()

    # input Decision Ref
    await page.get_by_label("Decision Ref").fill(decision_ref)

    # set Audit Recommendation
    await page.get_by_role("combobox", name="Audit Recommendation").click()
    dropdown = page.get_by_role("listbox")
    await expect(dropdown).to_be_visible()
    await page.get_by_role("option", name=audit_recommendation).click()

    # set Corporate Risk
    await page.get_by_role("combobox", name="Corporate Risk").click()
    dropdown = page.get_by_role("listbox")
    await expect(dropdown).to_be_visible()
    await page.get_by_role("option", name=corporate_risk).click()

    # set Category
    await page.get_by_role("combobox", name="Category").click()
    dropdown = page.get_by_role("listbox")
    await expect(dropdown).to_be_visible()
    await page.get_by_role("option", name=category).click()

    # input Priority Score
    priority_score = str(random.randint(1, 100))
    await page.get_by_label("Priority Score").fill(priority_score)

    # input Priority
    priority = str(random.randint(1, 500))
    await page.get_by_label("Priority").nth(1).fill(priority)

    # Save the record and return to the Activities list
    await page.locator("xpath=(//button[contains(@title,'Save (CTRL+S)')])[1]").click()
    await page.wait_for_timeout(3000)
    await page.click("button[title='Go back']")

    # Validate
    #filter_box = page.get_by_placeholder("Filter by keyword")
    #await filter_box.fill(activity)
    #await filter_box.press("Enter")
    await expect(
        page.get_by_role("button", name="Active Activities & Projects")
    ).to_be_visible()
    locator = page.get_by_text(activity, exact=True)
    await expect(locator).to_have_count(1)
