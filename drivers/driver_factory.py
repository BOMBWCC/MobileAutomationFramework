from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions
from config.global_config import GlobalConfig
from utils.logger import logger

class DriverFactory:
    @staticmethod
    def start_driver(platform_name: str = "Android") -> webdriver.Remote:
        """
        Initializes the Appium Driver based on platform.
        """
        logger.info(f"Initializing Driver for Platform: {platform_name}")
        
        try:
            if platform_name.lower() == "android":
                options = UiAutomator2Options()
                options.platform_name = "Android"
                options.automation_name = "UiAutomator2"
                options.device_name = GlobalConfig.DEVICE_NAME
                
                if GlobalConfig.APP_PACKAGE:
                    options.app_package = GlobalConfig.APP_PACKAGE
                if GlobalConfig.APP_ACTIVITY:
                    options.app_activity = GlobalConfig.APP_ACTIVITY
                if GlobalConfig.APP_PATH:
                    options.app = GlobalConfig.APP_PATH
                if GlobalConfig.UDID:
                    options.udid = GlobalConfig.UDID
                if GlobalConfig.PLATFORM_VERSION:
                    options.platform_version = GlobalConfig.PLATFORM_VERSION
                
                # Auto Grant Permissions
                options.auto_grant_permissions = True
                
                command_executor = GlobalConfig.get_appium_url()
                logger.debug(f"Connecting to Appium Server at: {command_executor}")
                logger.debug(f"Capabilities: {options.to_capabilities()}")

                driver = webdriver.Remote(command_executor=command_executor, options=options)
                logger.success("Driver initialized successfully!")
                return driver
            
            elif platform_name.lower() == "ios":
                 # Future Implementation for iOS
                 raise NotImplementedError("iOS Driver not yet implemented")
            else:
                raise ValueError(f"Unsupported Platform: {platform_name}")

        except Exception as e:
            logger.error(f"Failed to initialize driver: {e}")
            raise e

    @staticmethod
    def quit_driver(driver: webdriver.Remote):
        """
        Safely quits the driver instance.
        """
        if driver:
            try:
                logger.info("Quitting Driver...")
                driver.quit()
                logger.success("Driver quit successfully.")
            except Exception as e:
                logger.error(f"Error while quitting driver: {e}")
