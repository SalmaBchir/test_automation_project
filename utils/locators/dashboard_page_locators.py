from selenium.webdriver.common.by import By

from utils.urls import Urls


class DashboardPageLocators:
    """
    locators for dashbord page elements
    """
    DROPDOWN_TOGGLE = (By.CLASS_NAME, "btn-profil")
    DROPDOWN_ITEM_PROFILE  = (By.XPATH, f"//*[@href='{Urls.PROFILE}']")
    DROPDOWN_ITEM_HISTORY= (By.XPATH, f"//*[@href='{Urls.COMPANY_HISTORY}']")
    DROPDOWN_ITEM_LOGOUT = (By.XPATH, f"//*[@href='{Urls.LOGOUT}']")