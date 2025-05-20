import os
import random
import string
import time
class TestDataUtils:
    @staticmethod
    def generate_valid_email():
        """
        Generate a random email address with valid format and domain.
        Returns:
            str: Randomly generated email with valid format (a1b2c3d4@gmail.com)
        """
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"{random_string}@gmail.com"

    @staticmethod
    def generate_invalid_email():
        """
        Generates two types of invalid emails:
        1. Contains consecutive dots in domain part
        2. Missing top-level domain (e.g., .com, .net)
        Returns:
            list: Contains two types of invalid email strings
        """
        # Type 1: Invalid domain format with consecutive dots
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        invalid_email = f"{random_string}@d..c"

        # Type 2: Missing top-level domain
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        invalid_email2 = f"{random_string}@com"

        return [invalid_email, invalid_email2]


class ValidUserData:
    VALID_LASTNAME = "A"
    VALID_FIRSTNAME = "a"
    VALID_PASSWORD = "Abc12?!="

    @staticmethod
    def generate_valid_email():
        return TestDataUtils.generate_valid_email()


class InvalidUserData:
    """
    for testing negative cases.
    """

    INVALID_PASSWORD = "A"  # Too short (length < 8)

    @staticmethod
    def generate_invalid_email():
        return TestDataUtils.generate_invalid_email()

class ValidCompanyData:
    VALID_NAME = "A"
    VALID_SIRET = "1"

    @staticmethod
    def generate_valid_email():
        return TestDataUtils.generate_valid_email()

class InvalidCompanyData:

    @staticmethod
    def generate_invalid_email():
        return TestDataUtils.generate_invalid_email()


class ResetPasswordData:


    IMAP_EMAIL = f"{os.getenv('TEST_EMAIL_PREFIX')}@{os.getenv('TEST_EMAIL_DOMAIN')}"  # Email address used to receive password reset emails
    IMAP_SERVER = os.getenv("IMAP_SERVER")
    IMAP_PASSWORD = os.getenv("TEST_EMAIL_PASSWORD") #  (an app-specific password)
    IMAP_FOLDER =  os.getenv("IMAP_FOLDER")  # Folder in the mailbox where password reset emails might be delivered.
    NEW_VALID_PASSWORD = "newpassword"  # New password that will be set during the password reset process
    SUBJECT_KEYWORD = "mot de passe" # Keyword used to filter the password reset email by subject

    @classmethod
    def generate_test_email(cls):
        """
        Generates a unique test email address for reset_password_tests
        """
        return f"{os.getenv('TEST_EMAIL_PREFIX')}+test{int(time.time())}@{os.getenv('TEST_EMAIL_DOMAIN')}"