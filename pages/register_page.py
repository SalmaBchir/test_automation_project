from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from utils.locators.register_page_locators import RegisterPageLocators
from utils.urls import Urls
from utils.users import ValidUserData  # Added import

class RegisterPage(BasePage):
    """Page object for the Register page"""
    def open(self):
        """Open the register page using the predefined URL"""
        self.open_url(Urls.CREATE_ACCOUNT)

    def enter_lastname(self,lastname):
        """Enter lastname in the lastname field
        Args:
            lastname: lastname to be entered
        """
        lastname_field = self.find_element(RegisterPageLocators.LASTNAME_FIELD)
        self.input_text(lastname_field, lastname)

    def enter_firstname(self, firstname):
        """Enter firstname in the firstname field
        Args:
            firstname: firstname to be entered
        """
        firstname_field = self.find_element(RegisterPageLocators.FIRSTNAME_FIELD)
        self.input_text(firstname_field, firstname)

    def enter_email(self, email):
        """Enter email in the email field
        Args:
            email: Email to be entered
        """
        email_field = self.find_element(RegisterPageLocators.EMAIL_FIELD)
        self.input_text(email_field, email)

    def enter_password(self, password):
        """Enter password in the password field
        Args:
            password: Password to be entered
        """
        password_field = self.find_element(RegisterPageLocators.PASSWORD_FIELD)
        self.input_text(password_field, password)

    def enter_password_confirmation(self, password_confirmation):
        """Enter password_confirmation in the password_confirmation field
        Args:
            password_confirmation: Password to be entered
        """
        password_confirmation_field = self.find_element(RegisterPageLocators.PASSWORD_CONFIRMATION_FIELD)
        self.input_text(password_confirmation_field, password_confirmation)

    def click_continue_button(self):
        """Click on the continue button"""
        continue_button = self.find_element(RegisterPageLocators.CONTINUE_BUTTON)
        self.click_element(continue_button)

    def register(self, lastname,firstname, email, password, password_confirmation):
        """Perform the register action sequence
        Args:
            lastname : admin lastname
            firstname : admin firstname
            email: Email to use
            password: Password to use
            password_confirmation
        """
        self.enter_lastname(lastname)
        self.enter_firstname(firstname)
        self.enter_email(email)
        self.enter_password(password)
        self.enter_password_confirmation(password_confirmation)
        self.click_continue_button()

    def register_valid_user(self):
        """Register a valid user and return the user data."""
        password = ValidUserData.VALID_PASSWORD
        user_data = {
            "lastname": ValidUserData.VALID_LASTNAME,
            "firstname": ValidUserData.VALID_FIRSTNAME,
            "email": ValidUserData.generate_valid_email(),
            "password": password,
            "password_confirmation": password
        }
        self.register(
            user_data["lastname"],
            user_data["firstname"],
            user_data["email"],
            user_data["password"],
            user_data["password_confirmation"]
        )
        return user_data

    def click_login_link(self):
        """Click on the login link"""
        login_link = self.find_element(RegisterPageLocators.LOGIN_LINK)
        self.click_element(login_link)

    def get_register_error_message(self):
        element= self.find_element(RegisterPageLocators.ERROR_MESSAGE)
        return self.get_text(element)

    def is_registration_successful(self):
        """Check if registration was successful
        Returns:
            bool: True if registration was successful, False otherwise.
        """
        try:
            self.wait.until(EC.url_to_be(Urls.REGISTER_COMPANY))
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            self.logger.info(f"User registered, current URL is = '{self.get_current_url()}'")
            return True
        except TimeoutException:
            self.logger.info(
                f"Current URL after registration attempt is = '{self.get_current_url()}'"
            )
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