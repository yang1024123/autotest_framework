import pytest
from page_objects.login_page import LoginPage


def test_valid_login(setup_driver):
    login_page = LoginPage(setup_driver)
    login_page.navigate()
    login_page.login("cs001", "Hmdz1234.")
    assert login_page.is_logged_in(), "Login failed"

def test_invalid_login(setup_driver):
    login_page = LoginPage(setup_driver)
    login_page.navigate()
    login_page.login("invalid_", "wrong_password")
    assert "用户名或密码错误" in login_page.get_error_message(), "Error message not displayed"
