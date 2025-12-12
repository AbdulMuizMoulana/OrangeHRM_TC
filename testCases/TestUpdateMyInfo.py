import pytest
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.LoginPage import LoginPage
from pages.MyInfoPage import MyInfoPage
from utilities.ReadProperties import ReadConfig


class TestUpdateMyInfo:
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()
    BASE_URL = ReadConfig.get_base_url()

    new_f_name = "akash"
    new_l_name = "lala"

    SCREENSHOT_DIR = Path.cwd() / "screenshots"
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    def _screenshot_and_fail(self, driver, name, message):
        path = str(self.SCREENSHOT_DIR / name)
        driver.save_screenshot(path)
        pytest.fail(f"{message} Screenshot: {path}")

    @pytest.mark.smoke
    def test_update_my_info_014(self, setup):
        driver = setup
        driver.get(self.BASE_URL)

        # Login
        login = LoginPage(driver)
        login.enter_username(self.username)
        login.enter_password(self.password)
        login.click_login()

        # Update My Info
        myinfo = MyInfoPage(driver)
        myinfo.click_myinfo()
        myinfo.update_firstname(self.new_f_name)
        myinfo.update_lastname(self.new_l_name)
        myinfo.update_emp_id("4222")
        myinfo.update_gender()
        myinfo.click_save_details()

        # Wait for success toast/message
        try:
            WebDriverWait(driver, 12).until(
                EC.visibility_of_element_located((By.XPATH, "//p[text()='Successfully Updated']"))
            )
        except Exception as e:
            self._screenshot_and_fail(driver, "update_myinfo_no_success.png",
                                      f"'Successfully Updated' message not found: {e}")

        # Refresh and verify updated name appears in topbar/user area
        # driver.refresh()
        try:
            driver.refresh()
            name_elem = WebDriverWait(driver, 12).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='oxd-topbar-header-userarea']//span//p"))
            )
            displayed_name = name_elem.text
            if self.new_f_name.lower() in displayed_name.lower():
                assert True
            else:
                self._screenshot_and_fail(driver, "update_myinfo_name_mismatch.png",
                                          f"Expected first name '{self.new_f_name}' in '{displayed_name}'")
        except Exception as e:
            self._screenshot_and_fail(driver, "update_myinfo_name_not_found.png",
                                      f"Updated name element not found after refresh: {e}")
