## File: `testcases/conftest.py`

**Role**: Test Configuration & Hook Manager
**Responsibility**: Manages CLI options, Driver Lifecycle (Setup/Teardown), Failure Hooks (Screenshots), and Allure Environment configuration.

### A. CLI Options & Configuration

*Responsible for enabling parameterized runs for your test scripts.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`pytest_addoption`** | `parser` | **[Pytest Hook]** Register custom command-line arguments.<br>

<br>1. `--env`: Specify target environment (test/prod), default to 'test'.<br>

<br>2. `--platform`: Specify platform (android/ios), default to 'android'.<br>

<br>3. `--browser`: (Optional) Whether to launch in Webview mode. |
| **`cmdopt`** | `request` | **[Fixture]** A simple fixture to parse values from the arguments above and return them as a dictionary to other fixtures (e.g., `{'env': 'test', 'platform': 'android'}`). |

### B. Driver Lifecycle Management

*This is the most critical Fixture in the entire automation suite.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`driver`** | `request`, `cmdopt` | **[Core Fixture]** `scope='function'` (recommended for isolation) or `'class'`.<br>

<br>**Setup Phase:**<br>

<br>1. Retrieve configuration from `cmdopt`.<br>

<br>2. Call `drivers.driver_factory.DriverFactory.get_driver(...)` to initialize the Driver.<br>

<br>3. **Critical Step**: Execute `request.cls.driver = driver`. This injects the driver into the Test Class, ensuring `self.driver` is populated in TestLogin.<br>

<br>4. `yield driver` (Test execution begins).<br>

<br>

<br>**Teardown Phase:**<br>

<br>1. Execute `driver.quit()` to close the app.<br>

<br>2. Log "Driver closed". |

### C. Failure Hooks & Screenshots

*Responsible for "leaving evidence" when things go wrong.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`pytest_runtest_makereport`** | `item`, `call` | **[Pytest Hook]** Intercept test execution results.<br>

<br>1. Check if `call.excinfo` exists (i.e., if an exception was raised).<br>

<br>2. If `report.when == 'call'` and `report.failed == True` (Test Failed):<br>

<br>3. Retrieve driver instance from `item` (usually via `item.instance.driver` or `item.funcargs['driver']`).<br>

<br>4. Call the `_capture_screenshot` helper function.<br>

<br>5. Attach the screenshot to the Allure report. |
| **`_capture_screenshot`** | `driver`, `name` | **[Internal Helper]** <br>

<br>1. Call `driver.get_screenshot_as_png()`.<br>

<br>2. Use `allure.attach()` to embed the binary image data into the report, named `failure_timestamp`.<br>

<br>3. (Optional) Simultaneously save a copy to the local `logs/screenshots/` directory. |

### D. Environment Info Collection (Allure)

*Makes the report look professional by displaying the device and environment details.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`pytest_configure`** | `config` | **[Pytest Hook]**<br>

<br>1. Before the run starts, read `global_config`.<br>

<br>2. Write Allure Environment Info (e.g., App Version, Base URL, Platform).<br>

<br>This ensures environment parameters appear on the Allure report homepage. |