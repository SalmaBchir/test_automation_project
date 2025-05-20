import email
import imaplib
import re
import time
from pages.forgot_password_page import ForgotPasswordPage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.reset_password_page import ResetPasswordPage
from utils.users import ValidUserData, ResetPasswordData
from utils.validation_messages.forgot_password_page_messages import ForgotPasswordPageMessages


class ResetPasswordHelper:
    @staticmethod
    def check_reset_email_received(driver,target_email,subject_keyword,
                                   timeout_sec: int = 60,
                                   interval_sec: int = 5,
                                  ) -> str:
        """
        Wait for a reset password email to be received and extract the reset link.
        Args:
            driver: WebDriver instance
            target_email: The target email address to check for
            timeout_sec: Maximum time to wait for the email (seconds)
            interval_sec: Delay between email checks (seconds)
            subject_keyword: Keyword to search in email subject
        Returns:
            The reset password URL extracted from the email body
        Raises:
            TimeoutError: If no email is received within timeout period
            ValueError: If email is found but no reset link can be extracted
            IMAPError: For issues with IMAP server communication
        """

        imap_folder = ResetPasswordData.IMAP_FOLDER
        imap_server = ResetPasswordData.IMAP_SERVER
        content_types = ("text/plain", "text/html")
        test_email = ResetPasswordData.IMAP_EMAIL
        test_password = ResetPasswordData.IMAP_PASSWORD

        def extract_reset_link(body: str) -> str:
            """Extract reset link from email body."""
            url_pattern = r'(https?://[^\s<>"]+reset[^\s<>"]+)'
            match = re.search(url_pattern, body)
            if not match:
                raise ValueError("No reset link found in email body")
            return match.group(1)

        try:
            with imaplib.IMAP4_SSL(imap_server) as mail:
                mail.login(test_email, test_password)
                driver.logger.info(f"Connected to IMAP server, waiting for reset email to {target_email}...")
                start_time = time.time()
                while (time.time() - start_time) < timeout_sec:
                    try:
                        status, _ = mail.select(imap_folder)
                        if status != "OK":
                            raise ConnectionError(f"Failed to select {imap_folder}")

                        search_query = f'(UNSEEN SUBJECT "{subject_keyword}" TO "{target_email}")'
                        status, messages = mail.search(None, search_query)

                        if status == "OK" and messages[0]:
                            latest_email_id = messages[0].split()[-1]
                            status, msg_data = mail.fetch(latest_email_id, '(RFC822)')

                            if status != "OK":
                                continue

                            raw_email = msg_data[0][1]
                            msg = email.message_from_bytes(raw_email)
                            body = ""

                            # Parse multipart and singlepart emails
                            if msg.is_multipart():
                                for content_type in content_types:
                                    for part in msg.walk():
                                        if part.get_content_type() == content_type:
                                            body = part.get_payload(decode=True).decode()
                                            break
                                    if body:
                                        break
                            else:
                                body = msg.get_payload(decode=True).decode()

                            if body:
                                return extract_reset_link(body)

                    except Exception as e:
                        driver.logger.warning(f"Temporary error during email check = {str(e)}")

                    time.sleep(interval_sec)

        except imaplib.IMAP4.error as e:
            error_msg = f"IMAP server error: {str(e)}"
            driver.logger.error(error_msg)
            raise ConnectionError(error_msg) from e
        except Exception as e:
            driver.logger.error(f"Unexpected error: {str(e)}")
            raise

        raise TimeoutError(
            f"No reset email received for {target_email} within {timeout_sec} seconds"
        )

    @staticmethod
    def register_then_request_and_open_password_reset_link(driver, email: str) -> None:
        register_page = RegisterPage(driver)
        register_page.open()
        register_page.register(
            ValidUserData.VALID_FIRSTNAME,
            ValidUserData.VALID_LASTNAME,
            email,
            ValidUserData.VALID_PASSWORD,
            ValidUserData.VALID_PASSWORD
        )

        assert register_page.is_registration_successful(), (
            "Initial user registration failed.\n"
            "Therefore, test cannot proceed."
        )
        register_page.click_login_link()
        assert register_page.is_login_page_opened(),(
            "Redirection from the registration page to the login page failed.\n"
            "Therefore, test cannot proceed"
        )
        login_page = LoginPage(driver)
        login_page.click_forgot_password_link()
        assert login_page.is_forgot_password_page_opened(), (
            "Redirection from register page to login page failed.\n"
            "Therefore, test cannot proceed"
        )
        forgot_password_page = ForgotPasswordPage(driver)
        forgot_password_page.request_password_reset(email)
        actual_message = forgot_password_page.get_validation_message()
        expected_message = ForgotPasswordPageMessages.SUCCESS_MESSAGE
        assert expected_message in actual_message, (
            f"Validation error mismatch.\n"
            f"Expected = '{expected_message}'\n"
            f"Actual = '{actual_message}' (normally used for: "
            f"'{ForgotPasswordPageMessages.get_message_type(actual_message)}')"
        )
        # Check for reset email
        reset_password_page = ResetPasswordPage(driver)
        reset_link = ResetPasswordHelper.check_reset_email_received(driver, email, ResetPasswordData.SUBJECT_KEYWORD)

        # Proceed with password reset
        reset_password_page.open(reset_link=reset_link)
        assert reset_password_page.is_reset_password_page_opened(), (
            f"Opening the reset password page failed.\n"
            f" when using link = '{reset_link}' extracted from the reset mail received\n'"
            f" Current URL is ='{reset_password_page.get_current_url()}'"
        )