import allure

from common.config import Config
from common.http_client import ApiClient


@allure.feature("规则案例构建-按故障持续时间分类")
def test_caseBuild_duration(bjdky_get_authorization, get_fileDocId):
    client = ApiClient(Config.BJDKY_BASE_URL)
    headers = {"authorization": bjdky_get_authorization}
    raw_data = {
        "caseType": 0,
        "name": "这是案例名称333",
        "describes": "这是案例描述",
        "faultLastTime": 41,
        "faultIds": get_fileDocId,
    }

    response = client.post("caseRule/add", json=raw_data, headers=headers)
    assert "保存成功" in response.text, f"Expected '保存成功', but got: {response.text}"


@allure.feature("案例删除")
def test_deleteCase(setup_addcase, teardown_deletecase):
    print("执行通过")
