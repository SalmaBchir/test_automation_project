import pytest
from pages.register_page import RegisterPage
from tests.base_test import BaseTest
from utils.validation_messages.register_page_messages import RegisterPageMessages
from utils.users import (ValidUserData, InvalidUserData)

class TestRegisterInvalidFields(BaseTest):

    @pytest.mark.parametrize("email", InvalidUserData.generate_invalid_email())
    def test_register_invalid_email(self, email):
        """Verify that user registration fails when using an invalid email format."""
        register_page = RegisterPage(self.driver)
        register_page.open()
        valid_password = ValidUserData.VALID_PASSWORD
        register_page.register(
            ValidUserData.VALID_LASTNAME,
            ValidUserData.VALID_FIRSTNAME,
            email,
           valid_password,
           valid_password
        )
        assert not register_page.is_registration_successful(), (
            f"Unexpected user registration success with invalid email = '{email}'\n"
            f"Valid password used = '{valid_password}'"
        )

        error_message = register_page.get_register_error_message()
        expected_error = RegisterPageMessages.INVALID_EMAIL
        assert expected_error in error_message, (
            f"Error message validation failed.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}' (normally used for: "
            f"{RegisterPageMessages.get_message_type(error_message)})"
        )

    def test_register_invalid_password(self):
        """Verify that user registration fails when using an invalid password (less than 8 characters)."""
        register_page = RegisterPage(self.driver)
        register_page.open()
        invalid_password = InvalidUserData.INVALID_PASSWORD
        valid_email= ValidUserData.generate_valid_email()
        register_page.register(
            ValidUserData.VALID_LASTNAME,
            ValidUserData.VALID_FIRSTNAME,
            valid_email,
            invalid_password,
            invalid_password
        )
        assert not register_page.is_registration_successful(), (
            f"Unexpected user registration success with an invalid password = '{invalid_password}'\n"
            f"Valid email used = '{valid_email}'"
        )
        error_message = register_page.get_register_error_message()
        expected_error = RegisterPageMessages.INVALID_PASSWORD
        assert expected_error in error_message, (
            f"Validation error mismatch for password = '{invalid_password}.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}' (normally used for: "
            f"{RegisterPageMessages.get_message_type(error_message)})"
        )

    def test_register_invalid_confirm_password(self):
        """Verify that user registration fails when password and confirmation do not match"""
        register_page = RegisterPage(self.driver)
        register_page.open()
        valid_password = ValidUserData.VALID_PASSWORD
        invalid_confirmation = valid_password[:-1] + "X"
        valid_email = ValidUserData.generate_valid_email()
        register_page.register(
            ValidUserData.VALID_LASTNAME,
            ValidUserData.VALID_FIRSTNAME,
            valid_email,
            valid_password,
            invalid_confirmation
        )
        assert not register_page.is_registration_successful(), (
            f"Unexpected user registration success with mismatched password confirmation.\n"
            f"Valid email used = '{valid_email}'\n"
            f"Valid password used = '{valid_password}'\n"
            f"Confirmation used = '{invalid_confirmation}'"
        )
        error_message = register_page.get_register_error_message()
        expected_error = RegisterPageMessages.INVALID_PASSWORD_CONFIRMATION
        assert expected_error in error_message, (
            f"Validation error mismatch.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}' (normally used for: "
            f"{RegisterPageMessages.get_message_type(error_message)})"

        )