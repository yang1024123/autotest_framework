from datetime import datetime

import allure
import pytest

from common.config import Config
from common.http_client import ApiClient


@pytest.fixture(scope="module")
def client():
    return ApiClient(Config.BJDKY_BASE_URL)


@allure.feature("按文件名称查询")
def test_filename_query(client, bjdky_get_authorization):
    headers = {"authorization": bjdky_get_authorization}
    filename = "不接地"
    raw_data = {"commitCompany": None, "fileName": filename, "pageNum": 1, "pageSize": 20}

    response = client.post("anyise/search", json=raw_data, headers=headers)
    response.raise_for_status()
    response_data = response.json()
    assert response_data and "data" in response_data, "Invalid response format"
    for item in response_data["data"]["records"]:
        assert filename in item["fileName"], f"{filename} not found in {item['fileName']}"


@allure.feature("按网省公司查询")
def test_province_query(client, bjdky_get_authorization):
    headers = {"authorization": bjdky_get_authorization}
    province = "110000"
    raw_data = {"provCompany": province, "commitCompany": None, "pageNum": 1, "pageSize": 20}

    response = client.post("anyise/search", json=raw_data, headers=headers)
    response.raise_for_status()
    response_dict = response.json()
    for item in response_dict["data"]["records"]:
        assert province == item.get("provCompany")


@allure.feature("按提交单位查询")
def test_commitCompany_query(client, bjdky_get_authorization):
    headers = {"authorization": bjdky_get_authorization}
    commitCompany = "430100"
    raw_data = {"commitCompany": commitCompany, "pageNum": 1, "pageSize": 20}

    response = client.post("anyise/search", json=raw_data, headers=headers)
    response.raise_for_status()
    response_dict = response.json()
    for item in response_dict["data"]["records"]:
        assert commitCompany == item.get("commitCompany"), f"{commitCompany} != {item.get('commitCompany')}"


@allure.feature("按错误原因查询")
def test_errorInfo_query(client, bjdky_get_authorization):
    headers = {"authorization": bjdky_get_authorization}
    errorInfo = "找不到故障点"
    raw_data = {"errorInfo": errorInfo, "pageNum": 1, "pageSize": 50}

    response = client.post("anyise/search", json=raw_data, headers=headers)
    response.raise_for_status()
    response_dict = response.json()
    for item in response_dict["data"]["records"]:
        assert errorInfo == item.get("errorInfo")


@allure.feature("按提交时间查询")
def test_commitTime_query(client, bjdky_get_authorization):
    headers = {"authorization": bjdky_get_authorization}
    start_time_str = "2025-02-01 00:00:00"
    end_time_str = "2025-02-28 00:00:00"
    time_format = "%Y-%m-%d %H:%M:%S"
    start_dt = datetime.strptime(start_time_str, time_format)
    end_dt = datetime.strptime(end_time_str, time_format)

    raw_data = {
        "commitCompany": None,
        "commitTimeBegin": start_time_str,
        "commitTimeEnd": end_time_str,
        "pageNum": 1,
        "pageSize": 20,
    }

    response = client.post("anyise/search", json=raw_data, headers=headers)
    response.raise_for_status()
    response_dict = response.json()
    for item in response_dict["data"]["records"]:
        commit_time = datetime.strptime(item.get("commitTime"), time_format)
        assert start_dt <= commit_time <= end_dt
