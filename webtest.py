from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import time

# 从环境变量获取配置
URL = os.getenv("TEST_URL", "http://10.10.106.250:11306/xhdl/hmdz/homePage")
USERNAME = os.getenv("TEST_USERNAME", "cs001")
PASSWORD = os.getenv("TEST_PASSWORD", "Hmdz1234.")
WAIT_TIMEOUT = 10


def init_driver():
    options = Options()
    options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    return driver, WebDriverWait(driver, WAIT_TIMEOUT)


def main():
    driver, wait = init_driver()

    try:
        driver.get(URL)
        driver.maximize_window()

        # 登录操作
        username_field = (By.XPATH, "//input[@class='el-input__inner' and @placeholder='账号']")
        password_field = (By.XPATH, "//input[@class='el-input__inner' and @placeholder='密码']")
        login_button = (By.XPATH, "//button[contains(@class, 'el-button') and contains(@class, 'loginBtn')]")
        order_flow = (By.XPATH, "//a[@href='/xhdl/hmdz/fixedValueOrderFlow']")

        wait.until(EC.visibility_of_element_located(username_field)).send_keys(USERNAME)
        wait.until(EC.visibility_of_element_located(password_field)).send_keys(PASSWORD)
        wait.until(EC.element_to_be_clickable(login_button)).click()

        # 等待首页加载完成
        wait.until(EC.url_contains("homePage"))
        wait.until(EC.presence_of_element_located(order_flow)).click()

        # 工单操作
        new_order_btn = (
        By.XPATH, "//button[@class='el-button el-button--primary el-button--small']//span[text()='新建工单']")
        line_input_img = (By.XPATH, "//div[contains(@class, 'lineInputImg') and contains(@class, 'el-popover__reference')]")

        wait.until(EC.element_to_be_clickable(new_order_btn)).click()
        wait.until(EC.element_to_be_clickable(line_input_img)).click()
        elements = wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//input[@placeholder='请选择线路' and @class='el-input__inner']")))

        # 遍历元素，找到第一个未被禁用的元素
        for element in elements:
            if not element.get_attribute("disabled"):
                # 执行操作，例如点击
                element.send_keys("985")
                break
        time.sleep(10)
        print("工单操作成功")
    except TimeoutException as e:
        print(f"元素加载超时: {str(e)}")
    except NoSuchElementException as e:
        print(f"元素未找到: {str(e)}")
    except Exception as e:
        print(f"发生错误: {str(e)}")
    finally:
        print("测试完成")
        driver.quit()
if __name__ == "__main__":
    main()