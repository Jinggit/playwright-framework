import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.db_utils import query_db

def test_login_success(page, config):
    login_page = LoginPage(page)
    dashboard = DashboardPage(page)

    login_page.open(config["baseUrl"])
    login_page.login("jingghster", "2566")

    username = dashboard.get_username()
    assert "jingghster" in username

    result = query_db("SELECT * FROM users WHERE username='jingghster'", config)
    assert len(result) > 0