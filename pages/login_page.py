class LoginPage:
    def __init__(self, page):
        self.page = page
        self.username = '[name="name"]'
        self.password = '[name="user_pin"]'
        self.login_btn = '[name="commit"]'

    def open(self, base_url):
        self.page.goto(f"{base_url}/user/login")

    def login(self, user, pwd):
        self.page.fill(self.username, user)
        self.page.fill(self.password, pwd)
        self.page.click(self.login_btn)
