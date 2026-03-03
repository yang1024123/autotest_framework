import logging
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class ProcessDeletePage:
    def __init__(self, driver, base_url="http://10.10.106.250:11306/xhdl/hmdz/fixedValueOrderFlow"):
        self.driver = driver
        self.url = base_url
        self.logger = logging.getLogger(__name__)

    def _wait_element_clickable(self, locator, timeout=10):
        """等待元素可点击"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
        except Exception as e:
            self.logger.error(f"等待元素可点击失败: {locator}, 错误: {e}")
            raise

    def _wait_element_present(self, locator, timeout=10):
        """等待元素存在"""
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
        except Exception as e:
            self.logger.error(f"等待元素存在失败: {locator}, 错误: {e}")
            raise

    def go_to_delete(self):
        """执行删除操作的主流程"""
        try:
            # 访问页面
            self.driver.get(self.url)
            self.logger.info(f"已访问页面: {self.url}")

            # 使用显式等待替代固定sleep
            delete_buttons = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//button[contains(., '删除')]"))
            )

            if not delete_buttons:
                self.logger.warning("未找到删除按钮，无法执行删除操作")
                return False

            # 点击最后一个删除按钮
            last_delete_button = delete_buttons[-1]
            last_delete_button.click()
            self.logger.info("已点击删除按钮")

            # 等待确认对话框出现
            btns_div = self._wait_element_present((By.CSS_SELECTOR, "div.el-message-box__btns"))

            # 查找并点击"是"按钮
            yes_button = btns_div.find_element(By.XPATH, ".//button[.//span[contains(text(), '是')]]")
            yes_button.click()
            self.logger.info("已确认删除操作")

            # 可选的：等待删除完成提示
            time.sleep(1)  # 可根据实际情况调整或替换为显式等待
            print("删除操作成功完成")
            return True

        except Exception as e:
            self.logger.error(f"删除操作执行失败: {e}")
            print(f"删除失败: {e}")
            return False

    def process_delete(self):
        """对外提供的删除处理方法"""
        return self.go_to_delete()