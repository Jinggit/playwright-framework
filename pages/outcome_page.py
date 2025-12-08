from utils.db_utils import query_db
from playwright.async_api import Page
from pages.base_page import BasePage

class OutcomePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.menu_outcomes = self.page.get_by_role("treeitem", name="Outcomes")

    async def go_to_outcomes(self):
        await self.menu_outcomes.click()
