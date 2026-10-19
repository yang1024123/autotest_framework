"""全局公共 fixture。

提供：
- 各业务系统的登录/token fixture（session 级，避免每个用例重复登录）
- 数据库连接 fixture（function 级，yield 自动回收）
- 通用 WebDriver fixture

所有凭证/地址统一从 common.config 读取（.env 管理），不在此硬编码。
"""

import allure
import pymysql
import pytest
import requests

from common.config import Config
from common.http_client import ApiClient


def _login_by_url(url, login_payload, token_extractor, name):
    """通用登录逻辑（完整 URL 版本）：POST 登录 -> 提取 token。"""
    try:
        response = requests.post(url=url, json=login_payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        token = token_extractor(data)
        if not token:
            raise ValueError(f"响应中未提取到 token: {data}")
        return token
    except Exception as e:  # noqa: BLE001
        allure.attach(f"登录失败 [{name}]: {e}", name="Login Error")
        raise RuntimeError(f"[{name}] 登录失败: {e}") from e


def _login(client, login_payload, token_extractor, name):
    """通用登录逻辑：POST 登录 -> 提取 token。

    :param client: ApiClient 实例
    :param login_payload: 登录请求体
    :param token_extractor: 从响应 JSON 中提取 token 的回调
    :param name: 系统名（用于日志/错误提示）
    :return: token 字符串；失败抛出 RuntimeError（不静默吞掉）
    """
    try:
        response = client.post("login", json=login_payload)
        response.raise_for_status()
        data = response.json()
        token = token_extractor(data)
        if not token:
            raise ValueError(f"响应中未提取到 token: {data}")
        return token
    except Exception as e:  # noqa: BLE001 — 登录失败必须显式暴露
        allure.attach(f"登录失败 [{name}]: {e}", name="Login Error")
        raise RuntimeError(f"[{name}] 登录失败: {e}") from e


# ---------------------------------------------------------------------------
# 北京电力科研院 (ztyxsjsji) — 授权码
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def bjdky_get_authorization():
    client = ApiClient(Config.BJDKY_BASE_URL)
    payload = {"userName": Config.BJDKY_USERNAME, "password": Config.BJDKY_PASSWORD}
    return _login(client, payload, lambda d: d["data"], "bjdky")


# ---------------------------------------------------------------------------
# 新疆定值 (xj_dz) — token
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def xjdz_get_token():
    # token 接口为完整 URL，直接用 requests 请求
    payload = {
        "data": {
            "userAccount": Config.XJDZ_USER_ACCOUNT,
            "passWord": Config.XJDZ_PASSWORD,
            "token": "null",
        }
    }
    return _login_by_url(
        Config.XJDZ_TOKEN_URL,
        payload,
        lambda d: d["data"]["token"],
        "xjdz",
    )


# ---------------------------------------------------------------------------
# 行波 (xingbo) — token
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def xingbo_get_token():
    client = ApiClient(Config.XINGBO_BASE_URL)
    payload = {"account": Config.XINGBO_ACCOUNT, "password": Config.XINGBO_PASSWORD}

    def extractor(data):
        token = data["data"]["token"]
        return f"{token['tokenType']} {token['accessToken']}"

    return _login(client, payload, extractor, "xingbo")


# ---------------------------------------------------------------------------
# 数据库连接 (nx)
# ---------------------------------------------------------------------------
@pytest.fixture(scope="function")
def db_connection():
    """返回 pymysql 连接，测试结束后自动关闭。"""
    conn = pymysql.connect(
        host=Config.NX_DB_HOST,
        port=int(Config.NX_DB_PORT),
        user=Config.NX_DB_USER,
        password=Config.NX_DB_PASSWORD,
        db=Config.NX_DB_NAME,
        charset=Config.NX_DB_CHARSET,
        cursorclass=pymysql.cursors.DictCursor,
    )
    yield conn
    conn.close()


@pytest.fixture(scope="function")
def db_cursor(db_connection):
    """返回 DictCursor，测试结束后自动关闭。"""
    cursor = db_connection.cursor()
    yield cursor
    cursor.close()
