import pytest
import allure
from workflows.login_flow import LoginFlow

@allure.feature("Demo Scenarios")
class TestDemo:
    
    @allure.story("Login Success")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_success(self, driver):
        """
        Verifies that a user can successfully log in.
        """
        # Data
        user = "admin"
        password = "password123"

        # Initialize Workflow
        login_flow = LoginFlow(driver)

        # Execute & Verify
        status = login_flow.do_login_and_verify(user, password)
        
        assert status is True, "Login failed: Welcome message not displayed"
