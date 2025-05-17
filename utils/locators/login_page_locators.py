from utils.urls import Urls
from selenium.webdriver.common.by import By

class LoginPageLocators:
    """
    locators for login page elements
    """

    EMAIL_FIELD = (By.XPATH, "//input[@name='email']")
    PASSWORD_FIELD = (By.XPATH, "//input[@name='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    ERROR_MESSAGE = (By.CLASS_NAME, "alert")
    FORGOT_PASSWORD_LINK= (By.XPATH, f"//*[@href='{Urls.FORGOT_PASSWORD}']")
    CREATE_ACCOUNT_LINK = (By.XPATH, f"//*[@href='{Urls.CREATE_ACCOUNT}']")
