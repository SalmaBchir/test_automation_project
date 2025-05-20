from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from utils.locators.dashboard_page_locators import DashboardPageLocators
from utils.urls import Urls



class DashboardPage(BasePage):
    """Page object for the dashboard page"""

    def open(self):
        """Open the dashboard page using the predefined URL"""
        self.open_url(Urls.DASHBOARD)

    def logout(self):
        """logging out"""
        menu= self.find_element(DashboardPageLocators.DROPDOWN_TOGGLE)
        self.click_element(menu)
        logout_option = self.find_element(DashboardPageLocators.DROPDOWN_ITEM_LOGOUT)
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