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
    activity_manager = "# 1T Everaldo (ICA)"
    cost_center = "C1010"
    origin_of_decision = "Council"
    sequence_number = "5"
    type = "Activity"
    start = "12/4/2025"
    end = "12/4/2026"
    activity = f"QA-{int(time.time())}"
    programme = "P1"
    sdg_number = "2"
    funding = "Unfunded"
    funding_source = "QA"
    schedule = "Must be scheduled"
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

    # set SDG
    sdg_lookup = page.get_by_label("SDG, Lookup", exact=True)
    await sdg_lookup.click()
    await sdg_lookup.press("Enter")
    sdg_option = page.get_by_role("treeitem").filter(has_text=sdg_number).first
    await expect(sdg_option).to_be_visible()
    await sdg_option.click()

    # set Activity Manager
    await page.get_by_role("button", name="Search records for Activity Manager, Lookup field").click()
    await page.get_by_role("treeitem").filter(has_text=activity_manager).first.click()
    await page.keyboard.press("Escape")

    # set start date
    await page.get_by_label("Start Date").fill(start)
    await page.get_by_label("Start Date").press("Tab")

    # set end date
    await page.get_by_label("End Date").fill(end)
    await page.get_by_label("End Date").press("Tab")

    # set Programme
    await page.get_by_role("button", name="Search records for Programme, Lookup field").click()
    await page.locator("div[role='presentation']").filter(has_text=programme).first.click()



    # Open lookup search popup and set Cost Center
    await page.get_by_role("button", name="Search records for Cost Center, Lookup field").click()
    await page.locator("div[role='presentation']").filter(has_text=cost_center).first.click()
    await page.keyboard.press("Escape")

    # set Funding
    await page.wait_for_timeout(3000)
    await page.get_by_role("combobox", name="Funding").click()
    await page.get_by_role("option", name=funding).click()

    # input Funding Source
    funding_source_field = page.get_by_label("Funding Source")
    if await funding_source_field.count():
        await funding_source_field.fill(funding_source)

    # set Schedule
    await page.get_by_role("combobox", name="Schedule").click()
    dropdown = page.get_by_role("listbox")
    await expect(dropdown).to_be_visible()
    await page.get_by_role("option", name=re.compile(re.escape(schedule), re.IGNORECASE)).first.click()

    # set Pillar
    await page.get_by_role("combobox", name="Pillar").click()
    dropdown = page.get_by_role("listbox")
    await expect(dropdown).to_be_visible()
    await page.get_by_role("option", name=re.compile(rf"^{re.escape(pillar)}$", re.IGNORECASE)).click()

    # set Gender
    await page.get_by_role("combobox", name="Gender").click()
    dropdown = page.get_by_role("listbox")
    await expect(dropdown).to_be_visible()
    await page.get_by_role("option", name=re.compile(re.escape("GEM 1"), re.IGNORECASE)).first.click()

    # set Traceability Status
    await page.get_by_role("combobox", name="Traceability Status").click()
    dropdown = page.get_by_role("listbox")
    await expect(dropdown).to_be_visible()
    await page.get_by_role("option", name=re.compile(rf"^{re.escape(traceability_status)}$", re.IGNORECASE)).click()

    # input Traceability Ref ID
    await page.get_by_label("Traceability Ref ID").fill(traceability_ref_id)

    # set Origin of Decision
    await page.get_by_role("combobox", name="Origin of Decision").click()
    dropdown = page.get_by_role("listbox")
    await expect(dropdown).to_be_visible()
    await page.get_by_role("option", name=re.compile(rf"^{re.escape(origin_of_decision)}$")).click()

    # input Decision Ref
    await page.get_by_label("Decision Ref").fill(decision_ref)

    # set Audit Recommendation
    await page.get_by_role("combobox", name="Audit Recommendation").click()
    dropdown = page.get_by_role("listbox")
    await expect(dropdown).to_be_visible()
    await page.get_by_role("option", name=re.compile(rf"^{re.escape(audit_recommendation)}$", re.IGNORECASE)).click()

    # set Corporate Risk
    await page.get_by_role("combobox", name="Corporate Risk").click()
    dropdown = page.get_by_role("listbox")
    await expect(dropdown).to_be_visible()
    await page.get_by_role("option", name=re.compile(rf"^{re.escape(corporate_risk)}$", re.IGNORECASE)).click()

    # set Category
    await page.get_by_role("combobox", name="Category").click()
    dropdown = page.get_by_role("listbox")
    await expect(dropdown).to_be_visible()
    await page.get_by_role("option", name=re.compile(re.escape("Cat 2"), re.IGNORECASE)).first.click()

    # input Priority Score
    priority_score = str(random.randint(1, 100))
    priority_score_field = page.get_by_label("Priority Score")
    if await priority_score_field.count():
        await priority_score_field.fill(priority_score)

    # input Priority
    priority = str(random.randint(1, 500))
    priority_field = page.get_by_label("Priority").nth(1)
    if await priority_field.count():
        await priority_field.fill(priority)

    # Save the record and return to the Activities list
    await page.locator("xpath=(//button[contains(@title,'Save (CTRL+S)')])[1]").click()
    await page.wait_for_timeout(3000)
    await page.click("button[title='Go back']")

    # Validate
    filter_box = page.get_by_placeholder("Filter by keyword")
    await expect(filter_box).to_be_visible()
    await filter_box.fill(activity)
    await filter_box.press("Enter")
    locator = page.locator("[role='gridcell']").filter(has_text=activity).first
    await expect(locator).to_be_visible()
