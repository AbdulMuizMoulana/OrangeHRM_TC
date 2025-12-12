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


class TestPimContactDetailsPage:
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()
    BASE_URL = ReadConfig.get_base_url()

    SCREENSHOT_DIR = Path.cwd() / "screenshots"
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    def _screenshot_and_fail(self, driver, name, message):
        path = str(self.SCREENSHOT_DIR / name)
        driver.save_screenshot(path)
        pytest.fail(f"{message} Screenshot: {path}")

    @pytest.mark.smoke
    def test_pim_contact_details_006(self, setup):
        driver = setup
        driver.get(self.BASE_URL)

        # Login
        login = LoginPage(driver)
        login.enter_username(self.username)
        login.enter_password(self.password)
        login.click_login()

        # Add employee
        pim = PIMPage(driver)
        pim.click_pim_button()
        pim.click_employee_add_button()
        pim.enter_firstname("John")
        pim.enter_middlename("nitin")
        pim.enter_lastname("Doe")
        pim.enter_employee_id("abc123")
        pim.click_save_button()

        # Contact details
        contact = PIMContactDetailsPage(driver)
        contact.click_contact_details()
        contact.enter_street1("abcd 233")
        contact.enter_city("udupi")
        contact.enter_state("karnataka")
        # contact.select_country("Afghanistan")  # enable if needed
        contact.enter_zip_code("560068")
        contact.enter_mobile_phone_number("8951648603")
        mail = random_string_generator() + "@test.com"
        contact.enter_work_email(mail)
        contact.click_save_button()

        # Wait for success message
        try:
            success_elem = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//p[contains(normalize-space(),'Successfully Updated')]")
                )
            )
            assert "Successfully Updated" in success_elem.text
        except Exception as e:
            self._screenshot_and_fail(driver, "ContactDetails_failed.png",
                                      f"'Successfully Updated' message not found: {e}")
