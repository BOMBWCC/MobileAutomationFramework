import os
from pathlib import Path

class FileHelper:
    @staticmethod
    def get_project_root() -> Path:
        """
        Returns the root directory of the project.
        Assumes this file is located in <root>/utils/file_helper.py
        """
        # Go up two levels from utils/file_helper.py
        return Path(__file__).parent.parent.resolve()

    @staticmethod
    def resolve_path(relative_path: str) -> Path:
        """
        Resolves a relative path to an absolute path based on project root.
        :param relative_path: Path relative to project root (e.g., 'data/test_data.xlsx')
        :return: Absolute Path object
        """
        return FileHelper.get_project_root() / relative_path

    @staticmethod
    def get_absolute_path(relative_path: str) -> str:
        """
        Get absolute path relative to the project root directory.
        """
        return str(FileHelper.get_project_root() / relative_path)

    @staticmethod
    def join_path(*args) -> str:
        """
        Joins path components relative to the project root.
        """
        return str(FileHelper.get_project_root().joinpath(*args))

# For backward compatibility or direct function import if needed
get_project_root = FileHelper.get_project_root
resolve_path = FileHelper.resolve_path
get_absolute_path = FileHelper.get_absolute_path
join_path = FileHelper.join_path

if __name__ == "__main__":
    print(f"Project Root: {FileHelper.get_project_root()}")
