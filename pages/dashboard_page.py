class DashboardPage:
    def __init__(self, page):
        self.page = page
        self.user_card = '[data-js="user_card"]'

    def get_username(self):
        return self.page.text_content(self.user_card)
