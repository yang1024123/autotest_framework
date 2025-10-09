import requests
import json
import allure
import pytest
from requests.exceptions import RequestException

@pytest.mark.flaky(reruns=3, reruns_delay=2)
@allure.feature("登录")
def test_login_success():
    raw_data = '{"userName":"yw","password":"7c9a8efe507000abacdd433dc95645b9"}'
    data = json.loads(raw_data)

    url = "http://10.10.106.250:19971/login"
    try:
        response = requests.post(url=url, json=data, timeout=10)
        assert response.status_code == 200
    except RequestException as e:
        pytest.skip(f"API不可达: {str(e)}")
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@allure.feature("不存在用户登录")
def test_login_inexistentUser():
    raw_data = '{"userName":"YW123","password":"7c9a8efe507000abacdd433dc95645b9"}'
    data = json.loads(raw_data)

    url = "http://10.10.106.250:19971/login"
    try:
        response = requests.post(url=url, json=data, timeout=10)
        assert "用户名不存在" in response.text
    except RequestException as e:
        pytest.skip(f"API不可达: {str(e)}")
@pytest.mark.flaky(reruns=3, reruns_delay=2)
@allure.feature("错误密码登录")
def test_login_errorPwd():
    raw_data = '{"userName":"yw","password":"1234"}'
    data = json.loads(raw_data)

    url = "http://10.10.106.250:19971/login"
    try:
        response = requests.post(url=url, json=data, timeout=10)
        assert "密码错误" in response.text
    except RequestException as e:
        pytest.skip(f"API不可达: {str(e)}")


@pytest.mark.flaky(reruns=3, reruns_delay=2)
@allure.feature("退出登录")
def test_loginout(bjdky_get_authorization):
    url = "http://10.10.106.250:19971/logout"
    headers = {
        'authorization': bjdky_get_authorization
    }

    try:
        response = requests.post(url=url, headers=headers, timeout=10)
        assert "用户已注销" in response.text
    except RequestException as e:
        pytest.skip(f"API不可达: {str(e)}")