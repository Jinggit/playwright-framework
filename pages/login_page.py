from playwright.async_api import Page
from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username = '[name="name"]'
        self.password = '[name="user_pin"]'
        self.login_btn = '[name="commit"]'
        self.app_frame = "iframe#AppLandingPage"
        self.sales_app_text = "ICAO Sales App"
        self.cprm_app_text = "CPMR 2026-2028"

    async def open_login_page(self, base_url: str):
        """for login with username and password"""
        await self.goto(f"{base_url}/user/login")

    async def login(self, user: str, pwd: str):
        """login with username and password"""
        await self.page.fill(self.username, user)
        await self.page.fill(self.password, pwd)
        await self.click(self.login_btn)

    async def open_sales_app(self):
        """Enter Sales App"""
        frame = self.get_frame(self.app_frame)
        await frame.get_by_text(self.sales_app_text).click()

    async def open_cprm_app(self):
        """Enter CPRM App"""
        frame = self.get_frame(self.app_frame)
        await frame.get_by_text(self.cprm_app_text).first.click()


