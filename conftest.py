import requests
import allure
import pytest


@pytest.fixture(scope='function')
def bjdky_get_authorization():
    data = {"userName": "yw", "password": "7c9a8efe507000abacdd433dc95645b9"}
    url = "http://10.10.106.250:19971/login"
    try:
        response = requests.post(url=url, json=data)
        response.raise_for_status()
        json_dict = response.json()
        authorization = json_dict['data']
        return authorization
    except requests.exceptions.RequestException as e:
        allure.attach(f"Request failed: {e}", name="Error Log")
        return None
@pytest.fixture(scope='function')
def xjdz_get_token():
    data = {"data" :{"userAccount": "cs001", "passWord": "b73418389083e301e7458d1ceff85d10", "token": "null"}}
    url = "http://10.10.106.250:37110/pwapp/common/getToken"
    try:
        response = requests.post(url=url, json=data)
        response.raise_for_status()
        json_dict = response.json()
        token = json_dict["data"]["token"]
        return token
    except requests.exceptions.RequestException as e:
        allure.attach(f"Request failed: {e}", name="Error Log")
        return None
@pytest.fixture(scope='function')
def xingbo_get_token():
    data = {"account": "SystemUser000", "password": "Xhdl@20250228"}
    url = "http://10.10.106.250:29999/api/auth/login"
    try:
        response = requests.post(url=url, json=data)
        response.raise_for_status()
        json_dict = response.json()
        token = json_dict["data"]["token"]['accessToken']
        tokenType = json_dict["data"]["token"]["tokenType"]
        return tokenType + " " + token
    except requests.exceptions.RequestException as e:
        allure.attach(f"Request failed: {e}", name="Error Log")
        return None
