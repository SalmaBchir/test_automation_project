from selenium.common import TimeoutException
from pages.base_page import BasePage
from utils.locators.reset_password_page_locators import ResetPasswordPageLocators
from selenium.webdriver.support import expected_conditions as EC
from utils.urls import Urls
from utils.users import ResetPasswordData


class ResetPasswordPage(BasePage):
    """Page object for the reset password page"""

    def open(self, reset_link: str):
        """Open the reset password page using the reset link received"""
        return self.open_url(reset_link)


    def is_reset_password_page_opened(self):
        """
        Verify if reset password page is opened
        Returns:
            bool: True if page is opened, False otherwise
        """
        try:
            self.wait.until(EC.url_contains(Urls.RESET_PASSWORD))
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            self.logger.info(f"Reset password page opened successfully")
            return True
        except TimeoutException:
            self.logger.info(f"Reset password page not opened. Current URL is = {self.get_current_url()}")
            return False

    def enter_password(self, password):
        """
        Enter password in the password field
        Args:
            password: Password to be entered
        """
        password_field = self.find_element(ResetPasswordPageLocators.PASSWORD_FIELD)
        self.input_text(password_field, password)

    def enter_password_confirmation(self, password_confirmation):
        """
        Enter password confirmation in the confirmation field
        Args:
            password_confirmation: Password confirmation to be entered
        """
        password_confirmation_field = self.find_element(ResetPasswordPageLocators.PASSWORD_CONFIRMATION_FIELD)
        self.input_text(password_confirmation_field, password_confirmation)

    def click_reset_button(self):
        """Click on the reset button"""
        reset_button = self.find_element(ResetPasswordPageLocators.RESET_BUTTON)
        self.click_element(reset_button)

    def reset_password(self, password, password_confirmation):
        """
        Complete password reset process
        Args:
            password: New password to set
            password_confirmation: Password confirmation
        """
        self.enter_password(password)
        self.enter_password_confirmation(password_confirmation)
        self.click_reset_button()

    def get_reset_error_message(self):
        """
        Get error message displayed on reset password failure
        Returns:
            str: Error message text
        """
        element = self.find_element(ResetPasswordPageLocators.ERROR_MESSAGE)
        return self.get_text(element)

    def is_reset_password_redirection_successful(self):
        """
        Verify if user is redirected to login page after successful password reset
        Returns:
            bool: True if redirection is successful, False otherwise
        """
        try:
            self.wait.until(EC.url_to_be(Urls.LOGIN))
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            self.logger.info("Successfully redirected to login page after password reset")
            return True
        except TimeoutException:
            self.logger.info(f"Redirection to login page failed. Current URL is = {self.get_current_url()}")
            return False

