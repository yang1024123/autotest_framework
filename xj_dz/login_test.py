import pytest

from common.config import Config
from page_objects.login_page import LoginPage


def test_valid_login(setup_driver):
    login_page = LoginPage(setup_driver)
    login_page.navigate()
    login_page.login(Config.XJDZ_UI_USERNAME, Config.XJDZ_UI_PASSWORD)
    assert login_page.is_logged_in(), "登录成功提示未出现"


def test_invalid_login(setup_driver):
    login_page = LoginPage(setup_driver)
    login_page.navigate()
    login_page.login("invalid_", "wrong_password")
    assert "用户名或密码错误" in login_page.get_error_message(), "错误提示未显示"
