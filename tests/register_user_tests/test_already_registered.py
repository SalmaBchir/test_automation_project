import pytest
from pages.register_page import RegisterPage
from tests.base_test import BaseTest
from utils.error_messages.register_page_errors import RegisterPageErrors

class TestAlreadyRegistered(BaseTest):

    @pytest.mark.parametrize("use_fixture_names, description", [
        (True, "the same firstname and lastname as initial user"),
        (False, "different firstname and lastname")
    ])
    def test_already_registered(self, use_fixture_names, description, register_user_fixture):
        """Verify that an already registered user cannot register again."""
        register_page = RegisterPage(self.driver)
        register_page.navigate_back()

        firstname =register_user_fixture["firstname"] if use_fixture_names else "AnotherFirstName"
        lastname = register_user_fixture["lastname"] if use_fixture_names else "AnotherLastName"


        register_page.register(
            lastname=lastname,
            firstname=firstname,
            email=register_user_fixture["email"],
            password=register_user_fixture["password"],
            password_confirmation=register_user_fixture["password_confirmation"]
        )

        assert not register_page.is_registration_successful(), (
            f"Duplicate user registration unexpectedly succeeded "
            f"when reusing the same email with {description}."
        )

        error_message = register_page.get_register_error_message()
        expected_error = RegisterPageErrors.ALREADY_REGISTERED
        assert expected_error in error_message, (
            f"Validation error mismatch.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}'"
        )