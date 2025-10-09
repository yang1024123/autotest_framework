import pytest
from selenium import webdriver
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to execute tests on.")
    parser.addoption("--headless", action="store_true", help="Run tests in headless mode.")


@pytest.fixture(scope="function")
def setup_driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    if browser == "chrome":
        # 创建ChromeOptions对象
        from selenium.webdriver.chrome.options import Options
        options = Options()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        from selenium.webdriver.firefox.options import Options
        options = Options()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Browser {browser} is not supported.")

    driver.maximize_window()
    yield driver
    driver.quit()