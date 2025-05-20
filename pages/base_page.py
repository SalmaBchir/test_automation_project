import logging
import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from utils.config import (EXPLICIT_WAIT, PAGE_LOAD_TIMEOUT, IMPLICIT_WAIT)
from selenium.webdriver.support.ui import Select
from utils.config import  SCREENSHOT_DIR
class BasePage:
    """
    Base class for all page objects.
    Provides common methods for page interactions and element handling.
    """

    def __init__(self, driver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)
        self.driver.implicitly_wait(IMPLICIT_WAIT)
        self.driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        self.wait = WebDriverWait(self.driver, EXPLICIT_WAIT)
        self.is_subscription_required = True

    def set_subscription_required(self, value: bool):
        """
        Define if the subscription selection is required
        """
        self.is_subscription_required = value
        self.logger.info(f"Subscription required set to = '{self.is_subscription_required}'")

    def get_title(self):
        return self.driver.title.strip()

    def get_current_url(self):
        return self.driver.current_url.strip()

    def open_url(self, url):
        """
        Navigate to specified URL and ensure page is fully loaded.
        """
        try:
            self.driver.get(url)
            self.wait.until(EC.url_to_be(url))
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            self.logger.info(
                f"Page loaded successfully = '{url}' "
                f" having title = '{self.get_title()}'"
            )
        except TimeoutException as e:
            self.logger.error(
                f"Timeout while loading page '{url}' "
                f"after '{PAGE_LOAD_TIMEOUT}' seconds | {str(e)}"
                f"Current URL is = '{self.get_current_url()}'"
            )
            raise e
        except Exception as e:
            self.logger.error(
                f"Navigation to '{url}' failed | {str(e)}"
                f"Current URL is = '{self.get_current_url()}'")
            raise e

    def navigate_back(self):
        """
        Navigate to the previous page in browser history and ensure it's fully loaded.
        """
        try:
            self.driver.back()
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            self.logger.info(f"Successfully navigated back to = '{self.get_current_url()}'")
        except TimeoutException as e:
            self.logger.error(
                f"Timeout while trying to navigate back | {str(e)}"
                f"Current URL is = '{self.get_current_url()}'"
            )
            raise e
        except Exception as e:
            self.logger.error(
                f"Navigation back failed | {str(e)}"
                f"Current URL is = '{self.get_current_url()}'"
            )
            raise e

    def navigate_forward(self):
        """
        Navigate to the next page in browser history and ensure it's fully loaded.
        """
        try:
            self.driver.forward()
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            self.logger.info(f"Successfully navigated forward to = '{self.get_current_url()}'")
        except TimeoutException as e:
            self.logger.error(
                f"Timeout while trying to navigate forward | {str(e)}"
                f"Current URL is = '{self.get_current_url()}'"
            )
            raise e
        except Exception as e:
            self.logger.error(
                f"Navigation forward failed | {str(e)}"
                f"Current URL is = '{self.get_current_url()}'"
            )
            raise e

    def is_element_present(self, locator) -> bool:
        """
        Check if the element specified by the locator is visible on the page.
        Returns True if found, False otherwise without raising exceptions.
        """
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except (TimeoutException, NoSuchElementException):
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error while checking element presence at '{self.get_current_url()}'| {str(e)}")
            return False

    def find_element(self, locator) :
        """Find a single web element using provided locator.
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            return element
        except NoSuchElementException as e:
            self.logger.error(f"Unable to find any element using locator = {locator} at '{self.get_current_url()}'| {str(e)}")
            raise e
        except TimeoutException as e:
            self.logger.error(f"timeout while waiting for element with locator = {locator} to become visible at '{self.get_current_url()}' | {str(e)}")
            raise e
        except Exception as e:
            self.logger.error(
                f"An unexpected error occurred while searching for element with locator = {locator} at '{self.get_current_url()}'| {str(e)}")
            raise e

    def find_elements(self, locator):
        """Find multiple web elements using provided locator.
        Args:
            locator: Tuple
        Returns:
            list[WebElement]: List of found elements
        """
        try:
            elements = self.wait.until(EC.visibility_of_all_elements_located(locator))
            return elements
        except NoSuchElementException as e:
            self.logger.error(
                f"Unable to find  elements using locator = {locator}  at '{self.get_current_url()}' |  {str(e)}")
            raise e
        except TimeoutException as e:
            self.logger.error(
                f"Timeout while waiting for elements with locator = {locator} to become visible at '{self.get_current_url()}' | Exception: {str(e)}")
            raise e
        except Exception as e:
            self.logger.error(
                f"An unexpected error occurred while searching for elements with locator = {locator} on page ='{self.get_current_url()}' | Exception: {str(e)}")
            raise e

    def get_element_name(self, element):

        element = self.wait.until(EC.visibility_of(element))
        return (
                element.text or
                element.get_attribute("aria-label") or
                element.get_attribute("value") or
                element.get_attribute("title") or
                element.get_attribute("name") or
                element.get_attribute("id") or
                element.get_attribute("placeholder") or
                element.get_attribute("class") or
                ""
        )

    def click_element(self, element):
        """Wait until element is clickable and click it.
        Args:
            element: WebElement to be clicked
        """

        element_name = self.get_element_name(element)

        try:
            ActionChains(self.driver).move_to_element(element).perform()
            element = self.wait.until(EC.element_to_be_clickable(element))
            element.click()
            self.logger.info(f"Successfully clicked on element identified as '{element_name}'")

        except Exception as e:
            self.logger.error(
                f"Failed to click on element identified as '{element_name}' at '{self.get_current_url()}' | {str(e)}"
            )
            raise e

    def double_click_element(self, element):
        """Wait until element is clickable and double-click it.
        Args:
            element: WebElement to be double-clicked
        """
        element_name = self.get_element_name(element)

        try:
            ActionChains(self.driver).move_to_element(element).perform()
            element = self.wait.until(EC.element_to_be_clickable(element))
            ActionChains(self.driver).double_click(element).perform()
            self.logger.info(f"Successfully Double-clicked on element identified as '{element_name}'")

        except Exception as e:
            self.logger.error(
                f"Failed to double-click on element identified as'{element_name}' at '{self.get_current_url()}'| {str(e)}"
            )
            raise e


    def select_option_by_text_and_get_index(self, dropdown_element, text):
        """Select option in dropdown menu by visible text and get the option's index.
        Args:
            dropdown_element: Select WebElement ( type <select>)
            text: Visible text of option to select
        Returns:
            int: Index of the selected option
        """
        dropdown_name = self.get_element_name(dropdown_element)

        try:
            dropdown_element = self.wait.until(EC.element_to_be_clickable(dropdown_element))

            select = Select(dropdown_element)
            options = select.options

            for index, option in enumerate(options):
                option_text = option.text.strip()
                if option_text == text.strip():
                    select.select_by_visible_text(option_text)
                    self.logger.info(
                        f"Option with text '{text}' selected in dropdown menu ('{dropdown_name}'), "
                        f"its index is = {index}")
                    return index

            raise ValueError(
                f"Option with text '{text}' not found in dropdown menu (identified as '{dropdown_name}'). "
                f"Available options are: {[opt.text.strip() for opt in options]}")
        except Exception as e:
            self.logger.error(f"Failed to select option by text '{text}' in dropdown ('{dropdown_name}'): {e}")
            raise

    def check(self, element):
        """Wait until element is clickable and check it (select for radio buttons or checkboxes).
        Args:
            element: WebElement to be checked (checkbox or radio button)
        """

        element_name = self.get_element_name(element)

        try:
            element = self.wait.until(EC.element_to_be_clickable(element))

            # If the element is not selected, click to select it
            if not element.is_selected():
                element.click()
                self.logger.info(f"Successfully checked the element identified as '{element_name}'")
            else:
                self.logger.info(f"Element identified as '{element_name}' is already checked")

        except Exception as e:
            self.logger.error(
                f"Failed to check element identified as '{element_name}' at '{self.get_current_url()}' | {str(e)}"
            )
            raise e

    def input_text(self, element, text):
        """Enter text into an input field.
        Args:
            element: WebElement representing the input field
            text: String to enter into the field
        """
        element_name = self.get_element_name(element)
        try:
            element = self.wait.until(EC.element_to_be_clickable(element))
            element.click()
            element.clear()
            element.send_keys(text)
            if text == "":
                self.logger.info(f"Field '{element_name}' left empty")
            elif text.strip() == "":
                self.logger.info(f"Field '{element_name}' contains only whitespace")
            else:
                self.logger.info(f"Entered ='{text}' into field  '{element_name}'")

        except Exception as e:
            self.logger.error(f"Failed to enter = '{text}' into field  '{element_name}'| {str(e)}")
            raise e

    def get_text(self, element):
        """
        Get text content from a WebElement.
        Args:
            element: WebElement to extract text from
        Returns:
            str: Text content of element
        """
        element_name = self.get_element_name(element)
        try:
            text = element.text
            if not text:
                text = element.get_attribute("value") or ""
            self.logger.info(f"Retrieved text from element identified as '{element_name}' is = '{text}'")
            return text.strip()
        except Exception as e:
            self.logger.error(f"Failed to get text from element identified as '{element_name}' at '{self.get_current_url()}'| {str(e)}")
            return ""


    def switch_to_new_window(self):
        """Switch to the most recently opened window."""
        try:
            # Store the current window handle
            current_window = self.driver.current_window_handle
            # Get all window handles
            all_windows = self.driver.window_handles
            if len(all_windows) < 2:
                self.logger.error("No new window available")
                return

            new_window = all_windows[-1]
            if new_window != current_window:
                self.driver.switch_to.window(new_window)
                self.logger.info(
                    f"Switched to new window."
                    f"New window URL = '{self.get_current_url()}'"
                    f"New window Title = '{self.get_title()}'"
                )

        except Exception as e:
            self.logger.error(f"Failed to switch to new window | {str(e)}")
            raise e

    def switch_back_to_main_window(self):
        """Switch back to the main (initial) browser window."""
        try:
            all_windows = self.driver.window_handles
            if not all_windows:
                self.logger.error("No windows found to switch to.")
                return

            main_window = all_windows[0]
            self.driver.switch_to.window(main_window)
            self.logger.info(
                f"Switched back to main window. "
                f"URL = '{self.get_current_url()}', "
                f"Title = '{self.get_title()}'"
            )

        except Exception as e:
            self.logger.error(f"Failed to switch back to main window | {str(e)}")
            raise e

    def take_screenshot(self, name: str):
        """
        Manually capture a screenshot and save it under reports/screenshots/.
        """
        try:
            timestamp = time.strftime("%Y_%m_%d_T%H_%M")
            screenshot_filename = f"{name}_{timestamp}.png"
            screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_filename)

            os.makedirs(SCREENSHOT_DIR, exist_ok=True)
            self.driver.save_screenshot(screenshot_path)
            self.logger.info(f"Screenshot successfully captured at = {screenshot_path}")
            return screenshot_path

        except Exception as e:
            self.logger.info(f"Failed to capture screenshot '{name}' | {str(e)}")
            return None