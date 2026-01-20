## 1. File: `pages/base_page.py`

**Role**: Base Page Object Class
**Responsibility**: Handles single element interactions, state checks, and system environment operations. All Page classes must inherit from this class.

### A. Core Interactions

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`_find_element`** | `locator`, `timeout` | **[Internal Core]** Encapsulate `WebDriverWait` and `expected_conditions`. All subsequent methods **must** call this method to handle exceptions and logging uniformly. |
| **`click_element`** | `locator` | Wait for the element to be **Visible and Clickable**, then execute the click operation. |
| **`input_text_direct`** | `locator`, `text` | **[Direct Input]** Click element to focus -> Directly `send_keys` to append content (skip `clear` operation). |
| **`input_text_clear`** | `locator`, `text` | **[Standard Input]** Click element -> Execute `clear()` -> Input content -> **Detect and Hide Keyboard** to prevent UI obstruction. |
| **`get_text`** | `locator` | **[Smart Retrieval]** Prioritize reading the `text` attribute; if empty, fallback to reading the `content-desc` attribute. |
| **`get_element_attribute`** | `locator`, `attr_name` | Retrieve specific attribute values (e.g., `enabled`, `checked`, `resource-id`). |
| **`set_switch_status`** | `locator`, `status(bool)` | **[Smart Switch]** Get current `checked` status. If current status differs from target `status`, click; if consistent, skip. |

### B. State Checks

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`is_element_exist`** | `locator`, `timeout=3` | **[Boolean Check]** Set a short timeout. Catch `TimeoutException` without raising an error. Return `True` if exists, `False` otherwise. |
| **`wait_for_element_disappear`** | `locator`, `timeout` | **[Wait for Disappear]** Use `invisibility_of_element_located`. Commonly used to wait for Loading spinners/overlays to vanish. |
| **`get_toast_message`** | `partial_text` | **[Toast Capture]** Search using XPath `//*[@class='android.widget.Toast']`. Must locate rapidly (short timeout). |

### C. System & Context

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`switch_to_webview`** | `context_name` | **[H5 Switch]** Log current Contexts. If `context_name` is not specified, auto-switch to the first Context containing "WEBVIEW". |
| **`switch_to_native`** | None | Force switch back to the `NATIVE_APP` Context. |
| **`press_back`** | None | Simulate the physical **Back Button** (KEYCODE_BACK). |
| **`press_keycode`** | `keycode(int)` | Send specific Android KeyCode (e.g., 66=Enter, 67=Delete). |
| **`save_screenshot`** | `name_prefix` | Capture screenshot and save to `logs/screenshots/` directory. Filename must include a timestamp. |