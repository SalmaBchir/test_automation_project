from tests.base_test import BaseTest
from utils.urls import Urls
from pages.register_page import RegisterPage
class TestRedirectsFromRegisterPage(BaseTest):
    def test_navigate_to_login_page(self):
        """Verify that clicking the Login link on the user registration page
        navigates to the login page."""
        register_page = RegisterPage(self.driver)
        register_page.open()
        register_page.click_login_link()
        assert register_page.is_login_page_opened(),(
            f"Redirection to the login page failed\n"
            f" expected URL is = '{Urls.LOGIN}\n "
            f"- Current URL is = '{register_page.get_current_url()}'"
        )

