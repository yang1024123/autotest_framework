from datetime import datetime

import pytest
import requests
import allure

@allure.feature("规则案例构建-按故障持续时间分类")
def test_caseBuild_duration(teardown_deletecase,bjdky_get_authorization,get_fileDocId):
    url = "http://10.10.106.250:19971/caseRule/add"
    headers = {
        'authorization': bjdky_get_authorization
    }
    raw_data = {"caseType":0,
                "name":"这是案例名称333",
                "describes":"这是案例描述",
                "faultLastTime":41,
                "faultIds": get_fileDocId
                }
    try:
        response = requests.post(url=url, json=raw_data, headers=headers)
        assert "保存成功" in response.text, f"Expected '保存成功' in response, but got: {response.text}"
    except requests.exceptions.RequestException as e:
        allure.attach(f"Request failed: {e}", name="Error Log")
        pytest.fail(f"Request to {url} failed with exception: {e}")

@allure.feature("案例删除")
def test_deleteCase(setup_addcase,teardown_deletecase):
    print("执行通过")