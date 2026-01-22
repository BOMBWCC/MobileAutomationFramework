import pytest
import allure
import os
from drivers.driver_factory import DriverFactory
from config.global_config import GlobalConfig
from utils.logger import logger

@pytest.fixture(scope="function")
def driver(request):
    """
    Pytest fixture to handle Driver lifecycle.
    """
    driver_instance = None
    try:
        # Initialize Driver
        driver_instance = DriverFactory.start_driver(GlobalConfig.PLATFORM_NAME)
        yield driver_instance
    except Exception as e:
        logger.error(f"Driver Fixture Failed: {e}")
        raise e
    finally:
        # Teardown Driver
        DriverFactory.quit_driver(driver_instance)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshot on test failure.
    """
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()

    # Check if test failed
    if report.when == "call" and report.failed:
        logger.error(f"Test Failed: {item.nodeid}")
        
        # Retrieve driver from fixture
        driver = item.funcargs.get("driver", None)
        
        if driver:
            try:
                # Capture Screenshot
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name="failure_screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
                logger.info("Screenshot attached to Allure report")
            except Exception as e:
                logger.error(f"Failed to capture screenshot: {e}")
