"""
This module configures the pytest testing environment for Selenium-based automated tests.
"""
import os
import json
import pytest
import logging
import hashlib
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.config import (
    BROWSER,
    HEADLESS,
    SCREENSHOT_DIR,
    LOGS_DIR,
    NETWORK_LOGS_DIR,
    REPORT_DIR,
    REPORT_TITLE
)

# ------------------------------------------------
# Constants and Global Configuration
# ------------------------------------------------
TIMESTAMP = datetime.now().strftime("%Y_%m_%d_T%H_%M")
REPORT_FILENAME = f"report_{TIMESTAMP}.html"
REPORT_PATH = os.path.join(REPORT_DIR, REPORT_FILENAME)
TEST_RESULTS = {"passed": 0, "failed": 0, "total": 0}
USING_XDIST = False
logger = logging.getLogger(__name__)

# ------------------------------------------------
# Custom Logging Handler Class
# ------------------------------------------------

class MemoryLogHandler(logging.Handler):
    """
    Stores test execution logs in memory.
    """

    def __init__(self):
        super().__init__()
        self.log_records = []
        self.formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    def emit(self, record):
        self.log_records.append(self.formatter.format(record))

    def get_logs(self):
        return self.log_records

    def clear(self):
        self.log_records = []

# ------------------------------------------------
# Directory Setup and Configuration
# ------------------------------------------------
def pytest_configure(config):
    """
    Configures the test environment before execution,
    including output directories and report paths.
    """

    # Detection of parallel execution with pytest-xdist
    # Checks if the xdist plugin is installed AND enabled (-n)
    global USING_XDIST
    if config.pluginmanager.hasplugin("xdist"):
        numprocesses = getattr(config.option, "numprocesses", 0) or 0
        USING_XDIST = numprocesses > 0
    else:
        USING_XDIST = False

    # Output directories creation
    for directory in [REPORT_DIR, SCREENSHOT_DIR, LOGS_DIR, NETWORK_LOGS_DIR]:
        os.makedirs(directory, exist_ok=True)

    config.option.htmlpath = REPORT_PATH
    logger.info(f"Report will be generated at: {REPORT_PATH}")

    # Log configuration

    config.option.log_cli = False
    config.option.log_file_level = "INFO"
    config.option.log_format = "%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)"
    config.option.log_date_format = "%Y-%m-%d %H:%M:%S"
    config.option.log_auto_indent = True


    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)


# ------------------------------------------------
# WebDriver Setup
# ------------------------------------------------
@pytest.fixture
def setup_webdriver():
    """
    Initializes a browser instance with configured options,
    including network traffic logging capabilities.
    """
    if BROWSER.lower() == "chrome":
        options = webdriver.ChromeOptions()
        if HEADLESS:
            options.add_argument("--headless")

        options.set_capability('goog:loggingPrefs', {
            'browser': 'ALL',
            'performance': 'ALL'
        })

        # Add common Chrome options
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-background-networking")
        options.add_argument("--enable-logging")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--no-sandbox")
        options.add_argument("--v=1")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--disable-accelerated-2d-canvas")

        # Create Chrome driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    else:
        raise ValueError(f"Unsupported browser: {BROWSER}")


    yield driver

# ------------------------------------------------
# Test Logging Functions - Using Memory Handler
# ------------------------------------------------
@pytest.fixture(autouse=True)
def setup_memory_logging():
    """
    Attach memory logging handler for test.
    """
    memory_handler = MemoryLogHandler()
    memory_handler.setLevel(logging.INFO)


    root_logger = logging.getLogger()
    root_logger.addHandler(memory_handler)


    pytest.memory_log_handler = memory_handler

    yield


    root_logger.removeHandler(memory_handler)

# ------------------------------------------------
# Helper functions for artifact management
# ------------------------------------------------
def _get_test_name(item):
    """
    Extract test name from a pytest item.
    """
    nodeid = item.nodeid
    nodeid_last_part = nodeid.split("::")[-1]
    is_parameterized = '[' in nodeid_last_part

    func_name = nodeid_last_part.split('[')[0]

    if is_parameterized:
        param_part = nodeid_last_part.split('[', 1)[1].rstrip(']')
        param_hash = hashlib.md5(param_part.encode('utf-8')).hexdigest()
        short_hash = param_hash[-4:]
        test_name = f"{func_name}_p{short_hash}"
    else:
        test_name = func_name

    return test_name

def _get_artifact_path(base_dir, test_name, extension):
    """
    Generates standardized paths for test artifacts.
    """
    filename = f"{test_name}_{TIMESTAMP}.{extension}"
    file_path = os.path.join(base_dir, filename)


    rel_path = os.path.relpath(file_path, os.path.dirname(REPORT_PATH))

    return file_path, rel_path

def _save_memory_logs(log_path):
    """
     Saves in-memory test execution logs to disk.
     """
    try:
        if hasattr(pytest, 'memory_log_handler'):
            log_records = pytest.memory_log_handler.get_logs()
            with open(log_path, 'w', encoding='utf-8') as f:
                for record in log_records:
                    f.write(f"{record}\n")
            logger.info(f"Test logs saved: {log_path}")
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to save test logs: {e}")
        return False

def _capture_screenshot(item, screenshot_path):
    """Capture screenshot for failed test."""
    try:
        item.instance.driver.save_screenshot(screenshot_path)
        logger.info(f"Screenshot saved: {screenshot_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to capture screenshot: {e}")
        return False

def capture_network_logs(driver, output_path):
    """Capture and enrich network requests and responses."""
    logs = driver.get_log('performance')
    network_data = {}
    enriched_logs = []
    for entry in logs:
        try:
            log_data = json.loads(entry['message'])
            message = log_data.get('message', {})
            method = message.get('method', '')
            params = message.get('params', {})
            if method == 'Network.requestWillBeSent':
                request_id = params.get('requestId')
                request = params.get('request', {})
                network_data[request_id] = {
                    "url": request.get('url'),
                    "method": request.get('method'),
                    "type": "request",
                    "request_headers": request.get('headers'),
                    "postData": request.get('postData', ''),
                    "timestamp": params.get('timestamp')
                }
            elif method == 'Network.responseReceived':
                request_id = params.get('requestId')
                response = params.get('response', {})
                if request_id in network_data:
                    network_data[request_id]["type"] = "response"
                    network_data[request_id]["status"] = response.get('status')
                    network_data[request_id]["response_headers"] = response.get('headers')
                    network_data[request_id]["mimeType"] = response.get('mimeType')


        except json.JSONDecodeError:
            continue
        # Format as a list
    for entry in network_data.values():
        enriched_logs.append(entry)

        # Write to a JSON file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(enriched_logs, f, indent=2, ensure_ascii=False)

def _capture_network_logs(item, network_log_path):
    """
    Capture network logs for failed test.
    """
    try:
        capture_network_logs(item.instance.driver, network_log_path)
        logger.info(f"Network logs saved: {network_log_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to capture network logs: {e}")
        return False

def capture_test_artifacts(item, report):
    """
       Collects diagnostic data for failed tests
    """
    if not (hasattr(item, 'instance') and hasattr(item.instance, 'driver')):
        logger.warning(f"Test instance or driver not found for {item.nodeid}")
        return


    test_name = _get_test_name(item)

    links_html = "<div class='links-col'>"

    # Test Steps (Log)
    log_path, log_rel_path = _get_artifact_path(
        LOGS_DIR, test_name, "log"
    )
    log_captured = _save_memory_logs(log_path)
    if log_captured:
        links_html += f'<a href="{log_rel_path}" target="_blank">Test steps</a><br>'

    # Screenshot
    screenshot_path, screenshot_rel_path = _get_artifact_path(
        SCREENSHOT_DIR, test_name, "png"
    )
    screenshot_captured = _capture_screenshot(item, screenshot_path)
    if screenshot_captured:
        links_html += f'<a href="{screenshot_rel_path}" target="_blank">Screenshot</a><br>'

    # Network Logs
    network_path, network_rel_path = _get_artifact_path(
        NETWORK_LOGS_DIR, test_name, "json"
    )
    network_captured = _capture_network_logs(item, network_path)
    if network_captured:
        links_html += f'<a href="{network_rel_path}" target="_blank">Network Logs</a><br>'

    links_html += "</div>"
    report.sections.append(("Test Artifacts", links_html))


def _extract_failure_message(report):
    """Extract the main error message to display in the report.

Extraction priorities:
1. ERROR messages from the in-memory log handler
2. Selenium exceptions (Message: ...)
3. AssertionError with context
4. Other generic errors (truncated)

Returns:
    str: Formatted error message for display in the report.
"""
    error_messages = []

    # Collect ERROR logs from in-memory logging
    if hasattr(pytest, 'memory_log_handler'):
        for log in pytest.memory_log_handler.get_logs():
            if 'ERROR' in log:
                clean_msg = log.split(' - ')[-1].strip()
                error_messages.append(clean_msg)

    if error_messages:
        return "\n".join(error_messages)

    if hasattr(report, 'longrepr'):
        failure_msg = str(report.longrepr)

        # Handle Selenium exceptions - extract core message
        if 'Message: ' in failure_msg:
            message_part = failure_msg.split('Message: ', 1)[1]
            message_part = message_part.split('\n', 1)[0]
            return f"{message_part.strip()}"

        # Format AssertionErrors for clarity
        elif 'AssertionError:' in failure_msg:
            parts = failure_msg.split('AssertionError:', 1)
            if len(parts) > 1:
                error_part = parts[1].split('E       assert', 1)[0]
                return f"AssertionError: {error_part.strip()}"

        # Handle basic assert statements
        elif 'assert' in failure_msg:
            parts = failure_msg.split('assert', 1)
            return f"assert {parts[1].strip()}"

        else:
            return failure_msg.strip()

    return ""

# ------------------------------------------------
# Test Reporting Functions
# ------------------------------------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Generate test report and track results.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        item.report = report

    # Description from the docstring
    report.description = item.function.__doc__ or "No description"

    if report.when == "call":
        TEST_RESULTS["total"] += 1
        if report.passed:
            TEST_RESULTS["passed"] += 1
        elif report.failed:
            TEST_RESULTS["failed"] += 1

    # Process results for failed/error tests
    if report.outcome in ['failed', 'error']:
        failure_message = _extract_failure_message(report)
        report.failure_message = failure_message
        logger.error(f"Test {report.outcome}: {failure_message}")
        capture_test_artifacts(item, report)



# ------------------------------------------------
# HTML Report Customization
# ------------------------------------------------
def pytest_html_results_table_header(cells):
    """
    Customizes HTML report table headers to include:
    - Module location
    - Test description from docstring
    - Clean failure message
    - Separate column for artifacts
    """
    cells.insert(1, "<th>Module</th>")
    cells.insert(3, "<th>Description</th>")
    cells.insert(4, "<th>Failure message</th>")
    cells.pop()  # Remove the last cell (Links)
    cells.append("<th>Artifacts</th>")

def pytest_html_results_table_row(report, cells):
    """
    Populates HTML report table rows with:
    - Parent module information
    - Simplified test name
    - Test description from docstring
    - Clean failure message
    - Links to  artifacts
    """
    # Add the module (parent directory)
    test_path = report.nodeid.split('::')[0]
    parent_directory = os.path.basename(os.path.dirname(test_path))
    cells.insert(1, f"<td>{parent_directory}</td>")

    # Simplify the test name display (keep only the test method name)
    if len(cells) > 2 and '::' in report.nodeid:
        test_parts = report.nodeid.split('::')
        if len(test_parts) >= 3:
            # Extract just the test method name from nodeid
            test_name = test_parts[2]
            cells[2] = f"<td>{test_name}</td>"

    # Add description
    cells.insert(3, f"<td>{getattr(report, 'description', '')}</td>")

    # Add the failure message
    failure_message = ""

    if report.outcome in ['failed', 'error']:
        if hasattr(report, 'failure_message'):
            failure_message = report.failure_message
        elif hasattr(report, 'longrepr'):
            failure_message = str(report.longrepr)

    elif report.skipped:
        if hasattr(report, 'longreprtext'):
            skip_message = report.longreprtext.split('Skipped: ', 1)[-1]
            failure_message = skip_message

    if failure_message:
        failure_message = failure_message.replace(' ', '&nbsp;').replace('\n', '<br>')

    cells.insert(4, f"<td>{failure_message}</td>")

    # Replace the last cell (Links) with custom links
    cells.pop()

    # Find section links if available
    artifacts_html = ""
    for name, content in getattr(report, 'sections', []):
        if name == "Test Artifacts":
            artifacts_html = content
            break

    cells.append(f"<td class='links-col'>{artifacts_html}</td>")

def pytest_html_results_summary(prefix):
    """
    Adds custom summary statistics and styling to HTML report
    """
    prefix.append(f"<h3>{REPORT_TITLE}</h3>")

    # Do not display stats in parallel mode (xdist)
    if USING_XDIST :
        return

    passed = TEST_RESULTS["passed"]
    failed = TEST_RESULTS["failed"]
    total = TEST_RESULTS["total"]

    pass_percent = (passed / total * 100) if total > 0 else 0.0
    fail_percent = (failed / total * 100) if total > 0 else 0.0

    prefix.extend([
            f"<h3>Pass Rate: {pass_percent:.2f}%</h3>",
            f"<h3>Fail Rate: {fail_percent:.2f}%</h3>",
        ])

    prefix.extend([
        "<style>",
        "/* Balance the table cell size */",
        "table#results-table { table-layout: fixed; width: 100%; }",
        "table#results-table th, table#results-table td { word-wrap: break-word; overflow-wrap: break-word; }",
        "table#results-table th:nth-child(1), table#results-table td:nth-child(1) { width: 4%; }",
        "table#results-table th:nth-child(2), table#results-table td:nth-child(2) { width: 8%; }",
        "table#results-table th:nth-child(3), table#results-table td:nth-child(3) { width: 23%; }",
        "table#results-table th:nth-child(4), table#results-table td:nth-child(4) { width: 25%; }",
        "table#results-table th:nth-child(5), table#results-table td:nth-child(5) { width: 30%; }",
        "table#results-table th:nth-child(6), table#results-table td:nth-child(6) { width: 4%; }",
        "table#results-table th:nth-child(7), table#results-table td:nth-child(7) { width: 6%; }",
        "</style>"
    ])