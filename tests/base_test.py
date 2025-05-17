import logging
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages.register_company_page import RegisterCompanyPage
from pages.register_page import RegisterPage


class BaseTest:
    driver: WebDriver
    logger: logging.Logger
    
    @pytest.fixture(autouse=True)
    def setup(self, request, setup_webdriver):
        """
        Setup method that runs before and after every test.
          Args:
                   request: pytest request object
                   setup_webdriver: fixture that provides a webdriver instance
        """

        self.driver = setup_webdriver
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        test_name = request.node.name
        self.driver.delete_all_cookies()
        self.logger.info(f"Starting test: {test_name}")

        yield

        self.logger.info(f"Finished test: {test_name}")
        try:
            self.driver.quit()
        except Exception as e:
            self.logger.info(
                f"The browser was already closed or an error occurred | {str(e)}"
            )

    @pytest.fixture
    def register_user_fixture(self):
        """Fixture to create a valid user."""
        # Step 1: User registration
        register_page = RegisterPage(self.driver)
        register_page.open()
        user_data = register_page.register_valid_user()
        assert register_page.is_registration_successful(), (
            "Initial user registration failed.\n"
            "Therefore, test cannot proceed."
        )
        return user_data

    @pytest.fixture
    def register_user_and_company_fixture(self):
        """ fixture to create a valid user and a valid company."""
        # Step 1: User registration
        register_page = RegisterPage(self.driver)
        register_page.open()
        user_data = register_page.register_valid_user()
        assert register_page.is_registration_successful(), (
            "Initial user registration failed.\n"
            "Therefore, test cannot proceed."
        )


        # Step 2: Company registration
        register_company_page = RegisterCompanyPage(self.driver)
        company_data = register_company_page.register_valid_company()
        register_company_page.set_subscription_required(True)
        assert register_company_page.is_company_registration_successful(), (
            "Company registration failed.\n"
            "Therefore, test cannot proceed."
        )

        return user_data, company_data




