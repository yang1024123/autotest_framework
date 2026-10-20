"""新疆定值 UI 测试的 fixture。"""

import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser to execute tests on.")
    parser.addoption("--headless", action="store_true",
                     help="Run tests in headless mode.")


def _chrome_service():
    """定位 chromedriver。

    优先使用环境变量 CHROMEDRIVER_PATH 指定的路径；
    其次探测本地常见路径；都没有则回退到 Selenium Manager 自动管理。
    这样在 Jenkins（SYSTEM 账户，无法联网下载 driver）也能稳定运行。
    """
    candidates = [
        os.getenv("CHROMEDRIVER_PATH"),
        r"D:\python\chromedriver.exe",
        r"D:\python\chromedriver-win64\chromedriver.exe",
    ]
    for path in candidates:
        if path and os.path.exists(path):
            return ChromeService(executable_path=path)
    return None  # 回退 Selenium Manager


@pytest.fixture(scope="function")
def setup_driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    if browser == "chrome":
        options = webdriver.ChromeOptions()
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
    else:
        raise ValueError(f"Browser {browser} is not supported.")

    # CI/无桌面环境下建议启用 headless
    if headless or os.getenv("JENKINS_URL"):
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    if browser == "chrome":
        service = _chrome_service()
        if service:
            driver = webdriver.Chrome(options=options, service=service)
        else:
            driver = webdriver.Chrome(options=options)
    else:
        driver = webdriver.Firefox(options=options)

    driver.maximize_window()
    yield driver
    driver.quit()
