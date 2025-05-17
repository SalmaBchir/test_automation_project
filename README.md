# Automated Testing for Web Application
*• Built with Python, Selenium, Pytest*  
*• Page Object Model Architecture*  
*• Modular Data Separation*  
*• Reporting & Artifacts*  

---
## 📁 Project structure
Full directory hierarchy with key files

```text
test_automation_project/  
├── pages/                                # Page Object Model (POM) classes  
│   ├── base_page.py                      # Base class for all pages (inherited by others)  
│   ├── login_page.py                     # Login page interactions  
│   ├── register_page.py                  #  user registration page interactions 
│   └──  ...                              # Other pages (dashboard, subscription page, etc.)  
│
├── tests/                                # All test suites  
│   ├── base_test.py                      # Parent test class with setup/teardown logic  
│   ├── conftest.py                       # Pytest hooks, fixtures, global configurations 
│   │   
│   ├── login_tests/                      # Tests for login functionality  
│   │   ├── test_login_valid.py           # Specific test cases (e.g., valid subscriber user login, valid unsubscribed user login, etc.)  
│   │   ├── test_login_empty.py           
│   │   └──  ...                          # Other tests for login   
│   └── ...                               # Other test modules (directories: register_user_tests, etc.)  
│
├── utils/                                # Utilities and configurations  
│   ├── error_messages/                   # Error messages by page  
│   │   ├── __init__.py  
│   │   ├── login_page_errors.py  
│   │   ├── register_page_errors.py  
│   │   └──  ... 
│   │ 
│   ├── locators/                        # Element locators by page (IDs, XPaths)  
│   │   ├── __init__.py  
│   │   ├── login_page_locators.py  
│   │   ├── register_page_locators.py  
│   │   └── ... 
│   │ 
│   ├── ui_texts/                       # Button texts and labels by page  
│   │   ├── __init__.py  
│   │   ├── login_page_ui.py  
│   │   ├── register_page_ui.py 
│   │   └──  ... 
│   │  
│   ├── __init__.py  
│   ├── config.py                      # Global settings (browser, timeouts, paths)  
│   ├── urls.py                        # All application URLs (e.g., login URL)  
│   └── users.py                       # Test user data (valid/invalid credentials)  
│
├── reports/                                                         # Test reports and artifacts  
│   ├── screenshots/                                                 # Screenshots on test failure  
│   │   ├── test_login_valid_subscribed_user_2025_05_16_T12_26.png  
│   │   └──...
│   │ 
│   ├── network_logs/                                                # HTTP request/response logs (.json) on failure  
│   │   ├── test_login_valid_subscribed_user_2025_05_16_T12_26.json  
│   │   └──...
│   │ 
│   ├── test_steps_logs/                                             # Step-by-step test execution logs on failure  
│   │   ├── test_login_valid_subscribed_user_2025_05_16_T12_26.log 
│   │   └──...
│   │ 
│   ├── report_2025_05_16_T12_26.html                                # HTML report summarizing test results  
│   └──...
│  
├── requirements.txt                    # Project dependencies  
└── README.md                           # Project documentation  

```
---
## ⚙️ Setup & Execution

### 1. Prerequisites
- Install **Python 3.10+**
- Install **Google Chrome** (latest stable version recommended)
- Install **dependencies**
- 
```bash
   pip install -r requirements.txt
```

### 2. Running Tests

#### ❗ Note

You can run commands either from the **project root directory** (`test_automation_project/`) or from the `tests/` directory,  
as long as the `conftest.py` file is in scope so Pytest can auto-detect fixtures and configurations.

#### ✅ Command examples from the project root

| Command                                                                              | Description                                                        |
|--------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| `pytest tests/login_tests/test_login_valid.py`                                       | Run all tests in a specific file                                   |
| `pytest tests/login_tests/test_login_valid.py -k "test_login_valid_subscribed_user"` | Run a single test by name                                          |
| `pytest tests/login_tests/`                                                          | Run all tests in a directory (module)                              |
| `pytest tests/ -n 4`                                                                 | Run all tests in parallel with 4 workers (requires `pytest-xdist`) |

#### Why Use pytest-xdist?

Faster Execution: Distributes tests across multiple CPU cores.

Command: Add -n auto (auto-detects cores) or -n 2 (2 workers).

---
## 🔧 Key Features

### 1. Page Object Model (POM)

- Isolates UI elements and their interactions from test scripts for better maintainability.
- Centralizes common element actions (e.g., `click`, `input_text`) in reusable page classes.

### 2. Centralized Wait Management

The BasePage class (defined in base_page.py) standardizes Selenium wait mechanisms to ensure robust and stable test execution. It imports timeout configurations directly from `utils.config`:

- **Implicit Waits**: Automatically waits up to IMPLICIT_WAIT seconds (e.g., 10s) for elements to exist in the DOM. 
- **Explicit  Waits**:  Uses WebDriverWait with EXPLICIT_WAIT (e.g., 10s) to wait dynamically for specific conditions like element visibility or clickability, allowing more precise control over dynamic page behavior.
- **Page Load Timeout**:  Applies set_page_load_timeout(PAGE_LOAD_TIMEOUT) to fail test execution if a page takes too long to load (e.g., 30s), avoiding indefinite hangs on slow pages.

- This setup minimizes flakiness by handling delays, dynamic content, and slow page loads systematically.

### 3. Data Separation

- **Locators**: UI element identifiers (XPath/CSS) stored in `utils/locators/` (e.g., `login_page_locators.py`).
- **UI Texts**: Button texts and labels stored in `utils/ui_texts/` (e.g., `login_page_ui.py`).
- **Error Messages**: Page-specific error messages stored in `utils/error_messages/` (e.g., `login_page_errors.py`).
- **Test Data**: Valid and invalid user data stored in `utils/users.py`.
- **Configuration**: Global settings like browser type and timeouts in `utils/config.py`.
- **URLs**: All app URLs centralized in `utils/urls.py`.

- **Advantages**
  - **Safe Change Propagation** : Update locators or test data in a single file — changes automatically reflect across all tests.
  - **Improved Readability**: Tests remain focused on business logic instead of low-level UI details.
  - **Collaboration-Friendly**: QA engineers write tests, while developers can maintain or update locators separately.

### 3. Test Parametrization

- Execute the same test case with **multiple input combinations**.
- This example demonstrates how to use `@pytest.mark.parametrize` to test the same logic against a variety of invalid email inputs.

```python
@pytest.mark.parametrize("email", InvalidUserData.generate_invalid_email())
def test_register_invalid_email(self, email):
    # Attempts registration with each invalid email
    ...
```
**Benefits**:  One test method = dozens of variations executed automatically.

📄 Full test code available in:
📄 [test_register_invalid.py](tests/register_user_tests/test_register_invalid.py)


---
## 📊 Reports & Artifacts

### 1. Automatic Report Generation

- **Trigger**: Generated automatically after every test run.
- **Location**: `reports/report_<TIMESTAMP>.html`

- **Contents**:
  - Test module (name of the folder containing the test file)
  - Pass/fail status for each individual test
  - Test description (pulled from the test function's docstring)
  - Failure messages (if any)
  - Artifact links (only for failed tests)

- **Summary metrics**:
  - ✅ Pass Rate
  - ❌ Fail Rate


### 2. Artifact Links (for Failed Tests)

All artifact file names start with the **test name**, which corresponds to the **test function name** (e.g., `test_login_invalid_email`).


- **Screenshots**: Captured automatically on failure : `reports/screenshots/test_name_<TIMESTAMP>.png`

- **Network Logs**: Captured HTTP request/response details : `reports/network_logs/test_name_<TIMESTAMP>.json`

- **Execution Logs**: Step-by-step logs including failure traces : `reports/test_steps_logs/test_name_<TIMESTAMP>.log`

**Parameterized Test Naming Explanation**  

- When a test is parameterized (run with multiple datasets), its artifact files include a suffix with a short hash of the parameters:  
`<test_function_name>_p<short_hash>` (e.g., `test_login_p3f8a`).  

- The `p` indicates a parameterized test.  

- The short hash is an MD5 digest of the parameter values truncated to 4 characters.  
- This ensures artifact names are unique per parameter set and prevents conflicts between runs of the same test function with different inputs.

---
## 🧩 Fixtures
Reusable setup and teardown logic to support test execution.


### `setup_webdriver ( in conftest)`

**Purpose**: Initializes and tears down the WebDriver instance for browser automation.

- **What it does**:
  - Launches a Chrome browser (headless mode configurable via HEADLESS in config.py).
  - Configures Chrome options for performance logging, network capture, and stability.
  - Automatically manages ChromeDriver installation using webdriver_manager.
  
- **Scope**: Function-level_Automatically applied to all tests (autouse=True).

### `setup_memory_logging (in conftest)`

**Purpose**: Captures test execution logs in memory for diagnostics and reporting.

- **What it does**:
  - Attaches an in-memory logging handler to the root logger before each test.
  - Stores all log entries during test execution (e.g., errors, debug messages).
  - Automatically clears logs between tests to avoid contamination.
  - Integrates with the reporting system to save logs to disk for failed tests.
  
- **Scope**: Function-level_Automatically applied to all tests (autouse=True).

### `setup (in base_test)`

**Purpose**: Prepares a clean environment for tests inheriting from BaseTest.

- **What it does**:
  - Initializes the WebDriver via setup_webdriver and configures a class-specific logger.
  - deletes cookies before each test.
  - Logs test start/end events and ensures graceful browser shutdown after execution.
  - Integrates with the reporting system to save logs to disk for failed tests.
  
- **Scope**: Function-level. Automatically applied to all tests in BaseTest subclasses (autouse=True).

### `register_user_fixture (in base_test)`

**Purpose**: Provides a pre-registered user for authentication-dependent tests.

- **What it does**:
  - Navigates to the registration page and creates a user with valid credentials.
  - Returns user data (email, password) for use in downstream steps.
  
- **Scope**: Function-level. Must be explicitly requested by tests.

### `register_user_and_company_fixture (in base_test)`

**Purpose**: Simulates a full user + company onboarding flow.

- **What it does**:
  - Combines register_user_fixture to create a user.
  - Returns both user and company data for end-to-end workflow testing.
- **Scope**: Function-level. Must be explicitly requested by tests.

### Full Sequence for a Test Using `register_user_fixture`

Here's the precise order of setup and teardown calls, including conditional actions:

```python
# SETUP PHASE 
setup_memory_logging (start)  
→ setup_webdriver (initialize browser)  
→ setup (BaseTest: reset cookies, log test start)  
→ register_user_fixture (create user)  
→ Test Execution

# TEARDOWN PHASE 
register_user_fixture (no teardown logic)  
→ setup (BaseTest: log test end → quit browser via `driver.quit()`)  
→ setup_webdriver (no teardown logic)  
→ setup_memory_logging (detach logger → save logs to disk **only if test failed**)
```
---
## 👉 Start Testing!

Configure settings in utils/config.py (e.g., HEADLESS = True for no UI).

Run pytest tests/ to execute all tests.

Check reports/ for results and artifacts.