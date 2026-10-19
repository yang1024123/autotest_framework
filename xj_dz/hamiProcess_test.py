from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from common.config import Config
from page_objects.login_page import LoginPage
from page_objects.process_create import ProcessCreatePage
from page_objects.process_delete import ProcessDeletePage


def _login(driver):
    """复用登录，避免每个用例重复编写登录步骤。"""
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login(Config.XJDZ_UI_USERNAME, Config.XJDZ_UI_PASSWORD)
    assert login_page.is_logged_in(), "登录成功提示未出现"


def test_add_flow(setup_driver):
    driver = setup_driver
    _login(driver)

    create_page = ProcessCreatePage(driver)
    create_page.create_process("自动化测试流程", city_company="HM")

    # 等待创建成功提示（WebDriverWait 超时会自动抛异常，无需 try/except）
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class,'el-message--success')]//p[contains(text(),'操作成功')]")
        )
    )


def test_delete_flow(setup_driver):
    driver = setup_driver
    _login(driver)

    delete_page = ProcessDeletePage(driver)
    assert delete_page.process_delete(), "流程删除未成功"
