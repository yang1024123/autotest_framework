import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common.base_page import BasePage
from common.config import Config


class ProcessDeletePage(BasePage):
    def __init__(self, driver, base_url=None):
        super().__init__(driver)
        self.url = base_url or f"{Config.XJDZ_BASE_URL}/xhdl/hmdz/fixedValueOrderFlow"
        self.logger = logging.getLogger(__name__)

    def _find_deletable_buttons(self, timeout=10):
        """查找当前可见且可点击的「删除」按钮，过滤掉隐藏/禁用项。"""
        buttons = WebDriverWait(self.driver, timeout).until(
            EC.presence_of_all_elements_located((By.XPATH, "//button[contains(., '删除')]"))
        )
        deletable = []
        for btn in buttons:
            try:
                if btn.is_displayed() and btn.is_enabled():
                    deletable.append(btn)
            except Exception:  # noqa: BLE001 — 某些元素可能已脱离 DOM
                continue
        return deletable

    def go_to_delete(self):
        """执行删除操作的主流程。"""
        self.driver.get(self.url)
        self.logger.info(f"已访问页面: {self.url}")

        # 只取可见且可点击的删除按钮
        delete_buttons = self._find_deletable_buttons()
        if not delete_buttons:
            self.logger.warning("未找到可点击的删除按钮，无法执行删除操作")
            return False

        # 点击最后一条数据对应的删除按钮
        target = delete_buttons[-1]
        self._js_click(target)
        self.logger.info("已点击删除按钮")

        # 等待确认对话框出现，并点击确认按钮（兼容「是」/「确定」/「删除」等文案）
        confirm_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//div[contains(@class,'el-message-box')]"
                    "//button[.//span[contains(text(),'是') or contains(text(),'确定') or contains(text(),'删除')]]",
                )
            )
        )
        self._js_click(confirm_btn)
        self.logger.info("已确认删除操作")

        # 等待删除成功提示或对话框关闭（二选一，避免文案不一致导致误判）
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class,'el-message--success')]")
                )
            )
        except Exception:  # noqa: BLE001 — 以对话框关闭作为兜底判定
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(
                    (By.XPATH, "//div[contains(@class,'el-message-box')]")
                )
            )
        self.logger.info("删除操作完成")
        return True

    def _js_click(self, element):
        """用 JS 触发点击，规避元素被遮挡/未居中导致的 ElementNotInteractable。"""
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();",
            element,
        )

    def process_delete(self):
        """对外提供的删除处理方法。"""
        return self.go_to_delete()
