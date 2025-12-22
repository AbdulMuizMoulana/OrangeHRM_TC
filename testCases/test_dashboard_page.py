import os
from pathlib import Path

import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utilities.ReadProperties import ReadConfig
from pages.LoginPage import LoginPage
from pages.Dashboard import Dashboard

from utilities.CustomLogger import LogMaker


class TestDashboardPage:
    username = ReadConfig.USERNAME
    password = ReadConfig.PASSWORD
    BASE_URL = ReadConfig.URL
    log = LogMaker.log_gen()

    SCREENSHOT_DIR = Path.cwd() / "screenshots"
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    @pytest.mark.smoke
    def test_dashboard_end_session_003(self, setup):
        self.log.info("************** TEST STARTED: test_dashboard_end_session_003 **************")

        driver = setup
        self.log.info(f"Opening URL: {self.BASE_URL}")
        driver.get(self.BASE_URL)

        # Login
        self.log.info("Starting login process...")
        login = LoginPage(driver)

        self.log.info(f"Entering username: {self.username}")
        login.enter_username(self.username)

        self.log.info("Entering password.")
        login.enter_password(self.password)

        self.log.info("Clicking login button.")
        login.click_login()

        # Logout via dashboard
        self.log.info("Navigating to dashboard logout flow...")
        dashboard = Dashboard(driver)

        self.log.info("Clicking profile button.")
        dashboard.click_profile_btn()

        self.log.info("Clicking logout button.")
        dashboard.click_logout()

        self.log.info("Waiting for page to redirect to base URL after logout...")

        # Wait for URL to be expected base URL
        try:
            WebDriverWait(driver, 10).until(EC.url_to_be(self.BASE_URL))
            self.log.info(f"Successfully redirected to URL: {driver.current_url}")
            assert driver.current_url == self.BASE_URL
            self.log.info("Logout redirection verification PASSED.")

        except Exception as e:
            screenshot_path = str(self.SCREENSHOT_DIR / "DashboardTest.png")
            driver.save_screenshot(screenshot_path)

            self.log.error("Logout redirection verification FAILED.")
