## File: `workflows/base_workflow.py`

**Role**: Base Workflow Class
**Responsibility**: Dependency Injection (Driver), Page Object Management (Page Registry), App-level Operations (Lifecycle).

### A. Initialization & Page Registry

*Core Design Pattern: Use `@property` to implement **Lazy Loading**. This avoids instantiating all pages at the start of a test, saving memory and improving startup speed.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`__init__`** | `driver` | 1. Receive and store `self.driver`.<br>

<br>2. Initialize private variables (e.g., `self._home_page = None`) for subsequent lazy loading. |
| **`home_page`** (Property) | None | **[Property]** Check if `self._home_page` is None. If None, instantiate `HomePage(self.driver)` and assign it; otherwise, return the existing instance. |
| **`login_page`** (Property) | None | **[Property]** Same as above, instantiate `LoginPage`. |
| **`webview_page`** (Property) | None | **[Property]** Same as above, instantiate `WebviewPage` (for H5 operations). |
| **`...`** | None | **[Extension]** For every new Page added in the future, a corresponding Property must be registered here. |

### B. App Lifecycle Management

*These operations target the entire App, not specific pages, making the Workflow Base the most appropriate place for them.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`restart_app`** | None | **[Restart App]** Call `driver.terminate_app(app_id)` followed by `driver.activate_app(app_id)`. Used to ensure the next test case runs in a clean environment. |
| **`background_app`** | `seconds` | **[Background App]** Call `driver.background_app(seconds)`. Simulates user pressing the Home button to background the app and then returning (for testing hot starts or state saving). |
| **`close_app`** | None | **[Kill Process]** Call `driver.terminate_app(app_id)`. |
| **`launch_app`** | None | **[Cold Start]** Call `driver.activate_app(app_id)`. |

### C. Global Hardware Keys

*While `BasePage` has these capabilities, exposing them at the Workflow layer allows for smoother business flow scripting (avoiding calls like `self.home_page.press_back()`).*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`press_back`** | None | **[Physical Back]** Simulate clicking the phone's physical Back button. |
| **`press_home`** | None | **[Physical Home]** Simulate clicking the phone's Home button. |
| **`press_enter`** | None | **[Physical Enter]** Simulate clicking the keyboard's Enter key (Search/Send). |

### D. Flow Helpers

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`wait_seconds`** | `seconds`, `msg` | **[Forced Wait]** Wrap `time.sleep(seconds)`. **Must add logging** (e.g., `logger.info(f"Waiting {seconds} seconds: {msg}")`) to make forced waits traceable. |