from pages.register_company_page import RegisterCompanyPage
from tests.base_test import BaseTest
from utils.locators.register_company_page_locators import RegisterCompanyPageLocators
from utils.ui_texts.register_company_page_ui import RegisterCOMPANYPageUI

class TestCompanyRegisterPageUI(BaseTest):

    def test_company_register_page_title(self, register_user_fixture):
        """Validate the company register page title"""
        register_company_page = RegisterCompanyPage(self.driver)
        register_company_page.open()
        actual_title = register_company_page.get_title()
        expected_title = RegisterCOMPANYPageUI.REGISTER_COMPANY_PAGE_TITLE
        assert actual_title == expected_title, (
            f"Register Company Page title ERROR\n "
            f"Expected = '{expected_title}'\n"
            f"Actual = '{actual_title}'. "
        )

    def test_connection_button_text(self, register_user_fixture):
        """Validate the accuracy of the 'Connection' button text"""
        register_company_page = RegisterCompanyPage(self.driver)
        register_company_page.open()
        element = register_company_page.find_element(RegisterCompanyPageLocators.CONNECTION_BUTTON)
        actual_text = register_company_page.get_text(element)
        expected_text = RegisterCOMPANYPageUI.CONNECTION_BUTTON
        assert actual_text == expected_text, (
            f"CONNECTION BUTTON TEXT ERROR\n "
            f"Expected = '{expected_text}'\n"
            f"Actual = '{actual_text}'. "
        )

    def test_login_link_text(self, register_user_fixture):
        """Validate the accuracy of the login link text"""
        register_company_page = RegisterCompanyPage(self.driver)
        register_company_page.open()
        element = register_company_page.find_element(RegisterCompanyPageLocators.LOGIN_LINK)
        actual_text = register_company_page.get_text(element)
        expected_text = RegisterCOMPANYPageUI.LOGIN_LINK
        assert actual_text == expected_text, (
            f"LOGIN LINK TEXT ERROR\n "
            f"Expected = '{expected_text}'\n"
            f"Actual = '{actual_text}'. "
        )
