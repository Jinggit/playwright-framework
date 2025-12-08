from pages.base_page import BasePage
from playwright.async_api import Page

class StrategicGoalPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.menu_text = "text=Strategic Goals"

    async def go_to_strategic_goals(self):
        await self.wait_for_selector(self.menu_text, state="visible")
        await self.click(self.menu_text)
