from appium.webdriver.webdriver import WebDriver
from pages.android.login_page import LoginPage
from pages.android.home_page import HomePage
from utils.logger import logger

class BaseWorkflow:
    """
    Base class for all workflows.
    Manages the driver and provides lazy access to Page Objects.
    """
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self._login_page = None
        self._home_page = None

    @property
    def login_page(self) -> LoginPage:
        if not self._login_page:
            self._login_page = LoginPage(self.driver)
        return self._login_page

    @property
    def home_page(self) -> HomePage:
        if not self._home_page:
            self._home_page = HomePage(self.driver)
        return self._home_page

    def restart_app(self):
        """
        Restarts the application.
        """
        logger.info("Restarting App...")
        self.driver.terminate_app(self.driver.current_package)
        self.driver.activate_app(self.driver.current_package)

    def background_app(self, seconds: int = 5):
        """
        Puts the app in background for X seconds.
        """
        logger.info(f"Backgrounding App for {seconds}s...")
        self.driver.background_app(seconds)
