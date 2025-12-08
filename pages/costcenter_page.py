from playwright.async_api import Page, expect

class CostCenterPage:
    def __init__(self, page: Page):
        self.page = page

    # Navigation
    async def go_to_cost_centers(self):
        """Navigate to Cost Centers list page"""
        await self.page.get_by_text("Cost Centers", exact=True).click()
