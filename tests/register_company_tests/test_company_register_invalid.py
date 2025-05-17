import pytest
from pages.register_company_page import RegisterCompanyPage
from tests.base_test import BaseTest
from utils.error_messages.register_company_page_errors import RegisterCompanyPageErrors
from utils.users import ValidCompanyData, InvalidCompanyData


class TestCompanyRegisterInvalidFields(BaseTest):



    @pytest.mark.parametrize("invalid_email", InvalidCompanyData.generate_invalid_email())
    def test_company_register_invalid_email(self, invalid_email,register_user_fixture):
        """Verify that company registration fails with an invalid email."""
        register_company_page = RegisterCompanyPage(self.driver)
        register_company_page.register_company(
            ValidCompanyData.VALID_NAME,
            invalid_email,
            ValidCompanyData.VALID_SIRET
        )
        assert not register_company_page.is_company_registration_successful(), (
            f"Unexpected success in company registration with invalid email: '{invalid_email}'"
        )
        error_message = register_company_page.get_register_company_error_message()
        expected_error = RegisterCompanyPageErrors.INVALID_EMAIL
        assert expected_error in error_message, (
            f"Validation error mismatch.\n"
            f"Expected: '{expected_error}'\n"
            f"Actual: '{error_message}'"
            f"The system should flag the email ='{invalid_email}' as invalid."
        )