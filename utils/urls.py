"""
Contains the main URL endpoints and their corresponding page titles
used throughout the application.
"""

class Urls:
    BASE_URL = "https://crm.rapidosoftware.com"
    DASHBOARD = f"{BASE_URL}/dashboard"
    LOGIN = f"{BASE_URL}/login"
    LOGOUT = f"{BASE_URL}/logout"
    CREATE_ACCOUNT = f"{BASE_URL}/register"
    REGISTER_COMPANY = f"{CREATE_ACCOUNT}/company"
    FORGOT_PASSWORD = f"{BASE_URL}/forgot-password"
    RESET_PASSWORD =  f"{BASE_URL}/reset-password/"
    SUBSCRIPTION = f"{BASE_URL}/change-forfait"
    COMPANY_HISTORY = f"{BASE_URL}/historiques"
    PROFILE = f"{BASE_URL}/profil"