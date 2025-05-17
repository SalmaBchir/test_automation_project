from utils.urls import Urls
from selenium.webdriver.common.by import By

class RegisterPageLocators:
    """
    locators for register page elements
    """

    LASTNAME_FIELD = (By.XPATH, "//input[@name='nom']")
    FIRSTNAME_FIELD = (By.XPATH, "//input[@name='prenom']")
    EMAIL_FIELD = (By.XPATH, "//input[@name='email']")
    PASSWORD_FIELD = (By.XPATH, "//input[@name='password']")
    PASSWORD_CONFIRMATION_FIELD = (By.XPATH, "//input[@name='password_confirmation']")
    CONTINUE_BUTTON = (By.CLASS_NAME, "btn")
    ERROR_MESSAGE = (By.CLASS_NAME, "alert")
    LOGIN_LINK= (By.XPATH, f"//*[@href='{Urls.LOGIN}']")
