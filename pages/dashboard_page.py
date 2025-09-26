from utils.db_utils import query_db
from playwright.async_api import Page
from pages.base_page import BasePage

class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.opportunities_text = "text=Opportunities"
        self.user_card = '[data-js="user_card"]'

    async def go_to_opportunities(self):
        """Enter Opportunities"""
        await self.wait_for_selector(self.opportunities_text, state="visible")
        await self.click(self.opportunities_text)

    async def get_username(self):
        return self.page.text_content(self.user_card)

    async def should_see_username(self, expected):
        actual = self.get_username()
        assert expected in actual, f"Expected {expected}, but got {actual}"

    async def user_exists_in_db(self, username, config):
        sql = "SELECT * FROM users WHERE username=%s"
        result = query_db(sql, config, (username,))
        return len(result) > 0
