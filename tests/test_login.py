import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

def test_login_success(page, config):
    login_page = LoginPage(page)
    dashboard = DashboardPage(page)

    login_page.open(config["baseUrl"])
    login_page.login("jingghster", "2566")

    dashboard.should_see_username("jingghster")
    assert dashboard.user_exists_in_db("jingghster", config)