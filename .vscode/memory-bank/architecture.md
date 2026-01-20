# Project Architecture & Design Constraints

**Project Name:** MobileAutomationFramework
**Description:** A scalable, 3-layer automated testing framework for Android/iOS/H5 based on Appium, Pytest, and Allure.

## 1. Architectural Pattern

This project strictly follows the **Page Object Model (POM)** pattern layered with **Workflows** to decouple UI interactions from business logic and test data.

### The 3-Layer Design

1. **UI Layer (`pages/`)**: "How to interact". Handles low-level UI elements (Locators, clicks, inputs).
2. **Business Layer (`workflows/`)**: "What to do". Orchestrates Pages to perform business processes (Login, Checkout).
3. **Test Layer (`testcases/`)**: "What to verify". Handles data injection and assertions.

---

## 2. Directory Structure & Responsibilities

AI must strictly adhere to the responsibilities defined below. **Do not leak logic across layers.**

### 🟢 Layer 1: Pages (`pages/`)

* **Responsibility**: Encapsulate pure UI interactions.
* **Source of Truth**: Refer to `pages/_specs.md` (or specific spec files provided by user).
* **Key Rules**:
* Must inherit from `BasePage`.
* Must mixin `ActionMixin` if gestures are needed.
* **NO assertions** allowed (except for checking element existence state).
* **NO business logic** (e.g., "if login fails, retry" belongs in Workflow, not Page).
* Return `self` or page objects to support method chaining (optional) or simply return data/status.



### 🟡 Layer 2: Workflows (`workflows/`)

* **Responsibility**: Manage Page Lifecycles and Business Logic.
* **Source of Truth**: Refer to `workflows/_specs.md`.
* **Key Rules**:
* Must inherit from `BaseWorkflow`.
* Use `Lazy Loading` for Page Objects (do not instantiate all pages at start).
* Manage App Lifecycle here (`restart_app`, `background_app`).
* **NO direct `driver.find_element` calls**. All UI operations must go through Pages.



### 🔴 Layer 3: TestCases (`testcases/`)

* **Responsibility**: Test execution and Verification.
* **Source of Truth**: Refer to `testcases/_specs.md`.
* **Key Rules**:
* Use `Pytest` fixtures for setup/teardown.
* Use `utils.data_loader` for data parametrization.
* Use `Allure` decorators (`@allure.step`) for reporting.
* **Perform all Assertions here**.



### 🔵 Utils & Core (`utils/`, `config/`, `drivers/`)

* **Responsibility**: Support system infrastructure.
* **Source of Truth**: Refer to `utils/_specs.md`.
* **Key Rules**:
* **BasePage**: The engine of the framework. Must handle strict explicit waits.
* **ActionMixin**: Implementation of W3C Actions.
* **Utils**: Pure functions. Stateless where possible.



---

## 3. Design Constraints

1. **Contract First (契约优先)**: Before implementing any code, read the specific Markdown Spec file provided by the user in the target folder. Do not invent function signatures if they are defined in the spec.
2. **No Raw Selenium**: Do not import `selenium.webdriver` directly in TestCases or Workflows. Use the methods provided by `BasePage` and `BaseWorkflow`.
3. **Cross-Platform**: Code should be structure to support Android and iOS (even if currently focusing on Android). Avoid hardcoding OS-specific logic outside of `drivers/` or specific OS-page folders.
4. **Stability**:
* Never use `time.sleep()` unless wrapped in a specific helper with a log reason.
* Always use Explicit Waits (`WebDriverWait`).


5. **Logging**: All critical actions must be logged using the `utils.logger` module, not `print()`.

---

## 4. Tech Stack

* **Language**: Python 3.8+
* **Driver**: Appium-Python-Client (W3C Standard)
* **Runner**: Pytest
* **Reporting**: Allure
* **Logging**: Loguru
* **Data**: PyYAML, OpenPyXL
* **Utils**: OpenCV (Optional), AdbShell

---

## 5. File Map (关键文件映射)

* `pages/base_page.py`: Core interaction logic (Click, Input, Wait).
* `pages/mixins/action_mixin.py`: W3C Gestures (Swipe, Pinch).
* `workflows/base_workflow.py`: Page registry & App lifecycle.
* `testcases/conftest.py`: Driver injection & Hook management.
* `utils/file_helper.py`: Path management (Root directory resolution).