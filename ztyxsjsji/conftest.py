import json

import requests
import pytest
import allure

def get_authorization():
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

@pytest.fixture(scope='function',autouse=True)
def get_fileDocId():
    headers = {
        'authorization': get_authorization(),
        'Content-Type': 'application/json;charset=UTF-8',
    }
    data = {"caseType":0,"name":"这是案例333","faultLastTime":41}
    url = "http://10.10.106.250:19971/caseRule/svg-list/by-fault-type"
    try:
        response = requests.post(url=url, json=data,headers=headers)
        response_dict = response.json()
        file_doc_ids = ""
        for item in response_dict['data']:
            file_doc_ids += "," + item["fileDocId"]
        return file_doc_ids
    except requests.exceptions.RequestException as e:
        allure.attach(f"Request failed: {e}", name="Error Log")
        return None
def get_caseid():
    headers = {
        'authorization': get_authorization(),
        'Content-Type': 'application/json;charset=UTF-8',
    }
    data = {"current":1,"size":20}
    url = "http://10.10.106.250:19971/caseRule/page"
    try:
        response = requests.post(url=url, json=data, headers=headers)
        response_dict = response.json()
        case_id = response_dict['data']['records'][0].get("id")
        return case_id
    except requests.exceptions.RequestException as e:
        allure.attach(f"Request failed: {e}", name="Error Log")
        return None


@pytest.fixture(scope='function')
def setup_addcase(get_fileDocId):
    print('setup开始')
    url = "http://10.10.106.250:19971/caseRule/add"
    headers = {
        'authorization': get_authorization()
    }
    raw_data = {"caseType": 0,
                "name": "这是案例名称333",
                "describes": "这是案例描述",
                "faultLastTime": 41,
                "faultIds": get_fileDocId
                }
    try:
        response = requests.post(url=url, json=raw_data, headers=headers)
        assert "保存成功" in response.text, f"Expected '保存成功' in response, but got: {response.text}"
    except requests.exceptions.RequestException as e:
        allure.attach(f"Request failed: {e}", name="Error Log")
        pytest.fail(f"Request to {url} failed with exception: {e}")


@pytest.fixture(scope='function')
def teardown_deletecase():
    yield
    print('teardown开始')
    url = "http://10.10.106.250:19971/caseRule/delete"
    headers = {
        'authorization': get_authorization()
    }
    raw_data = {"id": get_caseid()}
    try:
        response = requests.post(url=url, json=raw_data, headers=headers)
        assert "删除成功" in response.text
    except requests.exceptions.RequestException as e:
        allure.attach(f"Request failed: {e}", name="Error Log")
        pytest.fail(f"Request to {url} failed with exception: {e}")

