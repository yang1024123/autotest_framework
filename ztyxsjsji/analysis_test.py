from datetime import datetime

import pytest
import requests
import allure


@allure.feature("按文件名称查询")
def test_filename_query(bjdky_get_authorization, api_base_url="http://10.10.106.250:19971"):
    API_URL = f"{api_base_url}/anyise/search"
    headers = {
        'authorization': bjdky_get_authorization
    }
    filename = "不接地"
    raw_data = {
        "commitCompany": None,
        "fileName": filename,
        "pageNum": 1,
        "pageSize": 20
    }

    try:
        response = requests.post(
            url=API_URL,
            json=raw_data,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        response_data = response.json()

        if not response_data or 'data' not in response_data:
            pytest.fail("Invalid response format")
        for item in response_data['data']['records']:
            assert filename in item['fileName'], f"{filename} not found in {item['fileName']}"

    except requests.exceptions.RequestException as err:
        error_msg = f"Request error occurred: {err}"
        allure.attach(error_msg, name="Request Error")
        pytest.fail(error_msg)


@allure.feature("按网省公司查询")
def test_province_query(bjdky_get_authorization):
    url = "http://10.10.106.250:19971/anyise/search"
    headers = {
        'authorization': bjdky_get_authorization
    }
    province = "110000"
    raw_data = {"provCompany": province, "commitCompany": None, "pageNum": 1, "pageSize": 20}
    try:
        response = requests.post(url=url, json=raw_data, headers=headers)
        response.raise_for_status()
        response_dict = response.json()
        for item in response_dict['data']['records']:
            item_province = item.get("provCompany")
            assert province == item_province
    except requests.exceptions.RequestException as e:
        allure.attach(f"Request failed: {e}", name="Error Log")
        pytest.fail(f"Request failed: {e}")


@allure.feature("按提交单位查询")
def test_commitCompany_query(bjdky_get_authorization):
    url = "http://10.10.106.250:19971/anyise/search"
    headers = {
        'authorization': bjdky_get_authorization
    }
    commitCompany = "430100"
    raw_data = {"commitCompany": commitCompany, "pageNum": 1, "pageSize": 20}
    try:
        response = requests.post(url=url, json=raw_data, headers=headers)
        response.raise_for_status()
        response_dict = response.json()
        for item in response_dict['data']['records']:
            item_commitCompany = item.get("commitCompany")
            assert commitCompany == item_commitCompany, f"{commitCompany} != {item_commitCompany}"
    except requests.exceptions.RequestException as e:
        allure.attach(f"Request failed: {e}", name="Error Log")
        pytest.fail(f"Request failed: {e}")


@allure.feature("按错误原因查询")
def test_errorInfo_query(bjdky_get_authorization):
    url = "http://10.10.106.250:19971/anyise/search"
    headers = {
        'authorization': bjdky_get_authorization
    }
    errorInfo = "找不到故障点"
    raw_data = {"errorInfo": errorInfo, "pageNum": 1, "pageSize": 50}
    try:
        response = requests.post(url=url, json=raw_data, headers=headers)
        response.raise_for_status()
        response_dict = response.json()
        for item in response_dict['data']['records']:
            item_errorInfo = item.get("errorInfo")
            assert errorInfo == item_errorInfo
    except requests.exceptions.RequestException as e:
        allure.attach(f"Request failed: {e}", name="Error Log")
        pytest.fail(f"Request failed: {e}")


@allure.feature("按提交时间查询")
def test_commitTime_query(bjdky_get_authorization):
    url = "http://10.10.106.250:19971/anyise/search"
    headers = {
        'authorization': bjdky_get_authorization
    }
    start_time_str = "2025-02-01 00:00:00"
    end_time_str = "2025-02-28 00:00:00"
    time_format = "%Y-%m-%d %H:%M:%S"
    str_to_datetime = datetime.strptime(start_time_str, time_format)
    end_time_datetime = datetime.strptime(end_time_str, time_format)

    raw_data = {"commitCompany": None, "commitTimeBegin": start_time_str, "commitTimeEnd": end_time_str, "pageNum": 1,
                "pageSize": 20}
    try:
        response = requests.post(url=url, json=raw_data, headers=headers)
        response.raise_for_status()
        response_dict = response.json()
        for item in response_dict['data']['records']:
            item_commitTime = item.get("commitTime")
            commitTime = datetime.strptime(item_commitTime, time_format)
            assert str_to_datetime <= commitTime <= end_time_datetime
    except requests.exceptions.RequestException as e:
        allure.attach(f"Request failed: {e}", name="Error Log")
        pytest.fail(f"Request failed: {e}")
