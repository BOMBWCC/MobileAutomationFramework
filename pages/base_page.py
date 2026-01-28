import time
from typing import Optional, List
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

from config.global_config import GlobalConfig
from utils.logger import logger
from pages.mixins.action_mixin import ActionMixin

class BasePage(ActionMixin):
    """
    Base Class for all Page Objects.
    Wraps WebDriverWait and common interaction logic.
    """

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.driver = driver
        self.wait = WebDriverWait(self.driver, GlobalConfig.EXPLICIT_WAIT)

    def find_element(self, locator: tuple, timeout: Optional[int] = None) -> WebElement:
        """
        Finds a single element with explicit wait.
        :param locator: Tuple (By, "value") e.g., (AppiumBy.ID, "com.example:id/btn")
        :param timeout: Optional override for timeout
        """
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        try:
            return wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            logger.error(f"Element not found within timeout: {locator}")
            raise

    def find_elements(self, locator: tuple, timeout: Optional[int] = None) -> List[WebElement]:
        """
        Finds multiple elements.
        """
        wait = WebDriverWait(self.driver, timeout) if timeout else self.wait
        try:
            return wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            logger.warning(f"No elements found for: {locator}")
            return []

    def click_element(self, locator: tuple):
        """
        Waits for element to be clickable and clicks it.
        """
        logger.info(f"Clicking element: {locator}")
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
        except Exception as e:
            logger.error(f"Failed to click element {locator}: {e}")
            raise

    def input_text(self, locator: tuple, text: str, clear: bool = True):
        """
         inputs text into an element.
        :param clear: If True, clears the field before typing.
        """
        logger.info(f"Inputting text '{text}' into {locator}")
        try:
            element = self.find_element(locator)
            if clear:
                element.clear()
            element.send_keys(text)
            # Optionally hide keyboard if needed, but usually Appium handles it or we use a separate method
        except Exception as e:
            logger.error(f"Failed to input text into {locator}: {e}")
            raise

    def get_text(self, locator: tuple) -> str:
        """
        Retrieves text from an element, falling back to content-desc if text is empty.
        """
        try:
            element = self.find_element(locator)
            text = element.text
            if not text:
                text = element.get_attribute("content-desc")
            return text if text else ""
        except Exception as e:
            logger.error(f"Failed to get text from {locator}: {e}")
            return ""

    def get_attribute(self, locator: tuple, attribute: str) -> str:
        """
        wrapper for get_attribute
        """
        try:
            element = self.find_element(locator)
            val = element.get_attribute(attribute)
            return val if val else ""
        except Exception as e:
            logger.error(f"Failed to get attribute {attribute} from {locator}: {e}")
            return ""

    def is_element_exist(self, locator: tuple, timeout: int = 3) -> bool:
        """
        Checks if an element exists without raising exception.
        """
        try:
            self.find_element(locator, timeout=timeout)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def save_screenshot(self, name: str):
        """
        Saves a screenshot to the reports directory.
        """
        import os
        from datetime import datetime
        
        # Ensure directory exists
        path = GlobalConfig.PROJECT_ROOT / "reports" / "screenshots"
        path.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        full_path = path / filename
        
        try:
            self.driver.save_screenshot(str(full_path))
            logger.info(f"Screenshot saved: {full_path}")
        except Exception as e:
            logger.error(f"Failed to save screenshot: {e}")

    def tap_by_coordinates(self, x_pct: float, y_pct: float):
        """
        Taps at coordinates specified as percentages of screen width and height.
        """
        x = int(self.width * x_pct)
        y = int(self.height * y_pct)
        self.tap_coordinates(x, y)

    def find_image_element(self, template_name: str, threshold: float = 0.8):
        """
        Finds an element by image template matching.
        Returns an object that has a .click() method to simulate element-like behavior.
        """
        from utils.cv_helper import CVHelper
        from utils.file_helper import FileHelper
        
        template_path = str(GlobalConfig.PROJECT_ROOT / "data" / "templates" / template_name)
        screenshot_bytes = self.driver.get_screenshot_as_png()
        
        coords = CVHelper.find_image_center(template_path, screenshot_bytes, threshold)
        if coords:
            class MockElement:
                def __init__(self, page, x, y):
                    self.page = page
                    self.x = x
                    self.y = y
                def click(self):
                    self.page.tap_coordinates(self.x, self.y)
            
            return MockElement(self, coords[0], coords[1])
        else:
            raise NoSuchElementException(f"Could not find image template: {template_name}")
    
    def format_locator(self, locator: tuple, *args) -> tuple:
        """
        Formats a dynamic locator with arguments.
        """
        return (locator[0], locator[1].format(*args))


