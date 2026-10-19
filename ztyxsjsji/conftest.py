"""ztyxsjsji 模块专属 fixture。

通用授权码 fixture (bjdky_get_authorization) 已在根 conftest.py 定义，
此处只保留本模块特有的造数/清数 fixture。
"""

import allure
import pytest
import requests

from common.config import Config
from common.http_client import ApiClient


def _client():
    return ApiClient(Config.BJDKY_BASE_URL)


@pytest.fixture(scope="function", autouse=True)
def get_fileDocId(bjdky_get_authorization):
    """获取案例关联的 fileDocId 列表（逗号分隔字符串）。"""
    headers = {
        "authorization": bjdky_get_authorization,
        "Content-Type": "application/json;charset=UTF-8",
    }
    data = {"caseType": 0, "name": "这是案例333", "faultLastTime": 41}
    try:
        response = _client().post("caseRule/svg-list/by-fault-type", json=data, headers=headers)
        response.raise_for_status()
        response_dict = response.json()
        file_doc_ids = ",".join(item["fileDocId"] for item in response_dict["data"])
        return file_doc_ids
    except Exception as e:  # noqa: BLE001
        allure.attach(f"获取 fileDocId 失败: {e}", name="Error Log")
        pytest.fail(f"获取 fileDocId 失败: {e}")


@pytest.fixture(scope="function")
def setup_addcase(bjdky_get_authorization, get_fileDocId):
    """造数：新增案例。"""
    headers = {"authorization": bjdky_get_authorization}
    raw_data = {
        "caseType": 0,
        "name": "这是案例名称333",
        "describes": "这是案例描述",
        "faultLastTime": 41,
        "faultIds": get_fileDocId,
    }
    try:
        response = _client().post("caseRule/add", json=raw_data, headers=headers)
        assert "保存成功" in response.text, f"新增案例失败: {response.text}"
    except requests.exceptions.RequestException as e:
        allure.attach(f"Request failed: {e}", name="Error Log")
        pytest.fail(f"新增案例请求失败: {e}")


@pytest.fixture(scope="function")
def teardown_deletecase(bjdky_get_authorization):
    """清数：删除最新案例（在用例结束后执行）。"""
    yield
    headers = {"authorization": bjdky_get_authorization}

    # 查询最新案例 id
    data = {"current": 1, "size": 20}
    resp = _client().post("caseRule/page", json=data, headers=headers)
    resp.raise_for_status()
    case_id = resp.json()["data"]["records"][0].get("id")

    raw_data = {"id": case_id}
    try:
        response = _client().post("caseRule/delete", json=raw_data, headers=headers)
        assert "删除成功" in response.text, f"删除案例失败: {response.text}"
    except requests.exceptions.RequestException as e:
        allure.attach(f"Request failed: {e}", name="Error Log")
        pytest.fail(f"删除案例请求失败: {e}")
