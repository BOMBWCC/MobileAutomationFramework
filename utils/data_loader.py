import yaml
import json
import csv
import logging
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional
try:
    import openpyxl
except ImportError:
    openpyxl = None

from utils.logger import logger
from utils.file_helper import get_absolute_path

def _process_dynamic_values(data: Any) -> Any:
    """
    [Internal Helper]
    Recursively traverses the data structure.
    If a string contains '%', it attempts to format it using datetime.strftime.
    Example: "User_%Y%m%d" -> "User_20231027"
    """
    if isinstance(data, dict):
        return {k: _process_dynamic_values(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [_process_dynamic_values(item) for item in data]
    elif isinstance(data, str):
        if "%" in data:
            try:
                return datetime.now().strftime(data)
            except Exception:
                return data
        return data
    else:
        return data

def load_yaml(file_path: str) -> Any:
    """
    [Basic Reading]
    Loads a YAML file and returns its content.
    """
    abs_path = get_absolute_path(file_path)
    try:
        with open(abs_path, 'r', encoding='utf-8') as f:
            raw_data = yaml.safe_load(f)
            # 处理动态参数
            return _process_dynamic_values(raw_data)
    except FileNotFoundError:
        logger.error(f"YAML file not found: {abs_path}")
        return {}
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file {abs_path}: {e}")
        return {}

def get_account(role: str) -> Dict[str, str]:
    """
    [Business Wrapper]
    Retrieves account details for a specific role from 'data/test_accounts.yaml'.
    """
    data = load_yaml("data/test_accounts.yaml")
    return data.get(role, {})

def load_excel(file_path: str, sheet_name: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    [Core Reading]
    Loads an Excel file and returns a list of dictionaries.
    Requres 'openpyxl' installed.
    """
    if not openpyxl:
        logger.error("openpyxl library is not installed. Cannot read Excel files.")
        return []

    abs_path = get_absolute_path(file_path)
    try:
        workbook = openpyxl.load_workbook(abs_path, data_only=True)
        sheet = workbook[sheet_name] if sheet_name else workbook.active

        rows = list(sheet.iter_rows(values_only=True))
        if not rows:
            return []

        headers = rows[0]
        data = []
        for row in rows[1:]:
            # Zip headers with row data to create a dict
            row_data = dict(zip(headers, row))
            data.append(row_data)

        # Excel 数据也同样支持动态替换
        return _process_dynamic_values(data)
    except FileNotFoundError:
        logger.error(f"Excel file not found: {abs_path}")
        return []
    except Exception as e:
        logger.error(f"Error reading Excel file {abs_path}: {e}")
        return []

def load_json(file_path: str) -> Dict[str, Any]:
    """
    [JSON Reading]
    """
    abs_path = get_absolute_path(file_path)
    try:
        with open(abs_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
            return _process_dynamic_values(raw_data)
    except Exception as e:
        logger.error(f"Error reading JSON file {abs_path}: {e}")
        return {}

def load_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    [CSV Reading]
    """
    abs_path = get_absolute_path(file_path)
    try:
        with open(abs_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            raw_data = list(reader)
            return _process_dynamic_values(raw_data)
    except Exception as e:
        logger.error(f"Error reading CSV file {abs_path}: {e}")
        return []