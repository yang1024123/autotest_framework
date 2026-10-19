"""Selenium 页面对象基类。

封装显式等待、元素查找等公共能力，供各 Page Object 复用，
避免每个页面类重复实现 _wait_element_clickable 等方法。
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """页面对象基类。"""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def find(self, locator):
        """查找单个元素（等待其存在）。"""
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator):
        """查找所有元素（等待至少一个存在）。"""
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        """等待元素可点击后点击。"""
        return self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator, text):
        """等待元素可点击后输入文本。"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.clear()
        element.send_keys(text)
        return element

    def get_text(self, locator):
        """等待元素存在并返回其文本。"""
        return self.find(locator).text
