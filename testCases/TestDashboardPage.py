import os
from pathlib import Path

import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utilities.ReadProperties import ReadConfig
from pages.LoginPage import LoginPage
from pages.Dashboard import Dashboard


class TestDashboardPage:
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()
    BASE_URL = ReadConfig.get_base_url()

    SCREENSHOT_DIR = Path.cwd() / "screenshots"
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    @pytest.mark.smoke
    def test_dashboard_end_session_003(self, setup):
        driver = setup
        driver.get(self.BASE_URL)

        # Login
        login = LoginPage(driver)
        login.enter_username(self.username)
        login.enter_password(self.password)
        login.click_login()

        # Logout via dashboard
        dashboard = Dashboard(driver)
        dashboard.click_profile_btn()
        dashboard.click_logout()

        # Wait for the URL to become the expected base URL (or login page URL)
        try:
            WebDriverWait(driver, 10).until(EC.url_to_be(self.BASE_URL))
            assert driver.current_url == self.BASE_URL
        except Exception:
            screenshot_path = str(self.SCREENSHOT_DIR / "DashboardTest.png")
            driver.save_screenshot(screenshot_path)
            pytest.fail(f"Logout did not redirect to expected URL. Screenshot: {screenshot_path}")
