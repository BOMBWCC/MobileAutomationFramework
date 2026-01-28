from typing import Optional, Tuple
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.remote.webdriver import WebDriver
from utils.logger import logger

class ActionMixin:
    """
    Mixin class for W3C Actions (Swipe, Tap, Scroll, etc.)
    Strictly avoids deprecated TouchAction.
    """
    def __init__(self, driver: WebDriver):
        self.driver = driver
        # Screen dimensions cache
        self._window_size = None

    @property
    def window_size(self) -> dict:
        if not self._window_size:
            self._window_size = self.driver.get_window_size()
        return self._window_size

    @property
    def width(self) -> int:
        return self.window_size.get('width', 0)

    @property
    def height(self) -> int:
        return self.window_size.get('height', 0)

    def swipe_percentage(self, start_x: float, start_y: float, end_x: float, end_y: float, duration_ms: int = 500):
        """
        Swipe from start percentage to end percentage of screen size.
        E.g. (0.5, 0.8, 0.5, 0.2) swipes up.
        """
        x_start = int(self.width * start_x)
        y_start = int(self.height * start_y)
        x_end = int(self.width * end_x)
        y_end = int(self.height * end_y)

        logger.debug(f"Swiping from ({x_start}, {y_start}) to ({x_end}, {y_end})")

        actions = ActionChains(self.driver)
        # The w3c_actions attribute is already an ActionBuilder instance
        actions.w3c_actions.pointer_action.move_to_location(x_start, y_start)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(duration_ms / 1000)
        actions.w3c_actions.pointer_action.move_to_location(x_end, y_end)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

    def swipe_up(self, duration_ms: int = 800):
        """Swipe from bottom to top"""
        self.swipe_percentage(0.5, 0.8, 0.5, 0.2, duration_ms)

    def swipe_down(self, duration_ms: int = 800):
        """Swipe from top to bottom"""
        self.swipe_percentage(0.5, 0.2, 0.5, 0.8, duration_ms)

    def swipe_left(self, duration_ms: int = 800):
        """Swipe from right to left"""
        self.swipe_percentage(0.9, 0.5, 0.1, 0.5, duration_ms)

    def swipe_right(self, duration_ms: int = 800):
        """Swipe from left to right"""
        self.swipe_percentage(0.1, 0.5, 0.9, 0.5, duration_ms)

    def tap_coordinates(self, x: int, y: int):
        """Tap at specific x, y coordinates"""
        logger.debug(f"Tapping at ({x}, {y})")
        actions = ActionChains(self.driver)
        # The w3c_actions attribute is already an ActionBuilder instance
        actions.w3c_actions.pointer_action.move_to_location(x, y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()

        actions.perform()
