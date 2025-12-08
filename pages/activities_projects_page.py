from utils.db_utils import query_db
from playwright.async_api import Page
from pages.base_page import BasePage

class ActivitiesPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.activities_text = "text=Activities & Projects"

    async def go_to_activities(self):
        """Enter Activities & Projects"""
        await self.wait_for_selector(self.activities_text, state="visible")
        await self.click(self.activities_text)
