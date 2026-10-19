import allure
import pytest

from common.config import Config
from common.http_client import ApiClient


@pytest.fixture(scope="module")
def client():
    return ApiClient(Config.BJDKY_BASE_URL)


@allure.feature("登录")
def test_login_success(client):
    data = {"userName": Config.BJDKY_USERNAME, "password": Config.BJDKY_PASSWORD}
    response = client.post("login", json=data)
    assert response.status_code == 200


@allure.feature("不存在用户登录")
def test_login_inexistentUser(client):
    data = {"userName": "YW123", "password": Config.BJDKY_PASSWORD}
    response = client.post("login", json=data)
    assert "用户名不存在" in response.text


@allure.feature("错误密码登录")
def test_login_errorPwd(client):
    data = {"userName": Config.BJDKY_USERNAME, "password": "1234"}
    response = client.post("login", json=data)
    assert "密码错误" in response.text


@allure.feature("退出登录")
def test_loginout(client, bjdky_get_authorization):
    headers = {"authorization": bjdky_get_authorization}
    response = client.post("logout", headers=headers)
    assert "用户已注销" in response.text
