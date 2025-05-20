from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from utils.locators.login_page_locators import LoginPageLocators
from utils.urls import Urls


class LoginPage(BasePage):
    """Page object for the login page"""

    def open(self):
        """Open the login page using the predefined URL"""
        self.open_url(Urls.LOGIN)

    def enter_email(self, email):
        """Enter email in the email field
        Args:
            email: Email to be entered
        """
        email_field = self.find_element(LoginPageLocators.EMAIL_FIELD)
        self.input_text(email_field, email)

    def enter_password(self, password):
        """Enter password in the password field
        Args:
            password: Password to be entered
        """
        password_field = self.find_element(LoginPageLocators.PASSWORD_FIELD)
        self.input_text(password_field, password)

    def click_login_button(self):
        """Click on the login button"""
        login_button = self.find_element(LoginPageLocators.LOGIN_BUTTON)
        self.click_element(login_button)


    def login(self, email, password):
        """Perform the login action sequence
        Args:
            email: Email to use
            password: Password to use
        """
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()

    def click_forgot_password_link(self):
        """Click on the 'Forgot Password' link"""
        forgot_password_link = self.find_element(LoginPageLocators.FORGOT_PASSWORD_LINK)
        self.click_element(forgot_password_link)

    def click_create_account_link(self):
        """Click on the 'Create_account' link"""
        create_account_link = self.find_element(LoginPageLocators.CREATE_ACCOUNT_LINK)
        self.click_element(create_account_link)

    def get_login_validation_message(self):
        element = self.find_element(LoginPageLocators.VALIDATION_MESSAGE)
        return self.get_text(element)

    def is_login_before_company_successful(self):
        """
          Check if the login succeeded and redirected to the company registration page.

          Returns:
              bool: True if redirected to the company registration URL.
          """
        try:
            self.wait.until(EC.url_to_be(Urls.REGISTER_COMPANY))
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            self.logger.info(f"User logged in, current URL is = '{self.get_current_url()}'")
            return True

        except TimeoutException:
            current_url = self.get_current_url()
            self.logger.info(f"Current URL after login attempt is = '{current_url}'")
            return False

    def is_login_successful(self):
        """Check if login was successful
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            target_url = Urls.SUBSCRIPTION if self.is_subscription_required else Urls.DASHBOARD
            self.wait.until(EC.url_to_be(target_url))
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            self.logger.info(f"User logged in, current URL is = '{self.get_current_url()}'")
            return True

        except TimeoutException:
            current_url = self.get_current_url()
            self.logger.info(f"Current URL after login attempt is = '{current_url}'")
            return False




    def is_forgot_password_page_opened(self):
        """Check if the 'Forgot Password' page is opened
        Returns:
            bool: True if redirection to 'Forgot Password' page is successful, False otherwise
        """
        try:
            self.wait.until(EC.url_to_be(Urls.FORGOT_PASSWORD))
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            self.logger.info(f"Redirected to 'Forgot Password' page = '{Urls.FORGOT_PASSWORD}'")
            return True
        except TimeoutException:
            self.logger.error(f"Redirection to 'Forgot Password' page failed = expected '{Urls.FORGOT_PASSWORD}'- Current url is = '{self.get_current_url()}'")
            return False

    def is_register_page_opened(self):
        """Check if the register page is opened
        Returns:
            bool: True if redirection to the register page is successful, False otherwise
        """
        try:
            self.wait.until(EC.url_to_be(Urls.CREATE_ACCOUNT))
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            self.logger.info(f"Redirected to the register page = '{Urls.CREATE_ACCOUNT}'")
            return True
        except TimeoutException:
            self.logger.error(
                f"Redirection to the register page failed. "
                f"expected ='{Urls.CREATE_ACCOUNT}'"
                f"- Current url is = '{self.get_current_url()}")
            return False