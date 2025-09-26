from playwright.async_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    async def goto(self, url: str):
        await self.page.goto(url)

    async def click(self, locator: str):
        await self.page.click(locator)

    async def wait_for_selector(self, locator: str, state="visible", timeout=10000):
        await self.page.wait_for_selector(locator, state=state, timeout=timeout)

    def get_frame(self, locator: str):
        return self.page.frame_locator(locator)
