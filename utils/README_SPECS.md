## File: `utils/adb_helper.py`

**Role**: Android System Operations Tool
**Responsibility**: Handles operations that Appium Driver cannot perform directly or operations where ADB is more efficient/stable.
**Core Implementation**: Invokes the `adb` command installed on the host machine via Python's `subprocess` module.

### A. Base Executor

*The low-level entry point for all ADB methods, handling command assembly and encoding issues.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`execute_adb_command`** | `cmd`, `device_id=None` | **[Low-level Wrapper]**<br>

<br>1. Receive ADB sub-command (e.g., `shell pm list`).<br>

<br>2. Assemble full command: `adb -s {device_id} {cmd}`.<br>

<br>3. Execute using `subprocess.check_output`.<br>

<br>4. Return decoded string (strip leading/trailing whitespace).<br>

<br>5. Catch exceptions and log errors. |
| **`get_connected_devices`** | None | **[Device Check]** Execute `adb devices` and return a list of connected device IDs. Used to automatically identify `device_id`. |

### B. Input Method Management (IME)

*Solves a major automation pain point: Appium keyboard cannot type Chinese or blocks UI, while system keyboards pop up unexpectedly.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`list_available_imes`** | None | Execute `adb shell ime list -a`. Return a list of all installed Input Method IDs. |
| **`get_current_ime`** | None | Execute `adb shell settings get secure default_input_method`. Return the ID of the currently active input method. |
| **`set_ime`** | `ime_id` | Execute `adb shell ime set {ime_id}`. Used to switch between Appium UnicodeKeyboard (Invisible/Supports Chinese) and System Keyboard (e.g., Gboard/Sogou). |
| **`enable_ime`** | `ime_id` | Execute `adb shell ime enable {ime_id}`. Ensure the input method is enabled. |

### C. App Management

*A cleanup method that is more thorough than Appium Driver.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`clear_app_data`** | `package_name` | **[Reset App]** Execute `adb shell pm clear {package_name}`.<br>

<br>Effect: Equivalent to uninstalling and reinstalling; clears all cache, login states, and databases. |
| **`stop_app`** | `package_name` | **[Force Stop Process]** Execute `adb shell am force-stop {package_name}`. |
| **`is_app_installed`** | `package_name` | Execute `adb shell pm list packages`. Check if the package name exists in the returned list. |

### D. System Control & Info

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`get_device_ip`** | None | Get device Wi-Fi IP address (usually for wireless debugging or network checking). Command: `adb shell ip -f inet addr show wlan0`. |
| **`input_text_adb`** | `text` | **[Backup Input]** Execute `adb shell input text {text}`.<br>

<br>*Note: Supports ASCII characters only (no Chinese), but effective in extreme scenarios where input fields cannot be located.* |
| **`toggle_wifi`** | `status(bool)` | **[WiFi Switch]** Execute `adb shell svc wifi enable` or `disable`. |
| **`screen_record`** | `filename`, `duration` | **[Screen Record]** Execute `adb shell screenrecord --time-limit {duration} /sdcard/{filename}`.<br>

<br>Execute `pull` to fetch the file to local machine after recording. |

## File: `utils/assert_helper.py`

**Role**: Advanced Assertion Utility Library
**Responsibility**: Compensates for the limitations of native `assert`. Provides **Soft Assertions** (collect errors without stopping) and **Complex Data Verification** (List sorting, JSON comparison).

### A. SoftAssert Class

*This is a critical feature for automation. For example, when verifying if prices for 10 items in a list are correct, a standard `assert` stops at the first failure. Soft asserts allow running all 10 checks and reporting errors collectively at the end.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`__init__`** | None | Initialize an empty list `self._errors = []` to collect error messages. |
| **`expect_true`** | `condition`, `msg` | **[Error Collection]** Check if `condition` is True.<br>

<br>If False, **DO NOT raise an exception**; instead, append `msg` to the `self._errors` list and print an Error log. |
| **`expect_equal`** | `actual`, `expected`, `msg` | **[Error Collection]** Check if `actual == expected`.<br>

<br>If not equal, append a formatted error message ("Expected A but got B...") to `self._errors`. |
| **`assert_all`** | None | **[Final Verdict]** Check if `self._errors` is empty.<br>

<br>If not empty, join all collected errors into a single long string and **raise AssertionError** to expose all issues at once. |

### B. Data Verification

*Assertion wrappers for complex data structures like lists and dictionaries.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`assert_list_sorted`** | `data_list`, `reverse=False` | **[Sort Check]**<br>

<br>1. Copy `data_list` to `sorted_list`.<br>

<br>2. Sort `sorted_list` (ascending/descending based on `reverse`).<br>

<br>3. Assert `data_list == sorted_list`.<br>

<br>4. Failure message: "List not sorted as expected". |
| **`assert_list_contains`** | `full_list`, `sub_list` | **[Subset Check]**<br>

<br>Verify that all elements in `sub_list` exist within `full_list`.<br>

<br>Used to verify if search results contain keywords. |
| **`assert_dict_subset`** | `actual_dict`, `expected_dict` | **[JSON Partial Match]**<br>

<br>Verify that all key-value pairs in `expected_dict` exist and match in `actual_dict`.<br>

<br>*Scenario: API returns 100 fields, UI only shows 3; we assert only those 3 and ignore the rest.* |

### C. Business Assertions

*Wrappers around basic asserts to add logging and make errors more readable.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`assert_text_contains`** | `full_text`, `keyword` | Check if `keyword` is contained within `full_text`.<br>

<br>Print a clear Diff log upon failure. |
| **`assert_not_empty`** | `value`, `msg` | Assert that `value` is neither `None` nor an empty string/list. |
| **`assert_file_exists`** | `file_path` | Check if the file exists (commonly used to verify if a download was successful). |

## File: `utils/cv_helper.py`

**Role**: Image Processing & Computer Vision Tool
**Responsibility**: Solves positioning issues for **Non-Native Controls** (e.g., Unity games, H5 Canvas, complex custom Views) and performs **UI Visual Regression Testing**.
**Core Dependencies**: `opencv-python`, `numpy`.

### A. Template Matching

*This is the most common CV function in automation: finding the position of a small icon in a screenshot, calculating coordinates, and instructing Appium to click.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`find_image_center`** | `target_img_path`, `source_img_path=None`, `threshold=0.8` | **[Core Positioning]**<br>

<br>1. If `source_img_path` is None, retrieve current screenshot from Driver (must convert to CV2 format).<br>

<br>2. Read `target_img_path` (the small icon you want to find).<br>

<br>3. Use `cv2.matchTemplate` method (recommend `TM_CCOEFF_NORMED`) for matching.<br>

<br>4. Get coordinates of the maximum match value.<br>

<br>5. If match score > `threshold`, calculate and return the **Center Coordinates (x, y)** of the target; otherwise return None. |
| **`is_image_exist`** | `target_img_path`, `threshold=0.8` | **[Boolean Check]**<br>

<br>Call `find_image_center`.<br>

<br>If coordinates are returned (not None), return `True`; otherwise return `False`.<br>

<br>Used to assert if an icon is displayed. |
| **`find_all_occurrences`** | `target_img_path`, `threshold=0.8` | **[Multi-Target Search]**<br>

<br>Use `np.where` to find all coordinate points with a match score greater than the threshold.<br>

<br>Return a list of coordinates `[(x1, y1), (x2, y2)...]`.<br>

<br>Scenario: Finding all red blocks in a Match-3 game. |

### B. Image Comparison

*Used for "Visual Assertion" to judge if UI has abnormal changes (e.g., rendering errors, incorrect colors).*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`calculate_ssim`** | `img1_path`, `img2_path` | **[Structural Similarity]**<br>

<br>Use `skimage.metrics.structural_similarity` (SSIM) algorithm to compare two images.<br>

<br>1. Convert both images to grayscale.<br>

<br>2. Resize to match dimensions (if different).<br>

<br>3. Return similarity score (0.0 - 1.0).<br>

<br>4. 1.0 indicates they are identical. |
| **`calculate_hist_similarity`** | `img1_path`, `img2_path` | **[Histogram Comparison]** (Alternative)<br>

<br>Use `cv2.calcHist` to calculate color histograms.<br>

<br>Used to judge if color distribution is consistent (ignoring position differences). |

### C. Preprocessing Helpers

*Handles conversion between Appium screenshot data and OpenCV formats.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`bytes_to_cv2`** | `image_bytes` | **[Format Conversion]**<br>

<br>Receive binary data returned by `driver.get_screenshot_as_png()`.<br>

<br>Use `np.frombuffer` and `cv2.imdecode` to convert directly into an OpenCV image object.<br>

<br>**Advantage**: Avoids IO overhead of "Save screenshot to disk -> Read from disk", making it faster. |
| **`crop_image`** | `image_path`, `rect` | **[Crop]**<br>

<br>Crop image based on `rect` (x, y, w, h) area.<br>

<br>Scenario: When comparing images, crop to compare only the center content, excluding the status bar (time/battery) at the top. |


## File: `utils/data_loader.py`

**Role**: Data-Driven Engine
**Responsibility**: Reads test data from external files (YAML, Excel, JSON, CSV) and converts them into Python objects (List/Dict) for use with Pytest's `@pytest.mark.parametrize`, enabling **separation of data and scripts**.
**Core Dependencies**: `PyYAML`, `openpyxl`, `pandas` (Optional).

### A. YAML Reading (Configuration & Accounts)

*The most common format, used for reading configurations in `config/global_config.py` or `data/test_accounts.yaml`.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`load_yaml`** | `file_path` | **[Basic Reading]**<br>

<br>1. Receive file path.<br>

<br>2. Use `yaml.safe_load()` to open and read the file.<br>

<br>3. Return a Python Dictionary (Dict) or List (List).<br>

<br>4. Catch `FileNotFoundError` and print a clear error log. |
| **`get_account`** | `role` | **[Business Wrapper]** (Optional)<br>

<br>1. Specifically reads `data/test_accounts.yaml`.<br>

<br>2. Returns the corresponding account/password dictionary based on the passed `role` (e.g., "user_vip", "user_normal").<br>

<br>3. Avoids hardcoding paths inside test cases. |

### B. Excel Reading (Batch Test Data)

*The workhorse for test case parameterization. For example, testing 20 exception scenarios for a login interface.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`load_excel`** | `file_path`, `sheet_name=None` | **[Core Reading]**<br>

<br>1. Use `openpyxl` library to open `.xlsx` files.<br>

<br>2. If `sheet_name` is not specified, default to reading the first Sheet.<br>

<br>3. **Read Headers**: Get content of the first row as Keys.<br>

<br>4. **Read Data**: Iterate starting from the second row, mapping each row's data to the headers.<br>

<br>5. **Return Format**: `[{"username": "a", "password": "1"}, {"username": "b", ...}]`.<br>

<br>This format is optimized for `pytest.mark.parametrize`. |

### C. JSON/CSV Reading (Legacy & API)

*Used for reading API Mock data or simple CSV data.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`load_json`** | `file_path` | **[JSON Reading]**<br>

<br>Use `json.load()` to read the file and return a dictionary. |
| **`load_csv`** | `file_path` | **[CSV Reading]**<br>

<br>Use Python's built-in `csv.DictReader`.<br>

<br>Logic is identical to Excel, returning a List of Dicts. |


## File: `utils/file_helper.py`

**Role**: File System Manager
**Responsibility**: Unified management of file paths (resolving "File Not Found" issues and cross-platform path separators) and handling test artifacts (cleaning logs, screenshots).
**Core Dependencies**: `os`, `pathlib`, `shutil`.

### A. Path Resolution

*This is the core functionality. Regardless of where `pytest` is executed (root directory or subdirectory), it guarantees the resolution of the correct file paths.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`get_project_root`** | None | **[Core Anchor]**<br>

<br>1. Get the absolute path of the current file (`utils/file_helper.py`).<br>

<br>2. Navigate up two levels (`../../`) to locate the project root directory `MobileAutomationFramework`.<br>

<br>3. Return the Root Path object (`pathlib.Path`). |
| **`join_path`** | `*args` | **[Path Concatenation]**<br>

<br>1. Call `get_project_root()` to retrieve the root path.<br>

<br>2. Use `os.path.join(root, *args)` to append subsequent path components.<br>

<br>3. **Example**: `join_path("data", "test.xlsx")` -> `/Users/xxx/MobileAuto/data/test.xlsx`. |
| **`get_absolute_path`** | `relative_path` | **[Convert to Absolute]**<br>

<br>Check if the input path is already absolute. If yes, return directly; if no, join it with the Project Root. |

### B. Directory Maintenance

*Used for environment cleanup before testing starts and directory creation during execution.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`ensure_dir_exist`** | `path` | **[Create Directory]**<br>

<br>Receive a directory path. If it does not exist, call `os.makedirs(path, exist_ok=True)` to create it.<br>

<br>Commonly used to create `logs/screenshots/`. |
| **`clean_directory`** | `dir_path` | **[Empty Directory]**<br>

<br>1. Check if the directory exists.<br>

<br>2. Iterate through all files and subdirectories.<br>

<br>3. Use `os.remove` to delete files and `shutil.rmtree` to delete subfolders.<br>

<br>4. **Preserve the root directory itself**, only empty its contents.<br>

<br>Commonly used to clear `reports/` before `conftest.py` starts. |

### C. File Operations

*Assists Driver Factory in locating App installation packages, etc.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`find_files`** | `directory`, `extension` | **[Find by Extension]**<br>

<br>Search for all files ending with `extension` (e.g., `.apk` or `.ipa`) within the specified `directory`.<br>

<br>Return a list of file paths.<br>

<br>Scenario: Automatically locate the latest installation package in the `apps/` directory. |
| **`get_file_extension`** | `file_path` | Retrieve the file extension (used to determine if it is `.apk` or `.ipa`). |


## File: `utils/logger.py`

**Role**: Logging System Wrapper
**Responsibility**: Provides **out-of-the-box** logging capabilities. Handles simultaneous output to **Console** and **File**, and manages automatic file rotation and retention.
**Core Recommendation**: Strongly recommended to use the **`loguru`** library instead of Python's native `logging` module.

### A. Core Configuration

*Initializes logging rules: determines where to save logs, how long to keep them, and their format.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`setup_logger`** | `level="INFO"` | **[Initialization Entry Point]**<br>

<br>1. Remove default Handlers (to prevent duplicate log entries).<br>

<br>2. **Console Output**: Add `sys.stderr`, set format (colorized), default level to INFO.<br>

<br>3. **File Output**: Call `_get_log_path()` to retrieve the path.<br>

<br>4. Configure **Rotation**: "10 MB" (new file every 10MB) or "00:00" (daily rotation).<br>

<br>5. Configure **Retention**: "7 days" (keep logs for the last 7 days only).<br>

<br>6. Configure **Encoding**: "utf-8" (prevent character encoding issues). |
| **`_get_log_path`** | None | **[Path Generation]**<br>

<br>1. Use `utils.file_helper.get_project_root()` to get the root directory.<br>

<br>2. Join with the `logs/` directory.<br>

<br>3. Ensure the directory exists (`os.makedirs`).<br>

<br>4. Return path in the format: `logs/runtime_{time:YYYY-MM-DD}.log`. |

### B. Interceptor (Optional)

*Appium and Selenium have internal logs. This allows "hijacking" them into Loguru for unified management.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`intercept_standard_logging`** | None | **[Hijack Standard Logging]**<br>

<br>Define an `InterceptHandler` class inheriting from `logging.Handler`.<br>

<br>Replace `logging.root` handlers with this interceptor.<br>

<br>Effect: Logs printed internally by `urllib3` or `Appium` will also be output to files following the Loguru format. |

### C. Exposed Singleton

*No need to define a class. Directly instantiate an object for external import.*

| Variable Name | Type | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`logger`** | `Object` | **[Direct Export]**<br>

<br>Directly `from loguru import logger`.<br>

<br>Execute `setup_logger()` at the end of the file to initialize.<br>

<br>External files only need `from utils.logger import logger` to use `logger.info()` directly. |


## File: `utils/notify_helper.py`

**Role**: Message Notification Center
**Responsibility**: Automatically pushes test results (Pass/Fail/Skip/Duration) to Instant Messaging tools (Lark/Feishu, DingTalk, WeCom, Slack) after the test finishes.
**Core Dependencies**: `requests`, `json`.

### A. Base Sender

*Responsible for handling HTTP requests, indifferent to the message content/format.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`post_webhook`** | `url`, `headers`, `payload` | **[Low-level Sender]**<br>

<br>1. Use `requests.post(url, json=payload, headers=headers)`.<br>

<br>2. Set `timeout=10` to prevent hanging.<br>

<br>3. Catch all network exceptions (`ConnectionError`) and log as Error. **Crucial: Sending failure MUST NOT cause the test process to crash.** |

### B. Template Factory

*Responsible for "decorating" raw data into beautiful cards. Choose the implementation based on the IM tool used by your company.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`_format_lark_card`** | `summary` (Dict) | **[Feishu/Lark Card]**<br>

<br>1. Construct JSON structure (`msg_type="interactive"`).<br>

<br>2. **Smart Title Color**: If `summary['failed'] > 0`, set card title background to Red; otherwise, set to Green.<br>

<br>3. **Content Layout**: Include Project Name, Environment, Pass Rate, and Allure Report Link.<br>

<br>4. Return the constructed Dict. |
| **`_format_dingtalk_md`** | `summary` (Dict) | **[DingTalk/WeCom Markdown]**<br>

<br>1. Construct Markdown text.<br>

<br>2. Header: `### UI Automation Report`.<br>

<br>3. List: `- Success: 10`, `- Failed: 2` (Bold and Red font).<br>

<br>4. Link: `[View Details](report_url)`.<br>

<br>5. Mention: If failed, add `@138xxxx` to tag the responsible person. |

### C. Business API

*The only publicly exposed method, usually called in the `pytest_sessionfinish` hook in `conftest.py`.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`send_test_report`** | `summary_data` | **[Main Entry Point]**<br>

<br>1. Read `WEBHOOK_URL` from `config/global_config.py` or `.env`.<br>

<br>2. If URL is empty, return immediately (do not send messages during local debugging).<br>

<br>3. Call `_format_xxx` to generate the platform-specific message body.<br>

<br>4. Call `post_webhook` to send.<br>

<br>5. Log: "Test report pushed to group chat". |

## File: `utils/decorators.py`

**Role**: Magic Decorators Library
**Responsibility**: Uses **AOP (Aspect-Oriented Programming)** to separate non-business logic (logging, retries, error handling, performance monitoring) from business code, keeping the core logic clean.
**Core Dependencies**: `functools`, `time`.

### A. Logging & Monitoring

*Makes code "self-explanatory," eliminating the need to write `logger.info` in every method.*

| Decorator Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`@log_step`** | `msg=None`, `level="INFO"` | **[Step Recorder]**<br>

<br>1. Use `functools.wraps` to preserve original function metadata.<br>

<br>2. **Entry Logic**: If `msg` is provided, log `[STEP START] {msg}`; otherwise, log `[STEP START] Executing {func_name}`.<br>

<br>3. **Args Logging**: (Optional) Log input `args` and `kwargs`.<br>

<br>4. **Exit Logic**: Execute function; upon success, log `[STEP END]`.<br>

<br>5. On exception, raise it to let the outer layer handle it. |
| **`@time_it`** | None | **[Time Monitoring]**<br>

<br>1. Record `start_time = time.time()`.<br>

<br>2. Execute the function.<br>

<br>3. Record `end_time`.<br>

<br>4. Calculate difference and log: `Function {name} took {x.xx} seconds`.<br>

<br>*Scenario: Monitor how long "Login" or "Cold Start" actually takes.* |

### B. Stability Enhancement

*This is the most valuable code in automation, solving issues like "network fluctuation" and "rendering delays."*

| Decorator Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`@retry`** | `max_attempts=3`, `delay=1`, `exceptions=(Exception,)` | **[Auto Retry]**<br>

<br>1. Start a loop: `for i in range(max_attempts)`.<br>

<br>2. **Try**: Execute function; if successful, return immediately.<br>

<br>3. **Except**: Catch specified exception types.<br>

<br>   - Log: `Retrying {func_name}... ({i+1}/{max})`.<br>

<br>   - `time.sleep(delay)`.<br>

<br>4. If the loop ends without success, raise the last captured exception.<br>

<br>*Scenario: Network request timeout, element temporarily not loaded.* |

### C. Error Handling

*Used for "Defensive Programming" on non-critical paths.*

| Decorator Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`@handle_exception`** | `default_return=None`, `screenshot=False` | **[Exception Swallowing]**<br>

<br>1. **Try**: Execute function.<br>

<br>2. **Except**: Catch all Exceptions.<br>

<br>   - Print Error log (include stack trace).<br>

<br>   - **Screenshot Logic**: If `screenshot=True`, check if the function's first argument `args[0]` contains a `driver` attribute (i.e., `self.driver`). If yes, call the screenshot method.<br>

<br>   - Return `default_return` (e.g., `None` or `False`).<br>

<br>*Scenario: Closing popup ads (if it fails, ignore and continue).* |

### D. Design Patterns

| Decorator Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`@singleton`** | `cls` | **[Singleton Pattern]**<br>

<br>1. Define a dictionary `_instances = {}`.<br>

<br>2. Inner function `get_instance`: Check if `cls` is in the dictionary.<br>

<br>3. If not, create and store it; if yes, return the existing instance.<br>

<br>*Scenario: Used for `DriverFactory` or `ConfigLoader` to ensure only one global instance exists.* |