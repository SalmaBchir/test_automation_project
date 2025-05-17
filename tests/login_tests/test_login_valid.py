from pages.login_page import LoginPage
from pages.register_company_page import RegisterCompanyPage
from pages.subscription_page import SubscriptionPage
from tests.base_test import BaseTest
from utils.urls import Urls


class TestLoginValid(BaseTest):

    def test_login_valid_before_company(self, register_user_fixture):
        """
        Verify that a registered user without a company can log in
        and is redirected to the company registration page.
        """
        register_company_page = RegisterCompanyPage(self.driver)
        register_company_page.click_login_link()

        assert register_company_page.is_login_page_opened(), (
            "Redirection to the login page by clicking the 'login' link failed.\n"
            f"Expected URL is = '{Urls.LOGIN}'\n"
            f"Actual URL is = '{register_company_page.get_current_url()}'"
        )

        login_page = LoginPage(self.driver)
        valid_email = register_user_fixture["email"]
        valid_password = register_user_fixture["password"]

        login_page.login(valid_email, valid_password)

        assert login_page.is_login_before_company_successful(), (
            "Login failed for a newly registered user without a company.\n"
            f"- Email used = '{valid_email}'\n"
            f"- Password used = '{valid_password}'\n"
            f"Current URL is = '{login_page.get_current_url()}'"
        )

    def test_login_valid_unsubscribed_user(self, register_user_and_company_fixture):
        """
        Verify that a registered unsubscribed user with a registered company can log in
        and is redirected to the subscription page.
        """
        subscription_page = SubscriptionPage(self.driver)
        subscription_page.logout()

        assert subscription_page.is_logout_successful(), (
            "Logout failed.\n"
            "As a result, the login test cannot proceed."
        )

        login_page = LoginPage(self.driver)
        user_data, _ = register_user_and_company_fixture
        valid_email = user_data["email"]
        valid_password = user_data["password"]

        login_page.login(valid_email, valid_password)

        assert login_page.is_login_successful(), (
            "Login failed for a registered user with a company before subscription.\n"
            f"- Email used = '{valid_email}'\n"
            f"- Password used =  '{valid_password}'\n"
            f"Current URL = '{login_page.get_current_url()}'"
        )

    def test_login_valid_subscribed_user(self, register_user_and_company_fixture):
        """
        Verify that a registered subscribed user with a registered company can log in
        and is redirected to the dashboard.
        """
        subscription_page = SubscriptionPage(self.driver)
        subscription_page.select_offer("essai")

        assert subscription_page.is_offer_selection_successful("essai"), (
            "Redirection failed after selecting 'essai' offer.\n"
            f"Current URL is = '{subscription_page.get_current_url()}'"
        )

        subscription_page.logout()
        assert subscription_page.is_logout_successful(), (
            "Logout failed.\n"
            "As a result, the login test cannot proceed."
        )
        login_page = LoginPage(self.driver)
        user_data, _ = register_user_and_company_fixture
        valid_email = user_data["email"]
        valid_password = user_data["password"]

        login_page.login(valid_email, valid_password)
        login_page.set_subscription_required(False)
        assert login_page.is_login_successful(), (
            "Login failed for a subscribed user\n"
            f"- Email used = '{valid_email}'\n"
            f"- Password used =  '{valid_password}'\n"
            f"Current URL = '{login_page.get_current_url()}'"
        )