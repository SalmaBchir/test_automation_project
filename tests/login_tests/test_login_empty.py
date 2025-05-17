import pytest
from pages.login_page import LoginPage
from pages.register_company_page import RegisterCompanyPage
from tests.base_test import BaseTest
from utils.error_messages.login_page_errors import LoginPageErrors
from utils.urls import Urls


class TestLoginEmptyFields(BaseTest):

    @pytest.mark.parametrize("password", ['', '        '])
    def test_login_empty_password(self, password,register_user_fixture):
       """Verify that login fails for empty/whitespace password."""
       register_company_page = RegisterCompanyPage(self.driver)
       register_company_page.click_login_link()
       assert register_company_page.is_login_page_opened(),(
           f"Redirection to the user registration page by clicking the 'login' link "
           f"failed.\n"
           f" expected URL is ='{Urls.LOGIN}\n'"
           f" Current URL is ='{register_company_page.get_current_url()}'"
        )

       login_page = LoginPage(self.driver)
       valid_email = register_user_fixture["email"]
       login_page.login(valid_email,password)
       assert  not login_page.is_login_successful(), (
            f"Unexpected login success with password = '{password}'\n"
            f"Valid email used = '{valid_email}'"
       )
       error_message = login_page.get_login_error_message()
       expected_error = LoginPageErrors.EMPTY_PASSWORD
       assert expected_error in error_message, (
            f"Validation error mismatch.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual= '{error_message}'"
       )

    @pytest.mark.parametrize("email", ['', '        '])

    def test_login_empty_email(self, email,register_user_fixture):
        """Verify that login fails for empty/whitespace email"""
        register_company_page = RegisterCompanyPage(self.driver)
        register_company_page.click_login_link()
        assert register_company_page.is_login_page_opened(), (
            f"Redirection to the user registration page by clicking the 'login' link "
            f"failed.\n"
            f" expected URL is ='{Urls.LOGIN}\n'"
            f" Current URL is ='{register_company_page.get_current_url()}'"
        )

        login_page = LoginPage(self.driver)
        valid_password = register_user_fixture["password"]
        login_page.login(email,valid_password)
        assert  not login_page.is_login_successful(), (
            f"Unexpected login success with email = '{email}'\n"
            f"Valid password used = '{valid_password}'"
        )
        error_message = login_page.get_login_error_message()
        expected_error = LoginPageErrors.EMPTY_EMAIL
        assert expected_error in error_message, (
            f"Validation error mismatch.\n"
            f"Expected= '{expected_error}'\n"
            f"Actual = '{error_message}'"
        )
