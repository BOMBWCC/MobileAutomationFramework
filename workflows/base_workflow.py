from selenium.webdriver.remote.webdriver import WebDriver
from utils.logger import logger

class BaseWorkflow:
    def __init__(self, driver: WebDriver):
        self.driver = driver