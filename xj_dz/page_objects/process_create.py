import logging
import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common.base_page import BasePage
from common.config import Config


class ProcessCreatePage(BasePage):
    DESCRIPTION_LOCATOR = (By.XPATH, "//textarea[@placeholder='请输入更改原因']")
    SUBMIT_LOCATOR = (By.XPATH, "//span[text()='发起']/parent::button")
    CREATE_ORDER_BTN = (By.XPATH, "//button[contains(@class,'el-button--primary')]//span[text()='新建工单']")
    LINE_INPUT = (By.XPATH, "//div[contains(@class,'lineInputImg') and contains(@class,'el-popover__reference')]")
    LINE_SEARCH = (By.XPATH, "//input[@placeholder='请选择线路' and @class='el-input__inner']")
    FLOW_SELECTOR = (By.CSS_SELECTOR, "input.el-input__inner[placeholder='请选择审批流']")
    SCROLLABLE_DIV = (By.XPATH, '//div[@class="addContent"]')

    # 「选择市公司」弹窗（新建工单后强制出现）
    CITY_DIALOG = (By.XPATH, "//span[text()='选择市公司']/ancestor::div[contains(@class,'el-dialog')]")

    def __init__(self, driver, base_url=None):
        super().__init__(driver)
        self.url = base_url or f"{Config.XJDZ_BASE_URL}/xhdl/hmdz/fixedValueOrderFlow"

    def _scroll_to_bottom(self):
        scrollable = self.find(self.SCROLLABLE_DIV)
        self.driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", scrollable)

    def go_to_create(self, city_company=None):
        self.driver.get(self.url)
        self.click(self.CREATE_ORDER_BTN)
        self._handle_city_dialog(city_company)

    def _handle_city_dialog(self, city_name=None):
        """处理「选择市公司」弹窗。

        新建工单后会强制弹出该弹窗，需选择市公司并提交才能进入创建页。
        弹窗不存在（旧版本页面）时静默跳过。

        :param city_name: 要选择的市公司名称；为 None 时选择下拉中第一个可见选项
        """
        try:
            dialog = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.CITY_DIALOG)
            )
        except TimeoutException:
            logging.info("未出现「选择市公司」弹窗，直接进入创建页")
            return

        logging.info("检测到「选择市公司」弹窗，开始选择")
        # 点击弹窗内下拉框展开
        self.driver.execute_script(
            "arguments[0].click();",
            dialog.find_element(By.XPATH, ".//div[contains(@class,'el-select')]"),
        )

        # 下拉选项渲染在 body 级 .el-select-dropdown 中，需取当前可见的那个
        if city_name:
            option_xpath = (
                "//div[contains(@class,'el-select-dropdown') and not(contains(@style,'display: none'))]"
                f"//li[contains(@class,'el-select-dropdown__item') and normalize-space(.)='{city_name}']"
            )
        else:
            option_xpath = (
                "//div[contains(@class,'el-select-dropdown') and not(contains(@style,'display: none'))]"
                "//li[contains(@class,'el-select-dropdown__item') and not(contains(@class,'disabled'))]"
            )

        # 定位到匹配的 li，再点击其内部的 span（Element UI 的选中逻辑绑定在 span 上）
        option_li = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, option_xpath))
        )
        selected_city = option_li.text.strip()
        option_span = option_li.find_element(By.XPATH, ".//span")
        self.driver.execute_script(
            "arguments[0].dispatchEvent(new MouseEvent('click', {bubbles: true}));",
            option_span,
        )
        logging.info("已选择市公司: %s", selected_city)

        # 提交弹窗
        submit_btn = dialog.find_element(By.XPATH, ".//button[.//span[text()='提交']]")
        self.driver.execute_script("arguments[0].click();", submit_btn)

        # 等待弹窗关闭，确认已进入创建页
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element(dialog))
        logging.info("「选择市公司」弹窗已提交并关闭")

    def select_specific_line(self, line_name="测试线路985"):
        self.click(self.LINE_INPUT)

        elements = self.find_all(self.LINE_SEARCH)
        for element in elements:
            if not element.get_attribute("disabled"):
                element.send_keys(line_name)
                break

        line_locator = (By.XPATH, f"//li[contains(@class,'el-select-dropdown__item') and .//span[text()='{line_name}']]")
        self.click(line_locator)

    def select_device(self, device_name="测试设备280"):
        device_checkbox = (
            By.XPATH,
            f"//label[@class='el-checkbox select-round' and contains(span[@class='el-checkbox__label'], '{device_name}')]",
        )
        self.click(device_checkbox)

    def select_flow(self, flow_name="哈密定值整定流程"):
        self.click(self.FLOW_SELECTOR)
        flow_option = (By.XPATH, f"//span[text()='{flow_name}']")
        self.click(flow_option)

    def upload_file(self, filename="example.jpg"):
        file_path = os.path.abspath(os.path.join("uploads", filename))
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件路径不存在: {file_path}")
        elements = self.driver.find_elements(By.CLASS_NAME, "el-upload__input")
        elements[-1].send_keys(file_path)

    def create_process(self, description, city_company=None):
        if not description:
            raise ValueError("Description cannot be empty")

        self.go_to_create(city_company)
        self.select_specific_line()
        self.select_device()
        self.type(self.DESCRIPTION_LOCATOR, description)
        self._scroll_to_bottom()
        self.select_flow()
        self.upload_file()
        self.click(self.SUBMIT_LOCATOR)
