import pytest
from pages.register_page import RegisterPage
from tests.base_test import BaseTest
from utils.error_messages.register_page_errors import RegisterPageErrors
from utils.users import ValidUserData


class TestRegisterEmptyFields(BaseTest):
    @pytest.mark.parametrize("lastname", ['','         '])
    def test_register_empty_lastname(self, lastname):
        """Verify that user registration fails for an empty or whitespace-only last name"""
        register_page = RegisterPage(self.driver)
        register_page.open()
        valid_email = ValidUserData.generate_valid_email()
        register_page.register(lastname, ValidUserData.VALID_FIRSTNAME,valid_email,ValidUserData.VALID_PASSWORD,ValidUserData.VALID_PASSWORD)
        assert not register_page.is_registration_successful(), (
            f"Unexpected user registration success with last name = '{lastname}'\n"
            f"Valid email used = '{valid_email}'"
        )
        error_message = register_page.get_register_error_message()
        expected_error = RegisterPageErrors.EMPTY_LASTNAME
        assert expected_error in error_message, (
            f"Validation error mismatch.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}'"
        )

    @pytest.mark.parametrize("firstname", ['', '        '])
    def test_register_empty_firstname(self, firstname):
        """Verify that user registration fails for an empty or whitespace-only first name"""
        register_page = RegisterPage(self.driver)
        register_page.open()
        valid_email = ValidUserData.generate_valid_email()
        register_page.register(ValidUserData.VALID_LASTNAME, firstname, valid_email, ValidUserData.VALID_PASSWORD, ValidUserData.VALID_PASSWORD)
        assert not register_page.is_registration_successful(), (
            f"Unexpected user registration success with first name = '{firstname}'\n"
            f"Valid email used = '{valid_email}'"
        )
        error_message = register_page.get_register_error_message()
        expected_error = RegisterPageErrors.EMPTY_FIRSTNAME
        assert expected_error in error_message, (
            f"Validation error mismatch.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}'"
        )

    @pytest.mark.parametrize("email", ['','        '])
    def test_register_empty_email(self, email):
        """Verify that user registration fails for an empty or whitespace-only email"""
        register_page = RegisterPage(self.driver)
        register_page.open()
        register_page.register(ValidUserData.VALID_LASTNAME, ValidUserData.VALID_FIRSTNAME, email,
                            ValidUserData.VALID_PASSWORD, ValidUserData.VALID_PASSWORD)
        assert not register_page.is_registration_successful(), (
            f"Unexpected user registration success with email = '{email}'"
        )
        error_message = register_page.get_register_error_message()
        expected_error = RegisterPageErrors.EMPTY_EMAIL
        assert expected_error in error_message, (
            f"Validation error mismatch.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}'"
        )

    @pytest.mark.parametrize("password",['','        '])
    def test_register_empty_password(self, password):
        """Verify that user registration fails for an empty or whitespace-only password"""
        register_page = RegisterPage(self.driver)
        register_page.open()
        valid_email = ValidUserData.generate_valid_email()
        register_page.register(ValidUserData.VALID_LASTNAME, ValidUserData.VALID_FIRSTNAME, valid_email, password,
                            password)
        assert not register_page.is_registration_successful(), (
            f"Unexpected user registration success with password = '{password}'\n"
            f"Valid email used = '{valid_email}'"
        )
        error_message = register_page.get_register_error_message()
        expected_error = RegisterPageErrors.EMPTY_PASSWORD
        assert expected_error in error_message, (
            f"Validation error mismatch.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}'"
        )

    def test_register_empty_confirm_password(self):
        """Verify that registration fails if the password confirmation field is empty"""
        register_page = RegisterPage(self.driver)
        register_page.open()
        valid_email = ValidUserData.generate_valid_email()
        valid_password = ValidUserData.VALID_PASSWORD
        register_page.register(ValidUserData.VALID_LASTNAME, ValidUserData.VALID_FIRSTNAME, valid_email,
                            valid_password, "")
        assert not register_page.is_registration_successful(),(
            f"Unexpected user registration success with empty password confirmation\n"
            f"Valid email used = '{valid_email}'\n"
            f"Valid password used = '{valid_password}'"
        )
        error_message = register_page.get_register_error_message()
        expected_error = RegisterPageErrors.INVALID_PASSWORD_CONFIRMATION
        assert expected_error in error_message, (
            f"Validation error mismatch.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}'"
        )