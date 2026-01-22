import subprocess
from typing import List, Optional
from utils.logger import logger

class ADBHelper:
    """
    Android System Operations Tool.
    Handles operations that Appium Driver cannot perform directly.
    """

    @staticmethod
    def execute_adb_command(cmd: str, device_id: Optional[str] = None) -> str:
        """
        [Low-level Wrapper]
        Executes an ADB command and returns the output.
        """
        target = f"-s {device_id} " if device_id else ""
        full_cmd = f"adb {target}{cmd}"
        
        logger.debug(f"Executing ADB: {full_cmd}")
        try:
            output = subprocess.check_output(full_cmd, shell=True, stderr=subprocess.STDOUT)
            return output.decode('utf-8').strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"ADB Execution Failed: {e.output.decode('utf-8')}")
            return ""
        except Exception as e:
            logger.error(f"ADB Unknown Error: {e}")
            return ""

    @staticmethod
    def get_connected_devices() -> List[str]:
        """
        [Device Check]
        Returns a list of connected device IDs.
        """
        output = ADBHelper.execute_adb_command("devices")
        devices = []
        for line in output.split('\n'):
            if "\tdevice" in line:
                devices.append(line.split('\t')[0])
        return devices

    # --- IME Management ---
    @staticmethod
    def list_available_imes(device_id: Optional[str] = None) -> List[str]:
        output = ADBHelper.execute_adb_command("shell ime list -a", device_id)
        # Extract ImeId from output (parsing logic simplified for robustness)
        imes = []
        for line in output.splitlines():
            if "mId=" in line:
                 imes.append(line.split("mId=")[1].strip())
        return imes

    @staticmethod
    def get_current_ime(device_id: Optional[str] = None) -> str:
        return ADBHelper.execute_adb_command("shell settings get secure default_input_method", device_id)

    @staticmethod
    def set_ime(ime_id: str, device_id: Optional[str] = None):
        ADBHelper.execute_adb_command(f"shell ime set {ime_id}", device_id)

    @staticmethod
    def enable_ime(ime_id: str, device_id: Optional[str] = None):
        ADBHelper.execute_adb_command(f"shell ime enable {ime_id}", device_id)

    # --- App Management ---
    @staticmethod
    def clear_app_data(package_name: str, device_id: Optional[str] = None):
        """[Reset App]"""
        logger.info(f"Clearing app data: {package_name}")
        ADBHelper.execute_adb_command(f"shell pm clear {package_name}", device_id)

    @staticmethod
    def stop_app(package_name: str, device_id: Optional[str] = None):
        """[Force Stop Process]"""
        ADBHelper.execute_adb_command(f"shell am force-stop {package_name}", device_id)

    @staticmethod
    def is_app_installed(package_name: str, device_id: Optional[str] = None) -> bool:
        output = ADBHelper.execute_adb_command("shell pm list packages", device_id)
        return package_name in output

    # --- System Control ---
    @staticmethod
    def get_device_ip(device_id: Optional[str] = None) -> str:
        """Get device Wi-Fi IP."""
        # Note: parsing might vary by device/android version, keeping generic
        return ADBHelper.execute_adb_command("shell ip -f inet addr show wlan0", device_id)

    @staticmethod
    def input_text_adb(text: str, device_id: Optional[str] = None):
        """[Backup Input] Supports ASCII only."""
        ADBHelper.execute_adb_command(f"shell input text '{text}'", device_id)

    @staticmethod
    def toggle_wifi(status: bool, device_id: Optional[str] = None):
        state = "enable" if status else "disable"
        ADBHelper.execute_adb_command(f"shell svc wifi {state}", device_id)

    @staticmethod
    def screen_record(filename: str, duration: int = 10, device_id: Optional[str] = None):
        """
        [Screen Record]
        Note: This is a blocking call if strictly following subprocess.
        In real usage, this should likely be async or run in a separate thread.
        For this implementation, we assume basic synchronous execution.
        """
        remote_path = f"/sdcard/{filename}"
        ADBHelper.execute_adb_command(f"shell screenrecord --time-limit {duration} {remote_path}", device_id)
        # Pull logic would typically go here or be a separate call
