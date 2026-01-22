import functools
import time
from typing import Callable, Type, Tuple, Optional, Any
from utils.logger import logger

def log_step(msg: Optional[str] = None, level: str = "INFO"):
    """
    [Step Recorder]
    Logs the start and end of a function execution.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            step_msg = msg or f"Executing {func.__name__}"
            logger.log(level, f"[STEP START] {step_msg}")
            # Optional: Log args if needed, but keeping it clean for now
            try:
                result = func(*args, **kwargs)
                logger.log(level, f"[STEP END] {step_msg}")
                return result
            except Exception as e:
                logger.error(f"[STEP FAILED] {step_msg}: {e}")
                raise e
        return wrapper
    return decorator

def time_it(func: Callable):
    """
    [Time Monitoring]
    Records how long a function takes to execute.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            end_time = time.time()
            duration = end_time - start_time
            logger.info(f"Function '{func.__name__}' took {duration:.2f} seconds")
    return wrapper

def retry(max_attempts: int = 3, delay: int = 1, exceptions: Tuple[Type[Exception], ...] = (Exception,)):
    """
    [Auto Retry]
    Retries the function upon encountering specified exceptions.
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for i in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    logger.warning(f"Retrying {func.__name__}... ({i + 1}/{max_attempts}) due to: {e}")
                    time.sleep(delay)
            
            logger.error(f"Function {func.__name__} failed after {max_attempts} attempts.")
            raise last_exception
        return wrapper
    return decorator

def handle_exception(default_return: Any = None, screenshot: bool = False):
    """
    [Exception Swallowing]
    Catches exceptions, logs them, and returns a default value.
    Optionally takes a screenshot if 'self.driver' is available in args[0].
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Exception in {func.__name__}: {e}")
                if screenshot and args:
                    instance = args[0]
                    if hasattr(instance, 'driver') and hasattr(instance.driver, 'save_screenshot'):
                        try:
                            # Using a generic name, ideally should use a timestamped helper
                            instance.driver.save_screenshot(f"error_{func.__name__}.png")
                            logger.info("Screenshot captured during exception handling.")
                        except Exception as s_e:
                            logger.error(f"Failed to capture screenshot: {s_e}")
                return default_return
        return wrapper
    return decorator

def singleton(cls):
    """
    [Singleton Pattern]
    Ensures a class has only one instance.
    """
    _instances = {}
    
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in _instances:
            _instances[cls] = cls(*args, **kwargs)
        return _instances[cls]
    return get_instance
