from typing import Any, List, Dict, Optional
from utils.logger import logger

class SoftAssert:
    """
    [Error Collection]
    Collects multiple assertion errors and raises them all at once.
    """
    def __init__(self):
        self._errors = []

    def expect_true(self, condition: bool, msg: str):
        if not condition:
            error_msg = f"[Failure] {msg}"
            self._errors.append(error_msg)
            logger.error(error_msg)

    def expect_equal(self, actual: Any, expected: Any, msg: str):
        if actual != expected:
            error_msg = f"[Failure] {msg} - Expected: {expected}, Got: {actual}"
            self._errors.append(error_msg)
            logger.error(error_msg)

    def assert_all(self):
        """
        [Final Verdict]
        Raises AssertionError if any errors were collected.
        """
        if self._errors:
            full_msg = "\n".join(self._errors)
            raise AssertionError(f"Soft Assert failed with {len(self._errors)} errors:\n{full_msg}")

# --- Data Verification ---
def assert_list_sorted(data_list: List[Any], reverse: bool = False):
    """[Sort Check]"""
    sorted_list = sorted(data_list, reverse=reverse)
    if data_list != sorted_list:
        logger.error(f"List not sorted. Actual: {data_list} vs Expected: {sorted_list}")
        raise AssertionError("List is not sorted as expected.")

def assert_list_contains(full_list: List[Any], sub_list: List[Any]):
    """[Subset Check]"""
    missing = [item for item in sub_list if item not in full_list]
    if missing:
        logger.error(f"Items missing from list: {missing}")
        raise AssertionError(f"List does not contain all expected items: {missing}")

def assert_dict_subset(actual_dict: Dict, expected_dict: Dict):
    """[JSON Partial Match]"""
    mismatches = []
    for k, v in expected_dict.items():
        if k not in actual_dict:
            mismatches.append(f"Missing key: {k}")
        elif actual_dict[k] != v:
            mismatches.append(f"Key '{k}': Expected '{v}', Got '{actual_dict[k]}'")
    
    if mismatches:
        raise AssertionError(f"Dict subset match failed:\n" + "\n".join(mismatches))

# --- Business Assertions ---
def assert_text_contains(full_text: str, keyword: str):
    if keyword not in full_text:
        raise AssertionError(f"Keyword '{keyword}' not found in text: '{full_text}'")

def assert_not_empty(value: Any, msg: str = "Value is empty"):
    if not value:
        raise AssertionError(msg)

def assert_file_exists(file_path: str):
    import os
    if not os.path.exists(file_path):
        raise AssertionError(f"File not found: {file_path}")
