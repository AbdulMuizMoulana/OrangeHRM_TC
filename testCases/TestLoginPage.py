import os
from pathlib import Path

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.LoginPage import LoginPage
from utilities.ReadProperties import ReadConfig
from utilities.CustomLogger import LogMaker


class TestHomePage:
    BASE_URL = ReadConfig.get_base_url()
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()
    log = LogMaker.log_gen()

    SCREENSHOT_DIR = Path.cwd() / "screenshots"
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    def _screenshot_and_fail(self, driver, name, message):
        path = str(self.SCREENSHOT_DIR / name)
        driver.save_screenshot(path)
        self.log.error(f"{message} | Screenshot saved at: {path}")
        pytest.fail(f"{message} Screenshot: {path}")

    # ------------------------------------------------------------------------------------
    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_001(self, setup):
        self.log.info("************** TEST STARTED: test_login_001 **************")

        driver = setup
        self.log.info(f"Opening application URL: {self.BASE_URL}")
        driver.get(self.BASE_URL)

        test_login_page = LoginPage(driver)
        self.log.info("Starting login process for valid credentials...")

        self.log.info(f"Entering username: {self.username}")
        test_login_page.enter_username(self.username)

        self.log.info(f"Entering password")
        test_login_page.enter_password(self.password)

        self.log.info("Clicking login button")
        test_login_page.click_login()

        self.log.info("Verifying landing page...")
        try:
            heading = WebDriverWait(driver, 12).until(
                EC.visibility_of_element_located((By.XPATH, "//h6"))
            ).text

            self.log.info(f"Dashboard heading found: '{heading}'")

            if "dashboard" in heading.lower():
                self.log.info("Successfully logged in and landed on dashboard.")
                assert True
            else:
                self._screenshot_and_fail(
                    driver,
                    "login_unexpected_heading.png",
                    f"Landing heading didn't contain 'dashboard'. Found: '{heading}'"
                )
        except Exception as e:
            self._screenshot_and_fail(driver, "login_error.png", f"Login landing page not found: {e}")

        self.log.info("************** TEST COMPLETED: test_login_001 **************")

    # ------------------------------------------------------------------------------------
    @pytest.mark.smoke
    def test_login_negative_002(self, setup):
        self.log.info("************** TEST STARTED: test_login_negative_002 **************")

        driver = setup
        self.log.info(f"Navigating to: {self.BASE_URL}")
        driver.get(self.BASE_URL)

        test_login_page = LoginPage(driver)
        self.log.info("Entering invalid username and password...")

        test_login_page.enter_username("Rockey")
        test_login_page.enter_password("hungama@123")
        test_login_page.click_login()

        expected_error_message = "Invalid credentials"
        self.log.info("Verifying invalid credential error message...")

        try:
            err_elem = WebDriverWait(driver, 8).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//p[contains(normalize-space(), 'Invalid credentials')]"))
            )

            self.log.info(f"Error message displayed: '{err_elem.text}'")

            if expected_error_message in err_elem.text:
                self.log.info("Negative login test passed.")
                assert True
            else:
                self._screenshot_and_fail(
                    driver,
                    "negative_login_wrong_text.png",
                    f"Error text mismatch. Found: '{err_elem.text}'"
                )
        except Exception as e:
            self._screenshot_and_fail(driver, "negative_login_no_error.png", f"Error message not shown: {e}")

        self.log.info("************** TEST COMPLETED: test_login_negative_002 **************")

    # ------------------------------------------------------------------------------------
    @pytest.mark.smoke
    def test_login_negative_007(self, setup):
        self.log.info("************** TEST STARTED: test_login_negative_007 **************")

        driver = setup
        self.log.info(f"Navigating to: {self.BASE_URL}")
        driver.get(self.BASE_URL)

        login_page = LoginPage(driver)

        self.log.info("Clicking login button with empty username and password...")
        login_page.click_login()

        self.log.info("Checking required field validation messages...")
        try:
            username_err = WebDriverWait(driver, 6).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div/input[@name='username']/parent::div/following-sibling::span"))
            ).text
        except Exception:
            username_err = ""

        try:
            password_err = WebDriverWait(driver, 6).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div/input[@name='password']/parent::div/following-sibling::span"))
            ).text
        except Exception:
            password_err = ""

        self.log.info(f"username_err='{username_err}', password_err='{password_err}'")

        if "Required" in username_err and "Required" in password_err:
            self.log.info("Negative test passed: Required field validation working.")
            assert True
        else:
            self._screenshot_and_fail(
                driver,
                "negative_required_fields.png",
                f"Missing required validation. username_err='{username_err}', password_err='{password_err}'"
            )

        self.log.info("************** TEST COMPLETED: test_login_negative_007 **************")

    # ------------------------------------------------------------------------------------
    @pytest.mark.smoke
    def test_login_ui_elements_presence_008(self, setup):
        self.log.info("************** TEST STARTED: test_login_ui_elements_presence_008 **************")

        driver = setup
        self.log.info(f"Navigating to: {self.BASE_URL}")
        driver.get(self.BASE_URL)

        test_login_page = LoginPage(driver)
        self.log.info("Checking presence of login UI elements...")

        assert test_login_page.is_displayed_login_branding(), "Login Branding is not displayed"
        assert test_login_page.is_displayed_login_logo(), "Login Logo is not displayed"
        assert test_login_page.is_displayed_username_text_field(), "Username field is not displayed"
        assert test_login_page.is_displayed_button_login(), "Login button is not displayed"

        self.log.info("All UI elements on login page are displayed correctly.")

        self.log.info("************** TEST COMPLETED: test_login_ui_elements_presence_008 **************")

    # ------------------------------------------------------------------------------------
    @pytest.mark.smoke
    def test_login_forgot_password_009(self, setup):
        self.log.info("************** TEST STARTED: test_login_forgot_password_009 **************")

        driver = setup
        self.log.info(f"Navigating to: {self.BASE_URL}")
        driver.get(self.BASE_URL)

        forget_login_details = LoginPage(driver)
        self.log.info("Clicking 'Forgot Password'...")

        forget_login_details.click_forgot_password()

        self.log.info(f"Entering username for password reset: {self.username}")
        forget_login_details.enter_username(self.username)

        self.log.info("Clicking reset password button...")
        forget_login_details.click_reset_password()

        try:
            self.log.info("Waiting for password reset confirmation message...")
            success_heading = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h6"))
            ).text

            self.log.info(f"Reset password response heading: '{success_heading}'")

            expected_text = "Reset Password link sent successfully"
            if expected_text in success_heading:
                self.log.info("Forgot password functionality validated successfully.")
                assert True
            else:
                self._screenshot_and_fail(
                    driver,
                    "forgot_password_unexpected.png",
                    f"Unexpected forgot password message: '{success_heading}'"
                )
        except Exception as e:
            self._screenshot_and_fail(
                driver,
                "forgot_password_no_success.png",
                f"Forgot password success message not found: {e}"
            )

        self.log.info("************** TEST COMPLETED: test_login_forgot_password_009 **************")
