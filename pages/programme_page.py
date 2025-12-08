from utils.db_utils import query_db
from playwright.async_api import Page
from pages.base_page import BasePage

class ProgrammePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.activities_text = "text=Programmes"

    async def go_to_programmes(self):
        """Enter programmes"""
        await self.wait_for_selector(self.activities_text, state="visible")
        await self.click(self.activities_text)
