"""全局配置加载。

从 .env 读取各业务系统的地址与凭证，并暴露为统一入口。
敏感信息统一通过环境变量管理，禁止在测试代码中硬编码。
"""

import os

from dotenv import load_dotenv

# 加载项目根目录下的 .env
load_dotenv()


def _get(key, default=None):
    """读取环境变量，返回去空白后的值；不存在则返回默认值。"""
    value = os.getenv(key)
    if value is None:
        return default
    return value.strip()


class Config:
    """集中式配置访问器。

    各系统配置通过属性访问，例如 Config.BJDKY_USERNAME。
    """

    # 北京电力科研院 (ztyxsjsji)
    BJDKY_BASE_URL = _get("BJDKY_BASE_URL")
    BJDKY_USERNAME = _get("BJDKY_USERNAME")
    BJDKY_PASSWORD = _get("BJDKY_PASSWORD")

    # 新疆定值 (xj_dz)
    XJDZ_BASE_URL = _get("XJDZ_BASE_URL")
    XJDZ_TOKEN_URL = _get("XJDZ_TOKEN_URL")
    XJDZ_USER_ACCOUNT = _get("XJDZ_USER_ACCOUNT")
    XJDZ_PASSWORD = _get("XJDZ_PASSWORD")
    XJDZ_UI_USERNAME = _get("XJDZ_UI_USERNAME")
    XJDZ_UI_PASSWORD = _get("XJDZ_UI_PASSWORD")

    # 兴博 (xingbo)
    XINGBO_BASE_URL = _get("XINGBO_BASE_URL")
    XINGBO_ACCOUNT = _get("XINGBO_ACCOUNT")
    XINGBO_PASSWORD = _get("XINGBO_PASSWORD")

    # 数据库 (nx)
    NX_DB_HOST = _get("NX_DB_HOST")
    NX_DB_PORT = _get("NX_DB_PORT")
    NX_DB_USER = _get("NX_DB_USER")
    NX_DB_PASSWORD = _get("NX_DB_PASSWORD")
    NX_DB_NAME = _get("NX_DB_NAME")
    NX_DB_CHARSET = _get("NX_DB_CHARSET", "utf8mb4")

    # 视觉回归
    APPLITOOLS_API_KEY = _get("APPLITOOLS_API_KEY")

    # 渗透目标
    PENTEST_BASE_URL = _get("PENTEST_BASE_URL")
    PENTEST_USERNAME = _get("PENTEST_USERNAME")
    PENTEST_PASSWORD = _get("PENTEST_PASSWORD")

    # Percy
    PERCY_TOKEN = _get("PERCY_TOKEN")
