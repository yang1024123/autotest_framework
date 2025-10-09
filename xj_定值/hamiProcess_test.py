import pytest
from page_objects.login_page import LoginPage
from page_objects.process_create import ProcessCreatePage
from page_objects.process_approval import ProcessApprovalPage


@pytest.mark.usefixtures("setup_driver")
class TestProcessApproval:
    def test_process_approval_flow(self, setup_driver):
        """
        测试流程：登录 -> 创建流程 -> 审批流程
        """
        driver = setup_driver

        # 步骤 1：登录系统

        login_page = LoginPage(driver)
        login_page.navigate()
        login_page.login("cs001", "Hmdz1234.")
        assert login_page.is_logged_in(), "Login failed"

        # 步骤 2：创建流程
        create_page = ProcessCreatePage(driver)
        create_page.create_process("自动化测试")

        # 步骤 3：审批流程
        approval_page = ProcessApprovalPage(driver)
        approval_page.approve_process()

        # 断言：流程状态为已审批
        assert "Approved" in driver.page_source
