from pages.login_page import LoginPage
from tests.base_test import BaseTest
from utils.urls import Urls

class TestRedirectsFromLoginPage(BaseTest):
    def test_navigate_to_forgot_password_page(self):
        """Verify that clicking the 'Forgot password' link on the login page
                navigates to the 'Forgot password' page"""
        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.click_forgot_password_link()
        assert login_page.is_forgot_password_page_opened(),(
            f"Redirection to the 'Forgot Password' page failed.\n"
            f" expected URL is = '{Urls.FORGOT_PASSWORD}'\n"
            f"Current URL is = '{login_page.get_current_url()}'"
        )

    def test_navigate_to_create_account_page(self):
        """Verify that clicking the 'Create account' link on the login page
        navigates to the user registration page."""
        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.click_create_account_link()
        assert login_page.is_register_page_opened(), (
            f"Redirection to the user registration page failed.\n"
            f" expected URL is ='{Urls.CREATE_ACCOUNT}\n'"
            f" Current URL is ='{login_page.get_current_url()}'"
        )


