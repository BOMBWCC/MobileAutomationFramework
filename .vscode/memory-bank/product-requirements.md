# Product Requirements Document (PRD)

**Project:** MobileAutomationFramework
**Version:** 1.0.0
**Status:** Implementation Phase

## 1. Executive Summary

Develop an enterprise-grade, data-driven mobile automation framework based on **Appium (Python)**. The framework must support Android and iOS (scalable), focusing on stability, ease of maintenance, and comprehensive reporting. It adopts a strict **3-Layer Architecture** (Pages, Workflows, TestCases) to decouple UI details from business logic.

## 2. Core Objectives

1. **Stability**: Eliminate "flaky tests" caused by network lag or rendering delays using robust explicit waits and retry mechanisms.
2. **Maintainability**: Centralize UI locators in Page Objects. One UI change should require updating only one file.
3. **Observability**: Provide detailed step logs, automatic screenshots on failure, and Allure reports.
4. **Hybrid Support**: Seamlessly handle context switching between Native App and WebViews (H5).

## 3. Functional Requirements

### 3.1 Core Interaction Layer (`pages/base_page.py`)

The system must provide a robust base class for all Page Objects.

* **Element Location**:
* Must wrap `WebDriverWait` and `expected_conditions`.
* Must support a global timeout (default 10s).


* **Interactions**:
* `click_element`: Wait for element to be visible AND clickable.
* `input_text_clear`: Standard mode (Click -> Clear -> Input -> Hide Keyboard).
* `input_text_direct`: Append mode (Direct input without clearing).
* `get_text`: Smart retrieval (Priority: `text` attribute > `content-desc` attribute).
* `get_element_attribute`: Retrieve specific attributes (enabled, checked, bounds).


* **State Management**:
* `set_switch_status`: Smart toggle. Only click if current status != target status.
* `is_element_exist`: Return Boolean (True/False) without throwing exceptions.
* `wait_for_element_disappear`: Support waiting for Loading spinners to vanish.


* **System**:
* `get_toast_message`: Capture system toast notifications.
* `switch_to_webview` / `switch_to_native`: Context management.
* `press_back` / `press_keycode`: Physical key simulation.
* `save_screenshot`: Save PNG to local directory.



### 3.2 Advanced Gestures Layer (`pages/mixins/action_mixin.py`)

The system must support complex touch interactions using **Appium W3C Actions** (No TouchAction).

* **Directional Swipes**: Up, Down, Left, Right (Screen-percentage based).
* **Precision Actions**:
* `swipe_by_coordinates`: A point to B point.
* `tap_by_coordinates`: Click on specific (x, y).


* **Multi-Touch**:
* `zoom_in` / `zoom_out`: Pinch gestures.
* `long_press_element`: Long press for N seconds.


* **Composite Actions**:
* `swipe_until_element_appear`: Scroll iteratively until an element is found or max swipes reached.



### 3.3 Business Flow Layer (`workflows/base_workflow.py`)

The system must provide a manager for business processes.

* **Page Registry**: Implement **Lazy Loading** for Page Objects (Initialize only when accessed).
* **App Lifecycle**:
* `restart_app`: Terminate and Activate app to ensure clean state.
* `background_app`: Simulate Home button backgrounding.


* **Global Actions**: Shortcut access to physical keys (Back, Home).

### 3.4 Infrastructure & Utilities (`utils/`)

The system must provide a robust toolkit.

* **ADB Wrapper (`adb_helper.py`)**:
* IME Switching (Appium Keyboard vs. System Keyboard).
* App Data Clearing (`pm clear`).
* Device Info (IP, connected devices).


* **Assertions (`assert_helper.py`)**:
* Soft Assertions (Collect errors, fail at end).
* Complex Data Verification (List sorting, Dict subset).


* **Computer Vision (`cv_helper.py`)** *(Optional Module)*:
* Find image coordinates via Template Matching.
* Image Comparison (SSIM).


* **Data Engine (`data_loader.py`)**:
* Support YAML and Excel (.xlsx) file parsing.


* **Reporting & Notifications**:
* Detailed Logging (Loguru).
* Webhook Notifications (Feishu/DingTalk) with pass/fail summaries.


* **Decorators**:
* `@log_step`: Automatic logging of function entry/exit.
* `@retry`: Automatic retry on failure.
* `@handle_exception`: Safe execution without crashing.



### 3.5 Test Execution Layer (`testcases/`)

* **Config**: Support CLI arguments for Environment (`--env`) and Platform (`--platform`).
* **Fixtures**:
* `driver`: Function-level fixture for Driver Setup/Teardown.
* `check_failure`: Hook to capture screenshots on test failure.



## 4. Non-Functional Requirements

1. **Code Style**: Adhere to PEP 8 standards.
2. **Dependencies**: Minimized external libraries (see `requirements.txt`).
3. **Cross-Platform**: Designed for Android first, but structure must allow iOS extension (e.g., separate locators folder).
4. **Error Handling**: No silent failures in critical paths. All exceptions must be logged with tracebacks.
5. **Performance**:
* Screenshot operations must be optimized (do not block main thread for too long).
* Wait times must be configurable via `global_config`.



## 5. Constraints

* **No Raw Selenium in Workflows**: `find_element` must strictly reside in `pages/`.
* **No Hardcoded Paths**: All file paths must be resolved dynamically relative to Project Root.
* **W3C Compliance**: All touch actions must use W3C standard (ActionBuilder), as TouchAction is deprecated in Appium 2.0.
