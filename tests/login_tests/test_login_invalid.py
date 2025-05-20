from pages.login_page import LoginPage
from pages.register_company_page import RegisterCompanyPage
from tests.base_test import BaseTest
from utils.validation_messages.login_page_messages import LoginPageMessages
from utils.urls import Urls


class TestLoginInvalidFields(BaseTest):

    def test_login_invalid_email(self, register_user_fixture):
        """Verify that login fails when using an invalid email format."""
        register_company_page = RegisterCompanyPage(self.driver)
        register_company_page.click_login_link()
        assert register_company_page.is_login_page_opened(), (
            f"Redirection to the login page by clicking the 'login' link failed.\n"
            f"Expected URL: '{Urls.LOGIN}'\n"
            f"Actual URL: '{register_company_page.get_current_url()}'"
        )

        login_page = LoginPage(self.driver)
        valid_password = register_user_fixture["password"]
        invalid_email = register_user_fixture["email"][:-3]  # simulate invalid email
        login_page.login(invalid_email, valid_password)

        assert not login_page.is_login_successful(), (
            f"Unexpected login success with invalid email = '{invalid_email}'\n"
            f"Valid password used = '{valid_password}'"
        )

        expected_error = LoginPageMessages.INVALID_EMAIL
        error_message = login_page.get_login_validation_message()
        assert expected_error in error_message, (
            f"Error message validation failed for email ='{invalid_email}'\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}' (normally used for: "
            f"{LoginPageMessages.get_message_type(error_message)})"
        )

    def test_login_invalid_password(self, register_user_fixture):
        """Verify that login fails when using an invalid password (less than 8 characters)."""
        register_company_page = RegisterCompanyPage(self.driver)
        register_company_page.click_login_link()
        assert register_company_page.is_login_page_opened(), (
            f"Redirection to the login page by clicking the 'login' link failed.\n"
            f"Expected URL: '{Urls.LOGIN}'\n"
            f"Actual URL: '{register_company_page.get_current_url()}'"
        )

        login_page = LoginPage(self.driver)
        valid_email = register_user_fixture["email"]
        invalid_password = register_user_fixture["password"][:-1]  # simulate invalid password
        login_page.login(valid_email, invalid_password)

        assert not login_page.is_login_successful(), (
            f"Unexpected login success with invalid password = '{invalid_password}'\n"
            f"Valid email used = '{valid_email}'"
        )

        expected_error = LoginPageMessages.WRONG_CREDENTIALS
        error_message = login_page.get_login_validation_message()

        assert expected_error in error_message, (
            f"Error message validation failed for password = '{invalid_password}'.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}' (normally used for: "
            f"{LoginPageMessages.get_message_type(error_message)})"
        )
