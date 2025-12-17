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
from utilities.CustomLogger import LogMaker


class TestLeavePage:
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()
    log = LogMaker.log_gen()

    emp_name = "abdul"
    ess_username = ReadConfig.get_ess_username()
    ess_password = ReadConfig.get_ess_password()
    BASE_URL = ReadConfig.get_base_url()

    SCREENSHOT_DIR = Path.cwd() / "screenshots"
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_apply_leave_010(self, setup):
        self.log.info("************** TEST STARTED: test_apply_leave_010 **************")

        driver = setup
        self.log.info(f"Opening application URL: {self.BASE_URL}")
        driver.get(self.BASE_URL)

        # Login as ESS user
        self.log.info("Initiating ESS user login...")
        login = LoginPage(driver)

        self.log.info(f"Entering ESS username: {self.ess_username}")
        login.enter_username(self.ess_username)

        self.log.info("Entering ESS password.")
        login.enter_password(self.ess_password)

        self.log.info("Clicking login button.")
        login.click_login()

        # Apply leave
        self.log.info("Navigating to Leave > Apply section.")
        leave = LeavePage(driver)

        self.log.info("Clicking Leave menu.")
        leave.click_leave()

        self.log.info("Clicking Apply leave option.")
        leave.click_apply()

        self.log.info("Selecting leave type.")
        leave.select_leave_type()

        self.log.info("Entering From Date")
        leave.enter_from_date("2025-05-12")

        leave.enter_to_date("2025-05-12")

        self.log.info("Selecting duration.")
        leave.select_duration()

        self.log.info("Entering comment.")
        leave.enter_comment("i needed leave")

        self.log.info("Submitting leave application.")
        leave.click_apply_submit_button()

        # Assert success
        self.log.info("Waiting for success message...")
        try:
            success_elem = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//p[text()='Successfully Saved']"))
            )
            self.log.info("Success message displayed: 'Successfully Saved'")
            assert True

        except Exception as e:
            screenshot = str(self.SCREENSHOT_DIR / "applyleave_apply_010.png")
            driver.save_screenshot(screenshot)

            self.log.error("Failed to validate success message for leave apply.")
            self.log.error(f"Screenshot saved at: {screenshot}")
            self.log.exception(e)

            pytest.fail(f"'Successfully Saved' message not found. Screenshot: {screenshot}")

        self.log.info("************** TEST COMPLETED: test_apply_leave_010 **************")


    @pytest.mark.smoke
    @pytest.mark.regression
    def test_assign_leave_011(self, setup):
        self.log.info("************** TEST STARTED: test_assign_leave_011 **************")

        driver = setup
        self.log.info(f"Opening URL: {self.BASE_URL}")
        driver.get(self.BASE_URL)

        # login as admin
        self.log.info("Initiating Admin login...")
        login = LoginPage(driver)

        self.log.info(f"Entering Admin username: {self.username}")
        login.enter_username(self.username)

        self.log.info("Entering Admin password.")
        login.enter_password(self.password)

        self.log.info("Clicking login button.")
        login.click_login()

        # Assign leave
        self.log.info("Navigating to Leave > Assign Leave section.")
        assign = LeavePage(driver)

        self.log.info("Clicking Leave menu.")
        time.sleep(3)
        assign.click_leave()

        self.log.info("Clicking Assign Leave option.")
        time.sleep(3)
        assign.click_assign_leave_button()

        self.log.info(f"Entering employee name for leave assignment: {self.emp_name}")
        assign.enter_emp_name(self.emp_name)

        self.log.info("Entering From Date")
        assign.enter_from_date("2025-18-12")
        assign.enter_to_date("2025-18-12")

        self.log.info("Selecting assign leave type.")
        assign.select_assign_leave_type()

        self.log.info("Selecting duration.")
        assign.select_duration()

        self.log.info("Entering comment for assigned leave.")
        assign.enter_comment("TEST_assign leave i needed leave")

        self.log.info("Submitting assigned leave request.")
        assign.click_assign_submit()

        # Assert success
        self.log.info("Waiting for success message...")
        try:
            success_elem = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//p[text()='Successfully Saved']"))
            ).text

            self.log.info("Success message displayed: 'Successfully Saved'")
            assert True

        except Exception as e:
            screenshot = str(self.SCREENSHOT_DIR / "Assignleave_apply_010.png")
            driver.save_screenshot(screenshot)

            self.log.error("Failed to validate success message for assigned leave.")
            self.log.error(f"Screenshot saved at: {screenshot}")
            self.log.exception(e)

            pytest.fail(f"'Successfully Saved' message not found. Screenshot: {screenshot}")

        self.log.info("************** TEST COMPLETED: test_assign_leave_011 **************")
