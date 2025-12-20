import pytest
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.LoginPage import LoginPage
from pages.MyInfoPage import MyInfoPage
from utilities.ReadProperties import ReadConfig

from utilities.CustomLogger import LogMaker


class TestUpdateMyInfo:
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()
    BASE_URL = ReadConfig.get_base_url()
    log = LogMaker.log_gen()

    new_f_name = "akash"
    new_l_name = "lala"

    SCREENSHOT_DIR = Path.cwd() / "screenshots"
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    def _screenshot_and_fail(self, driver, name, message):
        path = str(self.SCREENSHOT_DIR / name)
        driver.save_screenshot(path)
        self.log.error(f"{message} | Screenshot saved at: {path}")
        pytest.fail(f"{message} Screenshot: {path}")

    # ---------------------------------------------------------------------------------------------
    @pytest.mark.smoke
    def test_update_my_info_014(self, setup):
        self.log.info("************** TEST STARTED: test_update_my_info_014 **************")

        driver = setup
        self.log.info(f"Opening application URL: {self.BASE_URL}")
        driver.get(self.BASE_URL)

        # -------------------------------------------
        # Login
        # -------------------------------------------
        self.log.info("Starting login process...")
        login = LoginPage(driver)

        self.log.info(f"Entering username: {self.username}")
        login.enter_username(self.username)

        self.log.info("Entering password.")
        login.enter_password(self.password)

        self.log.info("Clicking login button.")
        login.click_login()

        # -------------------------------------------
        # Update My Info
        # -------------------------------------------
        self.log.info("Navigating to My Info page...")
        myinfo = MyInfoPage(driver)
        myinfo.click_myinfo()

        self.log.info(f"Updating first name to: {self.new_f_name}")
        myinfo.update_firstname(self.new_f_name)

        self.log.info(f"Updating last name to: {self.new_l_name}")
        myinfo.update_lastname(self.new_l_name)

        self.log.info("Updating employee ID to: 4222")
        myinfo.update_emp_id("4222")

        self.log.info("Selecting gender...")
        myinfo.update_gender()

        self.log.info("Saving My Info details...")
        myinfo.click_save_details()

        # -------------------------------------------
        # Verify update success message
        # -------------------------------------------
        self.log.info("Waiting for success confirmation message...")
        try:
            WebDriverWait(driver, 12).until(
                EC.visibility_of_element_located((By.XPATH, "//p[text()='Successfully Updated']"))
            )
            self.log.info("Success message displayed: Successfully Updated")
        except Exception as e:
            self._screenshot_and_fail(
                driver,
                "update_myinfo_no_success.png",
                f"'Successfully Updated' message not found: {e}"
            )

        # -------------------------------------------
        # Refresh and verify updated name
        # -------------------------------------------
        self.log.info("Refreshing page to validate updated name in topbar...")
        try:
            driver.refresh()
            name_elem = WebDriverWait(driver, 12).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[@class='oxd-topbar-header-userarea']//span//p")
                )
            )
            displayed_name = name_elem.text
            self.log.info(f"Name displayed in topbar after update: '{displayed_name}'")

            if self.new_f_name.lower() in displayed_name.lower():
                self.log.info("Updated name verification PASSED.")
                assert True
            else:
                self._screenshot_and_fail(
                    driver,
                    "update_myinfo_name_mismatch.png",
                    f"Expected first name '{self.new_f_name}' in topbar but found '{displayed_name}'"
                )
        except Exception as e:
            self._screenshot_and_fail(
                driver,
                "update_myinfo_name_not_found.png",
                f"Updated name element not found after refresh: {e}"
            )

        self.log.info("************** TEST COMPLETED: test_update_my_info_014 **************")
