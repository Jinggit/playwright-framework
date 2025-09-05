from utils.db_utils import query_db

class DashboardPage:
    def __init__(self, page):
        self.page = page
        self.user_card = '[data-js="user_card"]'

    def get_username(self):
        return self.page.text_content(self.user_card)

    def should_see_username(self, expected):
        actual = self.get_username()
        assert expected in actual, f"Expected {expected}, but got {actual}"

    def user_exists_in_db(self, username, config):
        sql = "SELECT * FROM users WHERE username=%s"
        result = query_db(sql, config, (username,))
        return len(result) > 0
