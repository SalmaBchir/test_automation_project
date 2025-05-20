from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from utils.locators.register_company_page_locators import  RegisterCompanyPageLocators
from utils.urls import Urls
from utils.users import ValidCompanyData


class RegisterCompanyPage(BasePage):
    """Page object for the Register Company page"""
    def open(self):
        """Open the register company page using the predefined URL"""
        self.open_url(Urls.REGISTER_COMPANY)

    def enter_name(self,name):
        """Enter name in the name field
        Args:
            name:  company name to be entered
        """
        name_field = self.find_element(RegisterCompanyPageLocators.NAME_FIELD)
        self.input_text(name_field, name)


    def enter_email(self, email):
        """Enter email in the email field
        Args:
            email: Email to be entered
        """
        email_field = self.find_element(RegisterCompanyPageLocators.EMAIL_FIELD)
        self.input_text(email_field, email)

    def enter_siret(self, siret):
        """Enter 'siret' in the siret field
        Args:
            siret: to be entered
        """
        siret_field = self.find_element(RegisterCompanyPageLocators.SIRET_FIELD)
        self.input_text(siret_field, siret)

    def click_connection_button(self):
        """Click on the connection button"""
        connection_button = self.find_element(RegisterCompanyPageLocators.CONNECTION_BUTTON)
        self.click_element(connection_button)

    def register_company(self, name,email,siret):
        """Perform the register company action sequence
        Args:
            name : company name
            email: company email
            siret
        """
        self.enter_name(name)
        self.enter_email(email)
        self.enter_siret(siret)
        self.click_connection_button()

    def register_valid_company(self):
        """Register a valid company and return the company data."""
        company_data = {
            "name": ValidCompanyData.VALID_NAME,
            "email": ValidCompanyData.generate_valid_email(),
            "siret": ValidCompanyData.VALID_SIRET
        }
        self.register_company(
            company_data["name"],
            company_data["email"],
            company_data["siret"]
        )
        return company_data

    def click_login_link(self):
        """Click on the login link"""
        login_link = self.find_element(RegisterCompanyPageLocators.LOGIN_LINK)
        self.click_element(login_link)

    def get_register_company_error_message(self):
        element=self.find_element(RegisterCompanyPageLocators.ERROR_MESSAGE)
        return self.get_text(element)

    def is_company_registration_successful(self):
        """
        Check if company registration was successful
        Returns:
            bool: True if company registration was successful, False otherwise.
        """
        try:
            target_url = Urls.SUBSCRIPTION if self.is_subscription_required else Urls.DASHBOARD
            self.wait.until(EC.url_to_be(target_url))
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            self.logger.info(f"Company registered, current URL is = '{target_url}'")
            return True

        except TimeoutException:
            self.logger.info(
                f"Current URL after company registration attempt is = '{self.get_current_url()}'")
            return False

    def is_login_page_opened(self):
        """Check if the 'login page' is opened
                Returns:
                    bool: True if redirection to the login page is successful, False otherwise
                """
        try:
            self.wait.until(EC.url_to_be(Urls.LOGIN))
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            self.logger.info(f"Redirected to the login page = '{Urls.LOGIN}'")
            return True
        except TimeoutException:
            self.logger.error(
                f"Redirection to the login page failed. "
                f"expected ='{Urls.LOGIN}'- "
                f"Current url is = '{self.get_current_url()}'")
            return False

    