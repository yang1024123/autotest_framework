from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def navigate(self):
        self.driver.get("http://10.10.106.250:11306/xhdl/hmdz/homePage")

    def login(self, name, password):
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@class='el-input__inner' and @placeholder='账号']"))).send_keys(name)
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@class='el-input__inner' and @placeholder='密码']"))).send_keys(password)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'el-button') and contains(@class, 'loginBtn')]"))).click()

    def is_logged_in(self):
        try:
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='el-message el-message--success']//p[contains(text(), '登录成功！')]")))
            return True
        except:
            return False

    def get_error_message(self):
        return self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='el-message el-message--error']//p[contains(text(), '用户名或密码错误')]"))).text
