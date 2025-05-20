from pages.login_page import LoginPage
from tests.base_test import BaseTest
from utils.locators.login_page_locators import LoginPageLocators
from utils.ui_texts.login_page_ui import LoginPageUI

class TestLoginPageUI(BaseTest):

    def test_login_page_title(self):
        """Validate the login page title"""
        login_page = LoginPage(self.driver)
        login_page.open()
        actual_title = login_page.get_title()
        expected_title = LoginPageUI.LOGIN_PAGE_TITLE
        assert actual_title == expected_title, (
            f"LOGIN PAGE TITLE ERROR\n "
            f"Expected = '{expected_title}'\n"
            f"Actual = '{actual_title}'. "
        )

    def test_forgot_password_link_text(self):
        """Validate the accuracy of the 'forgot password' link text"""
        login_page = LoginPage(self.driver)
        login_page.open()
        element = login_page.find_element(LoginPageLocators.FORGOT_PASSWORD_LINK)
        actual_text = login_page.get_text(element)
        expected_text = LoginPageUI.FORGOT_PASSWORD_LINK
        assert actual_text == expected_text, (
            f"FORGOT PASSWORD LINK TEXT ERROR\n "
            f"Expected= '{expected_text}'\n"
            f"Actual= '{actual_text}'. "
        )

    def test_create_account_link_text(self):
        """Validate the accuracy of the 'Create account' link text"""
        login_page = LoginPage(self.driver)
        login_page.open()
        element = login_page.find_element(LoginPageLocators.CREATE_ACCOUNT_LINK)
        actual_text = login_page.get_text(element)
        expected_text = LoginPageUI.CREATE_ACCOUNT_LINK
        assert actual_text == expected_text, (
            f"CREATE ACCOUNT LINK TEXT ERROR\n"
            f"Expected= '{expected_text}'\n"
            f"Actual= '{actual_text}'. "
        )