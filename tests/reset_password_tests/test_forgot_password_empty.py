import pytest
from pages.forgot_password_page import ForgotPasswordPage
from pages.login_page import LoginPage
from tests.base_test import BaseTest
from utils.urls import Urls
from utils.validation_messages.forgot_password_page_messages import ForgotPasswordPageMessages


class TestForgotPasswordEmptyEmail(BaseTest):

    @pytest.mark.parametrize("email", ['', '        '])
    def test_forgot_password_empty(self,email):
        """Verify that the system rejects password reset requests with empty or whitespace-only
            email fields."""
        login_page= LoginPage(self.driver)
        login_page.open()
        login_page.click_forgot_password_link()
        assert login_page.is_forgot_password_page_opened(), (
            f"Redirection to the forgot password page by clicking the 'forgot password' link "
            f"failed.\n"
            f" expected URL is ='{Urls.FORGOT_PASSWORD}\n'"
            f" Current URL is ='{login_page.get_current_url()}'"
        )
        forgot_password_page = ForgotPasswordPage(self.driver)
        forgot_password_page.request_password_reset(email)
        error_message = forgot_password_page.get_validation_message()
        expected_error = ForgotPasswordPageMessages.EMPTY_EMAIL
        assert expected_error in error_message, (
            f"Validation error mismatch for email = '{email}'.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}' (normally used for: "
            f"{ForgotPasswordPageMessages.get_message_type(error_message)})"
        )


