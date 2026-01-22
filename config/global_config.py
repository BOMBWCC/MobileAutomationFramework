import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class GlobalConfig:
    # Project Root
    PROJECT_ROOT = Path(__file__).parent.parent.resolve()

    # Appium Config
    APPIUM_HOST = os.getenv("APPIUM_HOST", "127.0.0.1")
    APPIUM_PORT = int(os.getenv("APPIUM_PORT", 4723))
    
    # Device Config
    PLATFORM_NAME = os.getenv("PLATFORM_NAME", "Android")
    DEVICE_NAME = os.getenv("DEVICE_NAME", "emulator-5554")
    UDID = os.getenv("UDID", None)
    PLATFORM_VERSION = os.getenv("PLATFORM_VERSION", None)

    # App Config
    APP_PACKAGE = os.getenv("APP_PACKAGE", "")
    APP_ACTIVITY = os.getenv("APP_ACTIVITY", "")
    APP_PATH = os.getenv("APP_PATH", "")

    # Wait Config
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", 10))
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", 20))

    @classmethod
    def get_appium_url(cls) -> str:
        return f"http://{cls.APPIUM_HOST}:{cls.APPIUM_PORT}"
