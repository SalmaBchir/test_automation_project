from pages.login_page import LoginPage
from pages.reset_password_page import ResetPasswordPage
from tests.base_test import BaseTest
from tests.reset_password_tests.reset_password_helper import ResetPasswordHelper
from utils.urls import Urls
from utils.users import ResetPasswordData
from utils.validation_messages.login_page_messages import LoginPageMessages


class TestResetPasswordValid(BaseTest):

    def test_reset_password_valid(self):
        """
           Tests the complete valid password reset flow, including user registration,
           password reset request, and login with the new password.
        """
        email = ResetPasswordData.generate_test_email()
        ResetPasswordHelper.register_then_request_and_open_password_reset_link(self.driver,email)
        new_password = ResetPasswordData.NEW_VALID_PASSWORD
        reset_password_page = ResetPasswordPage(self.driver)
        reset_password_page.reset_password(new_password, new_password)
        assert reset_password_page.is_reset_password_redirection_successful(),(
            f"Redirection to the login page failed.\n"
            f" expected URL is ='{Urls.LOGIN}\n'"
            f" Current URL is ='{reset_password_page.get_current_url()}'"
        )
        login_page = LoginPage(self.driver)
        actual_message = login_page.get_login_validation_message()
        expected_message = LoginPageMessages.RESET_PASSWORD_SUCCESS
        assert expected_message in actual_message, (
            f"Validation message mismatch.\n"
            f"Expected = '{expected_message}'\n"
            f"Actual = '{actual_message}' (normally used for: "
            f"{LoginPageMessages.get_message_type(actual_message)})"
        )

        # Verify login with new password
        login_page.login(email, new_password)
        assert login_page.is_login_before_company_successful(), (
            "Login with new password failed.\n"
            f"- Email used = '{email}'\n"
            f"- New Password used = '{new_password}'\n"
            f"Current URL is = '{login_page.get_current_url()}'"
        )



