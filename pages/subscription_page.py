from pages.base_page import BasePage
from utils.locators.subscription_page_locators import SubscriptionPageLocators
from utils.urls import Urls
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException



class SubscriptionPage(BasePage):
    """Page object for the subscription page"""
    def open(self):
        """Open the subscription page using the predefined URL"""
        self.open_url(Urls.SUBSCRIPTION)

    def logout(self):
        """logging out"""
        menu= self.find_element(SubscriptionPageLocators.DROPDOWN_TOGGLE)
        self.click_element(menu)
        logout_option = self.find_element(SubscriptionPageLocators.DROPDOWN_ITEM_LOGOUT)
        self.click_element(logout_option)

    def is_logout_successful(self):
        try:
            self.wait.until(EC.url_to_be(Urls.LOGIN))
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            self.logger.info(f"Logout successful. Current URL is = '{self.get_current_url()}'")
            return True
        except TimeoutException:
            self.logger.info(f"Logout failed. Current URL is = '{self.get_current_url()}'")
            return False

    def is_offer_present(self, offer_name: str) -> tuple[bool, int | None]:
        """
        Check if the offer with the given name exists on the page.

        Args:
            offer_name (str): The name of the offer to find (case-insensitive).

        Returns:
            tuple: (True, index) if the offer exists, otherwise (False, None).
        """
        offer_name = offer_name.strip().lower()
        for i in range(1, 5):
            if self.is_element_present(SubscriptionPageLocators.offer_name[i]):
                element = self.find_element(SubscriptionPageLocators.offer_name[i])
                text = element.text.strip().lower()
                if text == offer_name:
                    self.logger.info(f"Offer '{offer_name}' found with index {i}.")
                    return True, i

        self.logger.info(f"Offer '{offer_name}' not found on the subscription page.")
        return False, None

    def select_offer(self, offer_name: str):
        """
        Click on the subscription button of the offer with the given name.

        Args:
            offer_name (str): The name of the offer to select (case-insensitive).

        Raises:
            ValueError: If the offer is not present on the page.
        """
        exists, index = self.is_offer_present(offer_name)
        if exists and index:
            self.logger.info(f"Selecting the offer '{offer_name}' at index {index}.")
            button = self.find_element(SubscriptionPageLocators.offer_button[index])
            self.click_element(button)
        else:
            self.logger.error(f"Offer '{offer_name}' not found. Cannot perform click.")
            raise ValueError(f"Offer '{offer_name}' not found. Cannot perform click.")



    def is_offer_selection_successful(self, offer_name: str) -> bool:
        """
        Check if the user has been redirected correctly after selecting a subscription offer.
        - If 'essai' is selected, expect redirection to the dashboard.
        - If another offer is selected, expect redirection to Stripe checkout.
        """

        offer_name = offer_name.strip().lower()

        try:
            if offer_name == "essai":
                self.wait.until(EC.url_to_be(Urls.DASHBOARD))
                self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                self.logger.info(f"User redirected to dashboard after selecting 'essai'. "
                                 f" Current URL is ='{self.get_current_url()}'")
                return True
            elif offer_name in ["standard", "medium", "premium"]:
                self.wait.until(EC.url_contains("https://checkout.stripe.com"))
                self.logger.info(
                    f"User redirected to Stripe checkout after selecting '{offer_name}'. "
                    f"Current URL is = '{self.get_current_url()}'")
                return True
            else:
                self.logger.error(f"Unknown offer name = '{offer_name}'")
                return False
        except TimeoutException:
            self.logger.error(f"Redirection failed for offer '{offer_name}'. "
                              f"Current URL is = '{self.get_current_url()}'")
            return False
