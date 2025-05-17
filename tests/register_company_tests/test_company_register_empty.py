import pytest
from pages.register_company_page import RegisterCompanyPage
from tests.base_test import BaseTest
from utils.error_messages.register_company_page_errors import RegisterCompanyPageErrors
from utils.users import ValidCompanyData


class TestCompanyRegisterEmptyFields(BaseTest):


    @pytest.mark.parametrize("name", ['', '         '])
    def test_company_register_empty_name(self, name,register_user_fixture):
        """Verify that company registration fails for an empty or whitespace-only name"""
        register_company_page = RegisterCompanyPage(self.driver)
        register_company_page.register_company(name, ValidCompanyData.generate_valid_email(), ValidCompanyData.VALID_SIRET)
        assert not register_company_page.is_company_registration_successful(), (
            f"Unexpected company registration success with company name = '{name}'"
        )
        error_message = register_company_page.get_register_company_error_message()
        expected_error = RegisterCompanyPageErrors.EMPTY_NAME
        assert expected_error in error_message, (
            f"Validation error mismatch.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}'"
        )

    @pytest.mark.parametrize("email", ['', '         '])
    def test_company_register_empty_email(self, email,register_user_fixture):
        """Verify that company registration fails for an empty or whitespace-only email"""
        register_company_page = RegisterCompanyPage(self.driver)
        register_company_page.register_company(ValidCompanyData.VALID_NAME, email, ValidCompanyData.VALID_SIRET)
        register_company_page.set_subscription_required(True)
        assert not register_company_page.is_company_registration_successful(), (
            f"Unexpected company registration success with email = '{email}'"
        )
        error_message = register_company_page.get_register_company_error_message()
        expected_error = RegisterCompanyPageErrors.EMPTY_EMAIL
        assert expected_error in error_message, (
            f"Validation error mismatch.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}'"
        )

    @pytest.mark.parametrize("siret", ['', '         '])
    def test_company_register_empty_siret(self, siret,register_user_fixture):
        """Verify that company registration fails for an empty or whitespace-only SIRET"""
        register_company_page = RegisterCompanyPage(self.driver)
        register_company_page.register_company(ValidCompanyData.VALID_NAME, ValidCompanyData.generate_valid_email(), siret)
        register_company_page.set_subscription_required(True)
        assert not register_company_page.is_company_registration_successful(), (
            f"Unexpected company registration success with SIRET = '{siret}'"
        )
        error_message = register_company_page.get_register_company_error_message()
        expected_error = RegisterCompanyPageErrors.EMPTY_SIRET
        assert expected_error in error_message, (
            f"Validation error mismatch.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}'"
        )