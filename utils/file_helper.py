import os
from pathlib import Path

def get_project_root() -> Path:
    """
    Returns the root directory of the project.
    Assumes this file is located in <root>/utils/file_helper.py
    """
    # Go up two levels from utils/file_helper.py
    return Path(__file__).parent.parent.resolve()

def resolve_path(relative_path: str) -> Path:
    """
    Resolves a relative path to an absolute path based on project root.
    :param relative_path: Path relative to project root (e.g., 'data/test_data.xlsx')
    :return: Absolute Path object
    """
    return get_project_root() / relative_path

if __name__ == "__main__":
    print(f"Project Root: {get_project_root()}")
