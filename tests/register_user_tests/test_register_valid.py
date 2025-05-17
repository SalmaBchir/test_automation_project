from pages.register_page import RegisterPage
from tests.base_test import BaseTest

class TestRegisterValid(BaseTest):
    def test_register_valid(self):
        """Verify that a new valid user can successfully register."""
        register_page = RegisterPage(self.driver)
        register_page.open()
        user_data = register_page.register_valid_user()

        assert register_page.is_registration_successful(), (
            f"Registration failed for a new valid user.\n"
            f"Last name used = '{user_data['lastname']}'\n"
            f"First name used = '{user_data['firstname']}'\n"
            f"Email used = '{user_data['email']}'\n"
            f"Password used = '{user_data['password']}'\n"
            f"Password confirmation used = '{user_data['password_confirmation']}'\n"
            f"Current URL is = '{register_page.get_current_url()}'\n"
        )