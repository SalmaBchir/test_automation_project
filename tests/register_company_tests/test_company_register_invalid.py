import pytest
from pages.register_company_page import RegisterCompanyPage
from tests.base_test import BaseTest
from utils.validation_messages.register_company_page_messages import RegisterCompanyPageMessages
from utils.users import ValidCompanyData, InvalidCompanyData


class TestCompanyRegisterInvalidFields(BaseTest):



    @pytest.mark.parametrize("invalid_email", InvalidCompanyData.generate_invalid_email())
    def test_company_register_invalid_email(self, invalid_email,register_user_fixture):
        """Verify that company registration fails when using an invalid email format."""
        register_company_page = RegisterCompanyPage(self.driver)
        register_company_page.register_company(
            ValidCompanyData.VALID_NAME,
            invalid_email,
            ValidCompanyData.VALID_SIRET
        )
        assert not register_company_page.is_company_registration_successful(), (
            f"Unexpected success in company registration with invalid email = '{invalid_email}'"
        )
        error_message = register_company_page.get_register_company_error_message()
        expected_error = RegisterCompanyPageMessages.INVALID_EMAIL
        assert expected_error in error_message, (
            f"Validation error mismatch for email = '{invalid_email}'.\n"
            f"Expected = '{expected_error}'\n"
            f"Actual = '{error_message}' (normally used for: "
            f"{RegisterCompanyPageMessages.get_message_type(error_message)})"
        )