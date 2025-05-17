import random
import string

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

class RegisteredUsers:
   """
   Centralized repository of pre-registered user accounts
   """
