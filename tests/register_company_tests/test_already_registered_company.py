import pytest
from pages.login_page import LoginPage
from pages.register_company_page import RegisterCompanyPage
from pages.register_page import RegisterPage
from pages.subscription_page import SubscriptionPage
from tests.base_test import BaseTest
from utils.error_messages.register_company_page_errors import RegisterCompanyPageErrors
from utils.urls import Urls



class TestAlreadyRegisteredCompany(BaseTest):

    @pytest.mark.parametrize("use_fixture_names, description", [
        (True, "the same name and siret as the original company"),
        (False, "different company name and siret")
    ])
    def test_already_registered_company(self, use_fixture_names, description, register_user_and_company_fixture):
        """Verify that an already registered company cannot register again."""

        user_data, company_data = register_user_and_company_fixture
        subscription_page = SubscriptionPage(self.driver)
        subscription_page.logout()
        assert subscription_page.is_logout_successful(), (
            "logout failed.\n"
            "As a result, duplicate company registration cannot be verified."
        )
        login_page = LoginPage(self.driver)
        login_page.click_create_account_link()
        assert login_page.is_register_page_opened(), (
            f"Redirection to the user registration page by clicking the 'Create account' link "
            f"failed.\n"
            f" expected URL is ='{Urls.CREATE_ACCOUNT}\n'"
            f" Current URL is ='{login_page.get_current_url()}'"
        )

        register_page = RegisterPage(self.driver)
        new_user_data= register_page.register_valid_user()
        assert register_page.is_registration_successful() ,(
            f"Registration failed for a new valid user.\n"
            " therefore, duplicate company registration cannot be checked."
        )

        name = company_data["name"] if use_fixture_names else "AnotherCompanyName"
        siret = company_data["siret"] if use_fixture_names else "12345678901234"
        email = company_data["email"]  # same email to trigger duplication

        register_company_page = RegisterCompanyPage(self.driver)
        register_company_page.register_company(name=name, email=email, siret=siret)

        assert not register_company_page.is_company_registration_successful(), (
            f"Duplicate company registration unexpectedly succeeded "
            f"when reusing the same company email with {description}."
        )

        error_message = register_company_page.get_register_company_error_message()
        expected_error = RegisterCompanyPageErrors.ALREADY_REGISTERED
        assert expected_error in error_message, (
            f"Validation error mismatch.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}'"
        )