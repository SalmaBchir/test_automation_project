from selenium.webdriver.common.by import By



class ResetPasswordPageLocators:
    """
   locators for the forgot password page elements
   """
    PASSWORD_FIELD = (By.XPATH, "//input[@name='password']")
    PASSWORD_CONFIRMATION_FIELD = (By.XPATH, "//input[@name='password_confirmation']")
    RESET_BUTTON =  (By.CLASS_NAME, "btn")
    ERROR_MESSAGE = (By.CLASS_NAME, "alert")