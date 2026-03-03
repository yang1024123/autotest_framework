from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import os
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 从环境变量获取配置
URL = os.getenv("TEST_URL", "http://10.10.106.250:11306/xhdl/hmdz/homePage")
WAIT_TIMEOUT = 10

def init_driver():
    options = Options()
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    return driver, WebDriverWait(driver, WAIT_TIMEOUT)

def save_screenshot(driver, name):
    try:
        screenshot_path = f"screenshot_{name}_{int(time.time())}.png"
        driver.save_screenshot(screenshot_path)
        logger.info(f"Screenshot saved: {screenshot_path}")
    except Exception as e:
        logger.error(f"Failed to save screenshot: {str(e)}")

def main():
    driver, wait = init_driver()
    driver.get(URL)
    driver.maximize_window()

    # 登录操作
    username_field = (By.XPATH, "//input[@class='el-input__inner' and @placeholder='账号']")
    password_field = (By.XPATH, "//input[@class='el-input__inner' and @placeholder='密码']")
    login_button = (By.XPATH, "//button[contains(@class, 'el-button') and contains(@class, 'loginBtn')]")

    wait.until(EC.visibility_of_element_located(username_field)).send_keys("cs001")
    wait.until(EC.visibility_of_element_located(password_field)).send_keys("Hmdz1234.")
    wait.until(EC.element_to_be_clickable(login_button)).click()
    time.sleep(3)
    # 等待首页加载完成
    driver.get("http://10.10.106.250:11306/xhdl/hmdz/fixedValueOrderFlow")
    # 等待页面加载完成，确保最后一个删除按钮可见
    time.sleep(3)
    # 定位所有删除按钮（支持包含空格的文本）
    delete_buttons = driver.find_elements(By.XPATH, "//button[contains(., '删除')]")

    if delete_buttons:
        # 点击最后一个删除按钮
        last_delete_button = delete_buttons[-1]
        last_delete_button.click()
        logger.info("成功点击删除按钮")
    else:
        logger.warning("未找到删除按钮，无法执行删除操作")
        save_screenshot(driver, "no_delete_buttons")
        driver.quit()
        return
    # 等待并定位到包含按钮的div
    btns_div = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.el-message-box__btns"))
    )
    print(1111111)
    # 在该div内查找文本为“是”的button
    yes_button = btns_div.find_element(By.XPATH, ".//button[.//span[contains(text(), '是')]]")

    # 点击该按钮
    yes_button.click()
    logger.info("工单操作成功")
if __name__ == "__main__":
    main()
