from pages.login_page import LoginPage
from pages.register_company_page import RegisterCompanyPage
from tests.base_test import BaseTest
from utils.error_messages.login_page_errors import LoginPageErrors
from utils.urls import Urls


class TestLoginInvalidFields(BaseTest):

    def test_login_invalid_email(self, register_user_fixture):
        """Verify that login fails with invalid email."""
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

        expected_error = LoginPageErrors.INVALID_EMAIL
        error_message = login_page.get_login_error_message()
        assert expected_error in error_message, (
            f"Error message validation failed.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}'\n"
            f"The system should flag the email ='{invalid_email}' as invalid."
        )

    def test_login_invalid_password(self, register_user_fixture):
        """Verify that login fails with invalid password."""
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

        expected_error = LoginPageErrors.WRONG_CREDENTIALS
        error_message = login_page.get_login_error_message()

        assert expected_error in error_message, (
            f"Error message validation failed.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}'\n"

        )
