from selenium.common import TimeoutException
from pages.register_company_page import RegisterCompanyPage
from tests.base_test import BaseTest


class TestDirectAccess(BaseTest):
    def test_direct_access(self):
        """Verify that direct access to the company registration page is not allowed."""
        register_company_page = RegisterCompanyPage(self.driver)
        try:
            register_company_page.open()
        except TimeoutException:
            assert True
            return
        assert False, (
            "Direct access to the company registration page succeeded\n"
            "but it should have failed."
        )