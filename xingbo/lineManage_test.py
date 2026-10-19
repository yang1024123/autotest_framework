import allure
import pytest

from common.config import Config
from common.http_client import ApiClient


@pytest.fixture(scope="module")
def client():
    return ApiClient(Config.XINGBO_BASE_URL)


@allure.feature("按线路名称查询")
def test_linename_query(client, xingbo_get_token):
    headers = {"Authorization": xingbo_get_token}
    filename = "F002"
    raw_data = {"deptIds": [], "feederIds": [filename], "feederTypes": [], "pageNum": 1, "pageSize": 20}

    response = client.post("api/line/feeders/page", json=raw_data, headers=headers)
    response.raise_for_status()
    response_dict = response.json()
    for item in response_dict["data"]["list"]:
        assert filename in item.get("feederId")


@allure.feature("按线路类型查询")
def test_linetype_query(client, xingbo_get_token):
    headers = {"Authorization": xingbo_get_token}
    filetype = "1"
    raw_data = {"deptIds": [], "feederIds": [], "feederTypes": [filetype], "pageNum": 1, "pageSize": 20}

    response = client.post("api/line/feeders/page", json=raw_data, headers=headers)
    response.raise_for_status()
    response_dict = response.json()
    for item in response_dict["data"]["list"]:
        assert filetype == str(item.get("feederType"))


@allure.feature("分页切换")
def test_paging_query(client, xingbo_get_token):
    headers = {"Authorization": xingbo_get_token}
    pageSize = "10"
    raw_data = {"deptIds": [], "feederIds": [], "feederTypes": [], "pageNum": 1, "pageSize": pageSize}

    response = client.post("api/line/feeders/page", json=raw_data, headers=headers)
    response.raise_for_status()
    response_dict = response.json()
    pages = response_dict["data"]["pages"]
    total = response_dict["data"]["total"]
    if int(total) % int(pageSize) != 0:
        assert int(total) // int(pageSize) + 1 == int(pages)
    else:
        assert int(total) // int(pageSize) == int(pages)
