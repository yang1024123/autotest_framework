"""新疆定值 UI 测试的 fixture。"""

import pytest
from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Browser to execute tests on.")
    parser.addoption("--headless", action="store_true",
                     help="Run tests in headless mode.")


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

    if headless:
        options.add_argument("--headless")

    if browser == "chrome":
        driver = webdriver.Chrome(options=options)
    else:
        driver = webdriver.Firefox(options=options)

    driver.maximize_window()
    yield driver
    driver.quit()
