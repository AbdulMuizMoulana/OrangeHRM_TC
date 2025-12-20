import time
import pytest
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.LoginPage import LoginPage
from pages.PIMContactDetailsPage import PIMContactDetailsPage
from pages.PIMPage import PIMPage
from utilities.ReadProperties import ReadConfig
from utilities.RandomString import random_string_generator
from utilities.CustomLogger import LogMaker


class TestPimContactDetailsPage:
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()
    BASE_URL = ReadConfig.get_base_url()
    log = LogMaker.log_gen()

    SCREENSHOT_DIR = Path.cwd() / "screenshots"
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    def _screenshot_and_fail(self, driver, name, message):
        path = str(self.SCREENSHOT_DIR / name)
        driver.save_screenshot(path)
        self.log.error(f"{message} | Screenshot saved at: {path}")
        pytest.fail(f"{message} Screenshot: {path}")

    @pytest.mark.smoke
    def test_pim_contact_details_006(self, setup):
        self.log.info("************** TEST STARTED: test_pim_contact_details_006 **************")

        driver = setup
        self.log.info(f"Opening URL: {self.BASE_URL}")
        driver.get(self.BASE_URL)

        # ---------------------------------
        # Login
        # ---------------------------------
        self.log.info("Starting login process...")
        login = LoginPage(driver)

        self.log.info(f"Entering username: {self.username}")
        login.enter_username(self.username)

        self.log.info("Entering password.")
        login.enter_password(self.password)

        self.log.info("Clicking login button.")
        login.click_login()

        # ---------------------------------
        # Add Employee
        # ---------------------------------
        self.log.info("Navigating to PIM module to add a new employee...")
        pim = PIMPage(driver)

        self.log.info("Clicking PIM button.")
        pim.click_pim_button()

        self.log.info("Clicking Add Employee button.")
        pim.click_employee_add_button()

        self.log.info("Entering Employee First Name: John")
        pim.enter_firstname("John")

        self.log.info("Entering Employee Middle Name: nitin")
        pim.enter_middlename("nitin")

        self.log.info("Entering Employee Last Name: Doe")
        pim.enter_lastname("Doe")

        self.log.info("Entering Employee id")
        pim.enter_employee_id("gojo331")

        self.log.info("Saving new employee...")
        pim.click_save_button()
        time.sleep(3)

        # ---------------------------------
        # Update Contact Details
        # ---------------------------------
        self.log.info("Navigating to Contact Details section...")
        contact = PIMContactDetailsPage(driver)

        self.log.info("Clicking Contact Details tab.")
        contact.click_contact_details()

        self.log.info("Entering Street 1: abcd 233")
        contact.enter_street1("abcd 233")

        self.log.info("Entering City: udupi")
        contact.enter_city("udupi")

        self.log.info("Entering State: karnataka")
        contact.enter_state("karnataka")

        self.log.info("Entering Zip Code: 560068")
        contact.enter_zip_code("560068")

        self.log.info("Entering Mobile Number: 8951648603")
        contact.enter_mobile_phone_number("8951648603")

        mail = random_string_generator() + "@test.com"
        self.log.info(f"Entering Work Email: {mail}")
        contact.enter_work_email(mail)

        self.log.info("Saving contact details...")
        contact.click_save_button()

        # ---------------------------------
        # Assertion
        # ---------------------------------
        self.log.info("Waiting for success message: 'Successfully Updated' ...")
        try:
            success_elem = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//p[contains(normalize-space(),'Successfully Updated')]")
                )
            )

            self.log.info(f"Success message displayed: {success_elem.text}")

            assert "Successfully Updated" in success_elem.text
            self.log.info("Contact details updated successfully.")

        except Exception as e:
            self._screenshot_and_fail(
                driver,
                "ContactDetails_failed.png",
                f"'Successfully Updated' message not found: {e}"
            )

        self.log.info("************** TEST COMPLETED: test_pim_contact_details_006 **************")
