from pages.register_company_page import RegisterCompanyPage
from tests.base_test import BaseTest


class TestCompanyRegisterValid(BaseTest):


    def test_company_register_valid(self, register_user_fixture):
        """Verify that a new valid company can be successfully registered."""
        register_company_page = RegisterCompanyPage(self.driver)
        company_data = register_company_page.register_valid_company()
        register_company_page.set_subscription_required(True)
        assert register_company_page.is_company_registration_successful(), (
            f"Company registration failed for a new valid company.\n"
            f"user email used = '{register_user_fixture['email']}'\n"
            f"user password used = '{register_user_fixture['password']}'\n"
            f"Company name used = '{company_data['name']}'\n"
            f"Company email used = '{company_data['email']}'\n"
            f"Company siret used = '{company_data['siret']}'\n"
            f"Current URL is = '{register_company_page.get_current_url()}'\n"

        )

