# Tech Stack & Dependencies

**Project:** MobileAutomationFramework
**Language:** Python 3.10+

## 1. Core Automation Engine

| Component | Library/Tool | Version Constraint | Reasoning |
| --- | --- | --- | --- |
| **Driver** | `Appium-Python-Client` | **>= 3.1.0** | **CRITICAL**: Must support Appium 2.0+ and **W3C Standards**. Old `TouchAction` classes are deprecated; must use `ActionChains` / `W3C Actions`. |
| **Server** | Appium Server | 2.x | The target server environment. |
| **Protocol** | W3C WebDriver | N/A | Strict adherence to W3C protocol for gestures and element interaction. |

## 2. Test Execution & Reporting

| Component | Library/Tool | Version Constraint | Reasoning |
| --- | --- | --- | --- |
| **Runner** | `pytest` | >= 7.0.0 | Industry standard. Powerful fixture system and hook management (`conftest.py`). |
| **Reporting** | `allure-pytest` | >= 2.13.0 | Generates rich, interactive HTML reports with steps, logs, and screenshots. |
| **Parallelism** | `pytest-xdist` | (Optional) | For running tests in parallel (future scope). |

## 3. Utilities & Infrastructure

| Component | Library/Tool | Version Constraint | Reasoning |
| --- | --- | --- | --- |
| **Logging** | `loguru` | >= 0.7.0 | Modern logging. Simplifies configuration (rotation/retention) and supports structured logging better than `logging`. |
| **Config** | `PyYAML` | >= 6.0 | For reading `global_config` and `test_accounts`. |
| **Data** | `openpyxl` | >= 3.1.0 | For reading Excel (`.xlsx`) test data for parametrization. |
| **Env Vars** | `python-dotenv` | >= 1.0.0 | For loading secrets (passwords, tokens) from `.env` files. |
| **HTTP** | `requests` | >= 2.31.0 | For sending webhook notifications (Feishu/DingTalk). |
| **CV** | `opencv-python` | (Optional) | For image recognition (`cv_helper`). |
| **System** | `adbutils` or `subprocess` | N/A | For ADB interactions (Native `subprocess` preferred for zero-dependency). |

## 4. Development & Code Quality

| Component | Library/Tool | Reasoning |
| --- | --- | --- |
| **Formatting** | `black` | Uncompromising code formatter. |
| **Linting** | `pylint` | Static code analysis. |
| **Type Hints** | `mypy` | (Optional) For strict type checking. |

---

## 5. Architectural Decisions (ADR)

### ADR-001: Why Appium Python Client v3+?

* **Context**: Appium v2 server has removed support for the JSON Wire Protocol.
* **Decision**: Use Client v3+ which strictly enforces W3C.
* **Implication**: Code generation must NOT use `MobileBy` (deprecated) or `TouchAction`. Use `AppiumBy` and `ActionBuilder`.

### ADR-002: Why Loguru over standard Logging?

* **Context**: Standard `logging` requires verbose boilerplate for file rotation and formatting.
* **Decision**: Use `loguru`.
* **Implication**: All logs are centralized. Easy to add "sinks" (files, stdout) with one line.

### ADR-003: Why Pytest Fixtures over Unittest `setUp`?

* **Context**: `unittest` relies on class inheritance, which can be rigid.
* **Decision**: Use Pytest Fixtures (`conftest.py`).
* **Implication**: Dependency injection (Driver) is cleaner and more flexible (scope control).

---

## 6. Project Structure Rules

* **config/**: Only static configurations. No logic.
* **data/**: Only data files. No code.
* **pages/**: Only UI logic. No assertions.
* **testcases/**: Only assertions and data mapping. No `find_element`.
* **utils/**: Independent helpers. Should not import from `pages` or `workflows` to avoid circular imports.