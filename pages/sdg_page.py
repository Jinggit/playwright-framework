from playwright.async_api import Page
from pages.base_page import BasePage

class SDGPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.sdg_menu = "text=SDGs"

    async def go_to_sdgs(self):
        """Enter SDGs menu"""
        await self.wait_for_selector(self.sdg_menu, state="visible")
        await self.click(self.sdg_menu)
