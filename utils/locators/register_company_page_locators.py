from utils.urls import Urls
from selenium.webdriver.common.by import By

class RegisterCompanyPageLocators:
    """
    locators for register Company page elements
    """

    NAME_FIELD = (By.XPATH, "//input[@name='nom']")
    EMAIL_FIELD = (By.XPATH, "//input[@name='email']")
    PASSWORD_FIELD = (By.XPATH, "//input[@name='password']")
    SIRET_FIELD = (By.XPATH, "//input[@name='siret']")
    CONNECTION_BUTTON = (By.CLASS_NAME, "btn")
    ERROR_MESSAGE = (By.CLASS_NAME, "alert")
    LOGIN_LINK= (By.XPATH, f"//*[@href='{Urls.LOGIN}']")