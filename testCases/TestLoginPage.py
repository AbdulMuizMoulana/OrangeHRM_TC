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
    BASE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()
    log = LogMaker.log_gen()

    SCREENSHOT_DIR = Path.cwd() / "screenshots"
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    def _screenshot_and_fail(self, driver, name, message):
        path = str(self.SCREENSHOT_DIR / name)
        driver.save_screenshot(path)
        pytest.fail(f"{message} Screenshot: {path}")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_001(self, setup):
        driver = setup
        self.log.info("************** Launching the web application ***************")
        driver.get(self.BASE_URL)

        test_login_page = LoginPage(driver)
        self.log.info("************** starting logging in **************")
        test_login_page.enter_username(self.username)
        test_login_page.enter_password(self.password)
        test_login_page.click_login()

        self.log.info("************** verifying the landing page **************")
        try:
            # wait for the h6 element which contains the dashboard heading
            heading = WebDriverWait(driver, 12).until(
                EC.visibility_of_element_located((By.XPATH, "//h6"))
            ).text
            if "dashboard" in heading.lower():
                self.log.info(" ************** Successfully logged in to expected page **************")
                assert True
            else:
                self._screenshot_and_fail(driver, "login_unexpected_heading.png",
                                          f"Landing heading didn't contain 'dashboard'. Found: '{heading}'")
        except Exception as e:
            self._screenshot_and_fail(driver, "login_error.png", f"Login landing page not found: {e}")

    @pytest.mark.smoke
    def test_login_negative_002(self, setup):
        driver = setup
        driver.get(self.BASE_URL)

        test_login_page = LoginPage(driver)
        test_login_page.enter_username("Rockey")
        test_login_page.enter_password("hungama@123")
        test_login_page.click_login()

        expected_error_message = "Invalid credentials"
        try:
            err_elem = WebDriverWait(driver, 8).until(
                EC.visibility_of_element_located((By.XPATH, "//p[contains(normalize-space(), 'Invalid credentials')]"))
            )
            if expected_error_message in err_elem.text:
                assert True
            else:
                self._screenshot_and_fail(driver, "negative_login_wrong_text.png",
                                          f"Error text mismatch. Found: '{err_elem.text}'")
        except Exception as e:
            self._screenshot_and_fail(driver, "negative_login_no_error.png", f"Error message not shown: {e}")

    @pytest.mark.smoke
    def test_login_negative_007(self, setup):
        driver = setup
        driver.get(self.BASE_URL)

        login_page = LoginPage(driver)
        # click login with empty fields
        login_page.click_login()

        try:
            username_err = WebDriverWait(driver, 6).until(
                EC.visibility_of_element_located((By.XPATH, "//div/input[@name='username']/parent::div/following-sibling::span"))
            ).text
        except Exception:
            username_err = ""

        try:
            password_err = WebDriverWait(driver, 6).until(
                EC.visibility_of_element_located((By.XPATH, "//div/input[@name='password']/parent::div/following-sibling::span"))
            ).text
        except Exception:
            password_err = ""

        if "Required" in username_err and "Required" in password_err:
            self.log.info(f"negative Test passed: username_err='{username_err}', password_err='{password_err}'")
            assert True
        else:
            self._screenshot_and_fail(driver, "negative_required_fields.png",
                                      f"Required validation messages missing. username_err='{username_err}', password_err='{password_err}'")

    @pytest.mark.smoke
    def test_login_ui_elements_presence_008(self, setup):
        driver = setup
        driver.get(self.BASE_URL)

        test_login_page = LoginPage(driver)
        assert test_login_page.is_displayed_login_branding(), "Login Branding is not displayed"
        assert test_login_page.is_displayed_login_logo(), "Login Logo is not displayed"
        assert test_login_page.is_displayed_username_text_field(), "Login Text Field is not displayed"
        assert test_login_page.is_displayed_button_login(), "Login Button is not displayed"

    @pytest.mark.smoke
    def test_login_forgot_password_009(self, setup):
        driver = setup
        driver.get(self.BASE_URL)

        forget_login_details = LoginPage(driver)
        forget_login_details.click_forgot_password()
        forget_login_details.enter_username(self.username)
        forget_login_details.click_reset_password()

        try:
            # The page shows a heading/text on success — wait for it
            success_heading = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h6"))
            ).text
            expected_text = "Reset Password link sent successfully"
            if expected_text in success_heading:
                assert True
            else:
                self._screenshot_and_fail(driver, "forgot_password_unexpected.png",
                                          f"Forgot password success text mismatch: '{success_heading}'")
        except Exception as e:
            self._screenshot_and_fail(driver, "forgot_password_no_success.png", f"Forgot password success message not found: {e}")
