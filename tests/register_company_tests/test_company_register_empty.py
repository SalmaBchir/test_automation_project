import pytest
from pages.register_company_page import RegisterCompanyPage
from tests.base_test import BaseTest
from utils.validation_messages.register_company_page_messages import RegisterCompanyPageMessages
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
        expected_error = RegisterCompanyPageMessages.EMPTY_NAME
        assert expected_error in error_message, (
            f"Validation error mismatch for company name = '{name}'.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}' (normally used for: "
            f"{RegisterCompanyPageMessages.get_message_type(error_message)})"
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
        expected_error = RegisterCompanyPageMessages.EMPTY_EMAIL
        assert expected_error in error_message, (
            f"Validation error mismatch for email = '{email}'.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}' (normally used for: "
            f"{RegisterCompanyPageMessages.get_message_type(error_message)})"
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
        expected_error = RegisterCompanyPageMessages.EMPTY_SIRET
        assert expected_error in error_message, (
            f"Validation error mismatch for siret = '{siret}'.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}' (normally used for: "
            f"{RegisterCompanyPageMessages.get_message_type(error_message)})"
        )