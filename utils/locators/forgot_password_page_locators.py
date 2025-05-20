from selenium.webdriver.common.by import By

from utils.urls import Urls


class ForgotPasswordPageLocators:
    """
    locators for the forgot password page elements
    """
    VALIDATION_MESSAGE =  (By.CLASS_NAME, "alert")
    EMAIL_FIELD = (By.XPATH, "//input[@name='email']")
    SEND_BUTTON = (By.CLASS_NAME, "btn")
    CREATE_ACCOUNT_LINK = (By.XPATH, f"//*[@href='{Urls.CREATE_ACCOUNT}']")
