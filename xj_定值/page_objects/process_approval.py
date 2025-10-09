from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ProcessApprovalPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "http://your-app.com/process/approval"
        self.process_list_locator = (By.CSS_SELECTOR, ".process-list")
        self.approve_button_locator = (By.XPATH, "//button[text()='Approve']")

    def go_to_approval(self):
        self.driver.get(self.url)

    def approve_process(self):
        self.go_to_approval()
        # 假设流程已经在列表中
        process_list = self.driver.find_element(*self.process_list_locator)
        approve_button = process_list.find_element(*self.approve_button_locator)
        approve_button.click()
        return WebDriverWait(self.driver, 10).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".status"), "Approved"))
