import os
import time
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pytest

from pages.LeavePage import LeavePage
from pages.LoginPage import LoginPage
from utilities.ReadProperties import ReadConfig


class TestLeavePage:
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()

    emp_name = "abdul"
    ess_username = ReadConfig.get_ess_username()
    ess_password = ReadConfig.get_ess_password()
    BASE_URL = ReadConfig.get_base_url()

    SCREENSHOT_DIR = Path.cwd() / "screenshots"
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    # def _wait_for_success(self, driver, timeout=10):
    #     """Wait for the standard 'Successfully Saved' message and return the element (or None)."""
    #     try:
    #         return WebDriverWait(driver, timeout).until(
    #             EC.visibility_of_element_located((By.XPATH, "//p[text()='Successfully Saved']"))
    #         )
    #     except Exception:
    #         return None

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_apply_leave_010(self, setup):
        driver = setup
        driver.get(self.BASE_URL)

        # login as ESS user
        login = LoginPage(driver)
        login.enter_username(self.ess_username)
        login.enter_password(self.ess_password)
        login.click_login()

        # apply leave
        leave = LeavePage(driver)
        leave.click_leave()
        leave.click_apply()
        leave.select_leave_type()
        leave.enter_from_date("2025-08-12")
        leave.enter_to_date("2025-08-12")
        leave.select_duration()
        leave.enter_comment("i needed leave")
        leave.click_apply_submit_button()

        # Assert success
        success_elem = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//p[text()='Successfully Saved']")))
        if "Successfully Saved" in success_elem.text:
            assert True
        else:
            screenshot = str(self.SCREENSHOT_DIR / "applyleave_apply_010.png")
            driver.save_screenshot(screenshot)
            pytest.fail(f"'Successfully Saved' message not found. Screenshot: {screenshot}")

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_assign_leave_011(self, setup):
        driver = setup
        driver.get(self.BASE_URL)

        # login as admin (or normal user that can assign)
        login = LoginPage(driver)
        login.enter_username(self.username)
        login.enter_password(self.password)
        login.click_login()

        # assign leave
        assign = LeavePage(driver)
        time.sleep(3)
        assign.click_leave()
        time.sleep(3)
        assign.click_assign_leave_button()
        assign.enter_emp_name(self.emp_name)

        assign.enter_from_date("2025-09-12")
        assign.enter_to_date("2025-09-12")
        assign.select_assign_leave_type()
        assign.select_duration()
        assign.enter_comment("TEST_assign leave i needed leave")
        assign.click_assign_submit()

        # Assert success
        success_elem = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//p[text()='Successfully Saved']"))).text
        if "Successfully Saved" in success_elem:
            assert True
        else:
            screenshot = str(self.SCREENSHOT_DIR / "Assignleave_apply_010.png")
            driver.save_screenshot(screenshot)
            pytest.fail(f"'Successfully Saved' message not found. Screenshot: {screenshot}")