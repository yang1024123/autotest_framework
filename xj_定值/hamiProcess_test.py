import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from page_objects.login_page import LoginPage
from page_objects.process_create import ProcessCreatePage
from page_objects.process_delete import ProcessDeletePage


@pytest.mark.usefixtures("setup_driver")
class TestProcessApproval:
    def test_add_flow(self, setup_driver):
        """
        测试流程：登录 -> 创建流程
        """
        driver = setup_driver

        # 步骤 1：登录系统
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login("cs001", "Hmdz1234.")
        assert login_page.is_logged_in(), '登录成功！'

        # 步骤 2：创建流程
        create_page = ProcessCreatePage(driver)
        create_page.create_process("自动化测试流程")

        # 添加断言验证流程创建成功
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'el-message--success')]//p[contains(text(),'操作成功')]"))
            )
            print("流程创建成功验证通过   ")
        except:
            pytest.fail("流程创建成功提示未出现")

    def test_delete_flow(self, setup_driver):
        """
        测试流程：登录 -> 删除流程
        """
        driver = setup_driver

        # 步骤 1：登录系统
        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login("cs001", "Hmdz1234.")
        assert login_page.is_logged_in(), '登录成功！'

        # 步骤 2：删除流程
        delete_page = ProcessDeletePage(driver)
        delete_success = delete_page.process_delete()

        # 添加断言验证删除成功
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'el-message--success')]//p[contains(text(),'删除成功')]"))
            )
            print("流程删除成功验证通过")
        except:
            pytest.fail("流程删除成功提示未出现")

