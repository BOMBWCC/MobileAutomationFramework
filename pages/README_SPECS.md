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


## 2. File: `pages/mixins/action_mixin.py`

**Role**: Action Capability Extension Class (Mixin)
**Responsibility**: Handles screen gestures, multi-touch interactions, and composite lookups.
**Technical Requirements**: **Must use Appium W3C Actions API** (`ActionChains`, `PointerInput`). Usage of the legacy `TouchAction` class is **strictly prohibited**.

### A. Directional Swipe

*Note: Swipes in this category are calculated based on screen percentage coordinates.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`swipe_up`** | `duration=1000` | **[Swipe Up/Load More]** Slide from 80% screen height to 20% (X-axis stays centered). |
| **`swipe_down`** | `duration=1000` | **[Swipe Down/Refresh]** Slide from 20% screen height to 80% (X-axis stays centered). |
| **`swipe_left`** | `duration=1000` | **[Swipe Left]** Slide from 90% screen width to 10% (Y-axis stays centered). |
| **`swipe_right`** | `duration=1000` | **[Swipe Right/Back]** Slide from 10% screen width to 90% (Y-axis stays centered). |

### B. Precision Actions

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`swipe_by_coordinates`** | `start_x`, `start_y`, `end_x`, `end_y`, `duration` | **[Arbitrary Swipe]** Use `W3C ActionBuilder` to execute: Pointer Move -> Down -> Pause -> Move -> Up. |
| **`tap_by_coordinates`** | `x`, `y` | **[Blind Tap]** Click on specific pixel coordinates (Pointer Down -> Pause(0.1s) -> Up). |

### C. Advanced Gestures

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`long_press_element`** | `locator`, `duration=2000` | **[Long Press]** Locate element -> Move to element center -> Press down -> **Pause for specified duration** -> Release. |
| **`zoom_in`** | `percent` | **[Pinch to Zoom In]** Define two `PointerInput` sources (Finger1, Finger2). Move both fingers outwards from the screen center simultaneously (Spread). |
| **`zoom_out`** | `percent` | **[Pinch to Zoom Out]** Define two `PointerInput` sources. Move both fingers from outer edges towards the center simultaneously (Pinch). |

### D. Composite Actions

*Note: These methods contain logic loops but MUST NOT contain assertions.*

| Method Name | Arguments | Logic Description (Vibe Coding Prompt) |
| --- | --- | --- |
| **`swipe_until_element_appear`** | `locator`, `max_swipes`, `direction` | **[Swipe to Find Element]** <br>

<br>1. Loop `max_swipes` times.<br>

<br>2. In each loop, call `is_element_exist(timeout=1)`.<br>

<br>3. If exists, return the Element immediately.<br>

<br>4. If not, execute one swipe based on `direction` and wait for inertia to stop. |
| **`swipe_until_text_appear`** | `text`, `max_swipes`, `direction` | **[Swipe to Find Text]** <br>

<br>1. Internally construct XPath: `//*[contains(@text, 'text') or contains(@content-desc, 'text')]`.<br>

<br>2. Call `swipe_until_element_appear`. |