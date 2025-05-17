from selenium.webdriver.common.by import By
from utils.urls import Urls

class SubscriptionPageLocators:
    """
      locators for subscription page elements
    """
    DROPDOWN_TOGGLE = (By.CLASS_NAME, "btn-profil")
    DROPDOWN_ITEM_PROFILE  = (By.XPATH, f"//*[@href='{Urls.PROFILE}']")
    DROPDOWN_ITEM_HISTORY= (By.XPATH, f"//*[@href='{Urls.COMPANY_HISTORY}']")
    DROPDOWN_ITEM_LOGOUT = (By.XPATH, f"//*[@href='{Urls.LOGOUT}']")

    offer = {}
    offer_name = {}
    offer_button = {}

    for i in range(1, 5):
        base_xpath = f"//form[input[@name='abonnement_id' and @value='{i}']]"
        offer[i] = (By.XPATH, base_xpath)
        offer_name[i] = (By.XPATH, base_xpath + "//h4")
        offer_button[i] = (By.XPATH, base_xpath + "//button")