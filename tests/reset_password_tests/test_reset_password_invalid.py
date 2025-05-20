from pages.reset_password_page import ResetPasswordPage
from tests.base_test import BaseTest
from utils.users import ValidUserData, InvalidUserData, ResetPasswordData
from utils.validation_messages.reset_password_page_messages import ResetPasswordPageMessages
from tests.reset_password_tests.reset_password_helper import ResetPasswordHelper


class TestResetPasswordInvalidFields(BaseTest):

    def test_reset_password_invalid_password(self):
        """
        Verify that the system rejects password reset attempts when the new password is too short (less
        than 8 characters).
        """
        email = ResetPasswordData.generate_test_email()
        ResetPasswordHelper.register_then_request_and_open_password_reset_link(self.driver, email)

        reset_password_page = ResetPasswordPage(self.driver)
        reset_password_page.reset_password(
            InvalidUserData.INVALID_PASSWORD,
            InvalidUserData.INVALID_PASSWORD  # Same invalid password for confirmation
        )
        assert not reset_password_page.is_reset_password_redirection_successful(), (
            f"Unexpected reset password redirection success with an invalid password( less than 8 characters)\n"
            f"Valid email used = '{email}'\n"
            f"Password used = '{InvalidUserData.INVALID_PASSWORD}'"
        )
        error_message = reset_password_page.get_reset_error_message()
        expected_error = ResetPasswordPageMessages.INVALID_PASSWORD
        assert expected_error in error_message, (
            f"Validation error mismatch for invalid new password scenario.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}' (normally used for: "
            f"{ResetPasswordPageMessages.get_message_type(error_message)})"
        )

    def test_reset_password_confirmation_mismatch(self):
        """
        Verify that the system rejects password reset attempts when the password confirmation
        does not match the new password.
        """
        email = ResetPasswordData.generate_test_email()
        ResetPasswordHelper.register_then_request_and_open_password_reset_link(self.driver, email)

        valid_password = ValidUserData.VALID_PASSWORD
        invalid_confirmation = valid_password[:-1] + "X"  # Alter last character

        reset_password_page = ResetPasswordPage(self.driver)
        reset_password_page.reset_password(valid_password, invalid_confirmation)

        assert not reset_password_page.is_reset_password_redirection_successful(), (
            f"Unexpected success in reset password redirection with mismatched password confirmation.\n"
            f"Valid email used = '{email}'\n"
            f"Password used = '{valid_password}'\n"
            f"Password confirmation used = '{invalid_confirmation}'"
        )
        error_message = reset_password_page.get_reset_error_message()
        expected_error = ResetPasswordPageMessages.INVALID_PASSWORD_CONFIRMATION
        assert expected_error in error_message, (
            f"Validation error mismatch.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}' (normally used for: "
            f"{ResetPasswordPageMessages.get_message_type(error_message)})"
        )