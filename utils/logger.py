import sys
from loguru import logger
from config.logging_config import LoggingConfig

# Remove default handler
logger.remove()

# Add Console Handler
logger.add(
    sys.stdout,
    level=LoggingConfig.CONSOLE_LEVEL,
    format=LoggingConfig.LOG_FORMAT,
    colorize=True
)

# Add File Handler (Runtime)
logger.add(
    str(LoggingConfig.RUN_LOG_FILE),
    level=LoggingConfig.FILE_LEVEL,
    format=LoggingConfig.LOG_FORMAT,
    rotation=LoggingConfig.ROTATION,
    retention=LoggingConfig.RETENTION,
    encoding="utf-8"
)

# Add File Handler (Errors)
logger.add(
    str(LoggingConfig.ERROR_LOG_FILE),
    level="ERROR",
    format=LoggingConfig.LOG_FORMAT,
    rotation=LoggingConfig.ROTATION,
    retention=LoggingConfig.RETENTION,
    encoding="utf-8",
    backtrace=True,
    diagnose=True
)

# Expose the configured logger
__all__ = ["logger"]
