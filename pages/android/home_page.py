from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from utils.logger import logger

class HomePage(BasePage):
    # Locators
    WELCOME_TITLE = (AppiumBy.XPATH, "//*[@text='Welcome back!']")

    def is_welcome_displayed(self) -> bool:
        """
        Verifies if the welcome message is displayed.
        """
        is_displayed = self.is_element_exist(self.WELCOME_TITLE)
        logger.info(f"Welcome message displayed: {is_displayed}")
        return is_displayed