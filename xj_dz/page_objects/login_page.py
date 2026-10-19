from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from common.base_page import BasePage
from common.config import Config


class LoginPage(BasePage):
    USERNAME_LOCATOR = (By.XPATH, "//input[@class='el-input__inner' and @placeholder='账号']")
    PASSWORD_LOCATOR = (By.XPATH, "//input[@class='el-input__inner' and @placeholder='密码']")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(@class, 'el-button') and contains(@class, 'loginBtn')]")
    SUCCESS_MSG = (By.XPATH, "//div[@class='el-message el-message--success']//p[contains(text(), '登录成功！')]")
    ERROR_MSG = (By.XPATH, "//div[@class='el-message el-message--error']//p[contains(text(), '用户名或密码错误')]")

    def navigate(self):
        self.driver.get(f"{Config.XJDZ_BASE_URL}/xhdl/hmdz/homePage")

    def login(self, name, password):
        self.type(self.USERNAME_LOCATOR, name)
        self.type(self.PASSWORD_LOCATOR, password)
        self.click(self.LOGIN_BUTTON)

    def is_logged_in(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.SUCCESS_MSG))
            return True
        except Exception:
            return False

    def get_error_message(self):
        return self.get_text(self.ERROR_MSG)
