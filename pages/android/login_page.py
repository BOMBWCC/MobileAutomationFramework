from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from utils.logger import logger

class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = (AppiumBy.ID, "com.example.demo:id/et_username")
    PASSWORD_INPUT = (AppiumBy.ID, "com.example.demo:id/et_password")
    LOGIN_BUTTON = (AppiumBy.ID, "com.example.demo:id/btn_login")

    def login(self, user: str, password: str):
        """
        Performs login action.
        """
        logger.info(f"Attempting login with user: {user}")
        self.input_text(self.USERNAME_INPUT, user)
        self.input_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)