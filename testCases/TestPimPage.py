import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.LoginPage import LoginPage
from pages.PIMPage import PIMPage
from utilities.ReadProperties import ReadConfig
from pathlib import Path


class TestPimPage:
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()
    BASE_URL = ReadConfig.get_base_url()
    emp_id = f"AUTO{int(time.time() % 100000)}"

    ess_username = ReadConfig.get_ess_username()
    ess_password = ReadConfig.get_ess_password()

    PROJECT_ROOT = Path(__file__).resolve().parents[1]

    attachment_file = PROJECT_ROOT / "AIO_TestCases.xlsx"
    negative_file = PROJECT_ROOT / "Screen Recording 2025-11-07 120303.mp4"

    SCREENSHOT_DIR = Path.cwd() / "screenshots"
    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

    def _screenshot_and_fail(self, driver, name, message):
        path = str(self.SCREENSHOT_DIR / name)
        driver.save_screenshot(path)
        pytest.fail(f"{message} Screenshot: {path}")

    def _wait_for_success(self, driver, timeout=10):
        """Wait for the standard 'Successfully Saved' message and return the element (or None)."""
        try:
            return WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, "//p[text()='Successfully Saved']"))
            )
        except Exception:
            return None

    @pytest.mark.smoke
    def test_pim_add_employee_004(self, setup):
        driver = setup
        driver.get(self.BASE_URL)
        driver.maximize_window()
        driver.implicitly_wait(5)

        test_login_page = LoginPage(driver)
        test_login_page.enter_username(self.username)
        test_login_page.enter_password(self.password)
        test_login_page.click_login()

        test_pim_add_employee = PIMPage(driver)
        test_pim_add_employee.click_pim_button()
        test_pim_add_employee.click_employee_add_button()
        test_pim_add_employee.enter_firstname("luccy")
        test_pim_add_employee.enter_middlename("juiccy")
        test_pim_add_employee.enter_lastname("Spiccy")
        test_pim_add_employee.enter_employee_id(self.emp_id)
        test_pim_add_employee.click_save_button()
        time.sleep(2)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(normalize-space(),'Successfully Saved')]")))
        time.sleep(5)

        test_pim_add_employee.click_employee_list()
        driver.refresh()
        time.sleep(3)

        test_pim_add_employee.enter_employee_id(self.emp_id)
        test_pim_add_employee.click_emp_search()
        time.sleep(3)
        list_employees = driver.find_elements(By.XPATH, "//div[@class='oxd-table-card']/div")

        employee_found = False

        for employee in list_employees:
            if self.emp_id in employee.text:
                print(f"ID is present: {employee.text}")
                employee_found = True
                break
        # #
        # if not employee_found:
        #     screenshot = str(self.SCREENSHOT_DIR / "add_employee_04.png")
        #     driver.save_screenshot(screenshot)
        #     pytest.fail(f"Employee ID {self.emp_id} not found. Screenshot: {screenshot}")

    @pytest.mark.smoke
    def test_add_attachments_012(self, setup):
        driver = setup
        driver.get(self.BASE_URL)
        driver.maximize_window()
        driver.implicitly_wait(5)

        login_page = LoginPage(driver)
        login_page.enter_username(self.username)
        login_page.enter_password(self.password)
        login_page.click_login()

        test_add_attachments = PIMPage(driver)
        test_add_attachments.click_pim_button()
        test_add_attachments.click_card_emp_details()
        test_add_attachments.click_attachment_add_button()
        test_add_attachments.select_file(str(self.attachment_file))
        test_add_attachments.enter_comment("this example file")
        test_add_attachments.click_save_attachment()
        success_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//p[contains(normalize-space(),'Successfully Saved')]"))).text
        # success_message = driver.find_element(By.XPATH, "//p[contains(normalize-space(),'Successfully Saved')]").text
        if "Successfully Saved" in success_message:
            print("Successfully Saved")
            time.sleep(2)
            record = WebDriverWait(driver, 15).until(EC.visibility_of_element_located(
                (By.XPATH, "//div[text()='AIO_TestCases.xlsx']/parent::div/parent::div")))
            if record.is_displayed():
                print("successfully displayed record in list")
                assert True
        else:
            print("Failed to Saved")
            screenshot = str(self.SCREENSHOT_DIR / "attachments_failed_04.png")
            driver.save_screenshot(screenshot)
            pytest.fail(f" not found. Screenshot: {screenshot}")

    @pytest.mark.smoke
    def test_add_attachments_negative_013(self, setup):
        driver = setup
        driver.get(self.BASE_URL)
        driver.maximize_window()
        driver.implicitly_wait(5)

        login_page = LoginPage(driver)
        login_page.enter_username(self.username)
        login_page.enter_password(self.password)
        login_page.click_login()

        test_add_attachments = PIMPage(driver)
        test_add_attachments.click_pim_button()
        test_add_attachments.click_card_emp_details()
        test_add_attachments.click_attachment_add_button()
        test_add_attachments.select_file(str(self.negative_file))
        test_add_attachments.enter_comment("this example file")
        test_add_attachments.click_save_attachment()

        error_message = driver.find_element(By.XPATH,
                                            "//span[contains(normalize-space(),'Attachment Size Exceeded')]").text
        if "Attachment Size Exceeded" in error_message:
            print("displaying error message as Attachment \"Size Exceeded\"")
            assert True
            driver.close()
        else:
            print("Failed not displaying error message")
            screenshot = str(self.SCREENSHOT_DIR / "attachments_added_04.png")
            driver.save_screenshot(screenshot)
            pytest.fail(f" attachment added . Screenshot: {screenshot}")

    def test_employee_search_negative_015(self, setup):
        driver = setup
        driver.get(self.BASE_URL)
        driver.maximize_window()
        driver.implicitly_wait(5)

        login_page = LoginPage(driver)
        login_page.enter_username(self.username)
        login_page.enter_password(self.password)
        login_page.click_login()

        test_employee_search = PIMPage(driver)
        time.sleep(3)
        test_employee_search.click_pim_button()
        time.sleep(3)
        test_employee_search.enter_employee_name("abcd1df3")
        test_employee_search.click_emp_search()

        error_message = driver.find_element(By.XPATH, "//p[contains(normalize-space(),'No Records Found')]")
        if "No Records Found" in error_message.text:
            print("displaying error message as No Records Found")
            assert True
            driver.close()
        else:
            print("Failed not displaying error message")
            screenshot = str(self.SCREENSHOT_DIR / "searched_emp.png")
            driver.save_screenshot(screenshot)
            pytest.fail(f" not found. Screenshot: {screenshot}")
