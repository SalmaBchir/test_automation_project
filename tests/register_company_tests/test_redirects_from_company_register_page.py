from tests.base_test import BaseTest
from utils.urls import Urls
from pages.register_company_page import RegisterCompanyPage

class TestRedirectsFromCompanyRegisterPage(BaseTest):
    def test_navigate_to_login_page(self,register_user_fixture):
        """Verify that clicking the Login link on the company registration page
        navigates to the login page."""
        register_company_page = RegisterCompanyPage(self.driver)
        register_company_page.click_login_link()
        assert register_company_page.is_login_page_opened(), (
            f"Redirection to the login page failed\n"
            f"Expected URL is = '{Urls.LOGIN}'\n"
            f"- Current URL is = '{register_company_page.get_current_url()}'"
        )