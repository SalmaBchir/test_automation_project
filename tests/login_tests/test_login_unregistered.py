from pages.login_page import LoginPage
from tests.base_test import BaseTest
from utils.users import ValidUserData

class TestLoginUnregistered(BaseTest):
    def test_login_unregistered(self):
        """Verify system prevents authentication with unregistered credentials"""
        login_page = LoginPage(self.driver)
        login_page.open()
        unregistered_email = ValidUserData.generate_valid_email()
        password = ValidUserData.VALID_PASSWORD
        login_page.login(unregistered_email, password)
        assert not login_page.is_login_successful(), (
            "SECURITY FAILURE: System allowed access with unregistered credentials\n"
            f"Used email: {unregistered_email}\n"
            f"Used password: {password}\n"
        )