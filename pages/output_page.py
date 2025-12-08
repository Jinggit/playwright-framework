from utils.db_utils import query_db
from playwright.async_api import Page
from pages.base_page import BasePage

class OutputPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    async def go_to_outputs(self):
        """Navigate to Outputs in left navigation pane"""
        output_nav = self.page.get_by_role("treeitem", name="Outputs")
        await output_nav.wait_for(state="visible")
        await output_nav.click()
