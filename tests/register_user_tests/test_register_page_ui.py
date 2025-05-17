from pages.register_page import RegisterPage
from tests.base_test import BaseTest
from utils.locators.register_page_locators import RegisterPageLocators
from utils.ui_texts.register_page_ui import RegisterPageUI

class TestRegisterPageUI(BaseTest):
    def test_login_page_title(self):
        """Validate the register page title"""
        register_page = RegisterPage(self.driver)
        register_page.open()
        actual_title = register_page.get_title()
        expected_title = RegisterPageUI.REGISTER_PAGE_TITLE
        assert actual_title == expected_title, (
            f"Register Page title ERROR\n "
            f"Expected = '{expected_title}'\n"
            f"Actual = '{actual_title}'. "
        )
    def test_continue_button_text(self):
        """Validate the accuracy of the 'Continue' button text"""
        register_page = RegisterPage(self.driver)
        register_page.open()
        element = register_page.find_element(RegisterPageLocators.CONTINUE_BUTTON)
        actual_text = register_page.get_text(element)
        expected_text = RegisterPageUI.CONTINUE_BUTTON
        assert  actual_text == expected_text, (
            f"CONTINUE BUTTON TEXT ERROR\n "
            f"Expected = '{expected_text}'\n"
            f"Actual = '{actual_text}'. "
        )

    def test_login_link_text(self):
        """Validate the accuracy of the login link text"""
        register_page = RegisterPage(self.driver)
        register_page.open()
        element = register_page.find_element(RegisterPageLocators.LOGIN_LINK)
        actual_text = register_page.get_text(element)
        expected_text = RegisterPageUI.LOGIN_LINK
        assert actual_text == expected_text, (
            f"LOGIN LINK TEXT ERROR\n "
            f"Expected = '{expected_text}'\n"
            f"Actual = '{actual_text}'. "
        )
