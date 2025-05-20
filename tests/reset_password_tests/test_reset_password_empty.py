import pytest
from pages.reset_password_page import ResetPasswordPage
from tests.base_test import BaseTest
from utils.users import ValidUserData, ResetPasswordData
from utils.validation_messages.reset_password_page_messages import ResetPasswordPageMessages
from tests.reset_password_tests.reset_password_helper import ResetPasswordHelper


class TestResetPasswordEmptyFields(BaseTest):

    @pytest.mark.parametrize("password", ['', '        '])
    def test_reset_password_empty_password(self, password):
        """
        Verify that the system rejects password reset attempts when the new password field
        is empty or contains only whitespace.
        """
        email = ResetPasswordData.generate_test_email()
        ResetPasswordHelper.register_then_request_and_open_password_reset_link(self.driver, email)

        reset_password_page = ResetPasswordPage(self.driver)
        reset_password_page.reset_password(password, ValidUserData.VALID_PASSWORD)

        assert not reset_password_page.is_reset_password_redirection_successful(), (
            "Unexpected success in reset password redirection with an empty new password.\n"
            f"Valid email used = '{email}'\n"
        )

        error_message = reset_password_page.get_reset_error_message()
        expected_error = ResetPasswordPageMessages.EMPTY_PASSWORD
        assert expected_error in error_message, (
            f"Validation error mismatch for empty new password scenario.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}' (normally used for: "
            f"{ResetPasswordPageMessages.get_message_type(error_message)})"
        )

    @pytest.mark.parametrize("confirmation", ['', '        '])
    def test_reset_password_empty_confirmation(self, confirmation):
        """
        Verify that the system rejects password reset attempts when the new password confirmation field
        is empty or contains only whitespace.
        """
        email = ResetPasswordData.generate_test_email()
        ResetPasswordHelper.register_then_request_and_open_password_reset_link(self.driver, email)

        reset_password_page = ResetPasswordPage(self.driver)
        reset_password_page.reset_password(ValidUserData.VALID_PASSWORD, confirmation)

        assert not reset_password_page.is_reset_password_redirection_successful(), (
        f"Unexpected reset password redirection success with empty password confirmation\n"
        f"Valid email used = '{email}'\n"
        f"Password used = '{ValidUserData.VALID_PASSWORD}'"
        )

        error_message = reset_password_page.get_reset_error_message()
        expected_error = ResetPasswordPageMessages.EMPTY_PASSWORD_CONFIRMATION
        assert expected_error in error_message, (
            f"Validation error mismatch.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}' (normally used for: "
            f"{ResetPasswordPageMessages.get_message_type(error_message)})"
        )