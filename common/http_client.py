"""通用 HTTP 客户端封装。

统一处理请求、超时、异常与响应解析，供接口测试复用，
避免各测试文件重复拼接 headers/url 与重复的 try/except 逻辑。
"""

import requests


class ApiClient:
    """轻量 HTTP 客户端封装。"""

    def __init__(self, base_url, timeout=10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def _url(self, path):
        return f"{self.base_url}/{path.lstrip('/')}"

    def request(self, method, path, *, headers=None, json=None, data=None, **kwargs):
        """发起请求，统一注入超时；返回 Response，网络异常向上抛出。"""
        return self.session.request(
            method,
            self._url(path),
            headers=headers,
            json=json,
            data=data,
            timeout=kwargs.pop("timeout", self.timeout),
            **kwargs,
        )

    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path, **kwargs):
        return self.request("POST", path, **kwargs)
