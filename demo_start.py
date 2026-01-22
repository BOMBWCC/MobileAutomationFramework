import sys
import os

# Ensure project root is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from drivers.driver_factory import DriverFactory
from utils.logger import logger

def main():
    logger.info("Starting Demo...")
    
    driver = None
    try:
        # NOTE: This will fail if Appium Server is not running or no device is connected
        # But it verifies the code logic imports and factory structure.
        driver = DriverFactory.start_driver("Android")
        logger.info(f"Driver Session ID: {driver.session_id}")
        
    except Exception as e:
        logger.warning(f"Demo failed to start driver (Expected if no Appium/Device): {e}")
    finally:
        if driver:
            DriverFactory.quit_driver(driver)
        logger.info("Demo Finished.")

if __name__ == "__main__":
    main()
