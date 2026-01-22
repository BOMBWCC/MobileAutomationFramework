from datetime import datetime
from utils.file_helper import resolve_path

class LoggingConfig:
    # Log Directory
    LOG_DIR = resolve_path("logs")
    
    # Log Filename Pattern
    RUN_LOG_FILE = LOG_DIR / f"runtime_{datetime.now().strftime('%Y%m%d')}.log"
    ERROR_LOG_FILE = LOG_DIR / f"error_{datetime.now().strftime('%Y%m%d')}.log"

    # Rotation & Retention
    ROTATION = "10 MB"
    RETENTION = "7 days"
    
    # Log Levels
    CONSOLE_LEVEL = "INFO"
    FILE_LEVEL = "DEBUG"

    # Format
    LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
