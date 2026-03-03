import logging
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class ProcessCreatePage:
    def __init__(self, driver, base_url="http://10.10.106.250:11306/xhdl/hmdz/fixedValueOrderFlow"):
        self.driver = driver
        self.url = base_url
        self.description_locator = (By.XPATH, "//textarea[@placeholder='请输入更改原因']")
        self.submit_locator = (By.XPATH, "//span[text()='发起']/parent::button")
        self.create_order_btn = (By.XPATH, "//button[contains(@class,'el-button--primary')]//span[text()='新建工单']")
        self.line_input = (
        By.XPATH, "//div[contains(@class,'lineInputImg') and contains(@class,'el-popover__reference')]")
        self.line_search = (By.XPATH, "//input[@placeholder='请选择线路' and @class='el-input__inner']")
        self.device_checkbox = (By.XPATH,
                                "//label[@class='el-checkbox select-round' and contains(span[@class='el-checkbox__label'], '测试设备280')]")
        self.flow_selector = (By.CSS_SELECTOR, "input.el-input__inner[placeholder='请选择审批流']")
        self.flow_option = (By.XPATH, "//span[text()='哈密定值整定流程']")
        self.scrollable_div = (By.XPATH, '//div[@class="addContent"]')

    def _wait_element_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def _scroll_to_bottom(self):
        scrollable = self._wait_element_clickable(self.scrollable_div)
        self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scrollable)

    def go_to_create(self):
        self.driver.get(self.url)
        self._wait_element_clickable(self.create_order_btn).click()

    def select_specific_line(self, line_name='测试线路985'):
        try:
            self._wait_element_clickable(self.line_input).click()

            elements = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(self.line_search)
            )
            for element in elements:
                if not element.get_attribute("disabled"):
                    element.send_keys(line_name)
                    break

            line_locator = (
            By.XPATH, f"//li[contains(@class,'el-select-dropdown__item') and .//span[text()='{line_name}']]")
            self._wait_element_clickable(line_locator).click()

        except Exception as e:
            logging.error("Error selecting line %s: %s", line_name, str(e))
            raise

    def select_device(self):
        self._wait_element_clickable(self.device_checkbox).click()

    def select_flow(self):
        self._wait_element_clickable(self.flow_selector).click()
        self._wait_element_clickable(self.flow_option).click()

    def upload_file(self, filename: str = 'example.jpg') -> None:
        if not hasattr(self, 'driver') or self.driver is None:
            raise ValueError("Driver is not initialized")
        try:
            # 设置文件路径
            file_path = os.path.abspath(os.path.join('uploads', filename))
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"文件路径不存在: {file_path}")
            elements = self.driver.find_elements(By.CLASS_NAME, 'el-upload__input')
            uploadfile = elements[-1]
            uploadfile.send_keys(file_path)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"文件未找到: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"上传过程中发生错误: {str(e)}")
    def create_process(self, description):
        if not description:
            raise ValueError("Description cannot be empty")

        self.go_to_create()
        self.select_specific_line()
        self.select_device()

        self._wait_element_clickable(self.description_locator).send_keys(description)
        self._scroll_to_bottom()
        self.select_flow()
        self.upload_file()
        self._wait_element_clickable(self.submit_locator).click()
        print("流程创建成功")