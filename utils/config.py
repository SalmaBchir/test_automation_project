"""
Global Test Configuration
"""
import os

# Selenium Configuration
BROWSER = "chrome"
HEADLESS = False
IMPLICIT_WAIT = 10
EXPLICIT_WAIT= 10
PAGE_LOAD_TIMEOUT = 30
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directory Configuration
SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, "reports", "screenshots")
LOGS_DIR = os.path.join(PROJECT_ROOT, "reports", "test_steps_logs")
NETWORK_LOGS_DIR = os.path.join(PROJECT_ROOT, "reports", "network_logs")
REPORT_DIR = os.path.join(PROJECT_ROOT, "reports")

# System Under Test (SUT) Configuration
SUT = "RapidoCRM"
SUT_VERSION = "1"
TEST_ENVIRONMENT = "PROD"
REPORT_TITLE = f"Automated Test Report |{SUT} V{SUT_VERSION} | Environment: {TEST_ENVIRONMENT}"
