from pages.base_page import BasePage
from utils.locators.forgot_password_page_locators import ForgotPasswordPageLocators
from utils.urls import Urls


class ForgotPasswordPage(BasePage):
    """Page object for the forgot password page"""

    def open(self):
        """Open the forgot password page using the predefined URL"""
        self.open_url(Urls.FORGOT_PASSWORD)

    def enter_email(self, email):
        """Enter email in the email field
        Args:
            email: Email to be entered
        """
        email_field = self.find_element(ForgotPasswordPageLocators.EMAIL_FIELD)
        self.input_text(email_field, email)

    def click_send_button(self):
        """Click on the send button"""
        login_button = self.find_element(ForgotPasswordPageLocators.SEND_BUTTON)
        self.click_element(login_button)

    def request_password_reset(self,email):
        """Request a password reset by entering the email and submitting the form.

           Args:
               email: The user's email address
           """
        self.enter_email(email)
        self.click_send_button()

    def get_validation_message(self):
        element = self.find_element(ForgotPasswordPageLocators.VALIDATION_MESSAGE)
        return self.get_text(element)

