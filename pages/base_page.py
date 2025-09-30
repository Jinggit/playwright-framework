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

    async def safe_click(self,locator):
        try:
            await locator.click()
        except:
            await locator.scroll_into_view_if_needed()
            await locator.click(force=True)

    def get_frame(self, locator: str):
        return self.page.frame_locator(locator)

    async def safe_scroll_into_view(self,locator):
        container = self.page.locator(locator)
        await container.scroll_into_view_if_needed()
        box = await container.bounding_box()
        if box:
            await self.page.mouse.move(box["x"] + box["width"] / 2, box["y"] + 10)
            await self.page.mouse.wheel(0, box["height"])