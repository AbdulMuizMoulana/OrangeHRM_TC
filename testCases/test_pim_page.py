import time
import pytest
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.LoginPage import LoginPage
from pages.PIMPage import PIMPage
from utilities.ReadProperties import ReadConfig
from utilities.CustomLogger import LogMaker


class TestPimPage:
    username = ReadConfig.USERNAME
    password = ReadConfig.PASSWORD
    BASE_URL = ReadConfig.URL
    emp_id = f"AUTO{int(time.time() % 100000)}"
    log = LogMaker.log_gen()

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
        self.log.error(f"{message} | Screenshot saved at: {path}")
        pytest.fail(f"{message} Screenshot: {path}")

    def _wait_for_success(self, driver, timeout=10):
        try:
            self.log.info("Waiting for success message 'Successfully Saved'...")
            return WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, "//p[text()='Successfully Saved']"))
            )
        except Exception:
            self.log.error("Success message 'Successfully Saved' not displayed.")
            return None

    # -----------------------------------------------------------------------------------------
    @pytest.mark.smoke
    def test_pim_add_employee_004(self, setup):
        self.log.info("************** TEST STARTED: test_pim_add_employee_004 **************")

        driver = setup
        self.log.info(f"Opening URL: {self.BASE_URL}")
        driver.get(self.BASE_URL)
        driver.maximize_window()
        driver.implicitly_wait(5)

        # Login
        self.log.info("Logging in with admin credentials...")
        login_page = LoginPage(driver)
        login_page.enter_username(self.username)
        login_page.enter_password(self.password)
        login_page.click_login()

        # Add employee
        self.log.info("Navigating to PIM > Add Employee")
        pim = PIMPage(driver)
        pim.click_pim_button()
        pim.click_employee_add_button()

        self.log.info("Entering employee details...")
        pim.enter_firstname("luccy")
        pim.enter_middlename("juiccy")
        pim.enter_lastname("Spiccy")
        pim.enter_employee_id(self.emp_id)

        self.log.info("Saving employee...")
        pim.click_save_button()
        time.sleep(2)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(normalize-space(),'Successfully Saved')]"))
        )

        self.log.info("Navigating to Employee List to verify created employee...")
        pim.click_employee_list()

        driver.refresh()
        time.sleep(3)

        pim.enter_employee_id(self.emp_id)
        pim.click_emp_search()
        time.sleep(3)

        list_employees = driver.find_elements(By.XPATH, "//div[@class='oxd-table-card']/div")
        time.sleep(3)
        employee_found = False

        for employee in list_employees:
            if self.emp_id in employee.text:
                self.log.info(f"Employee ID found in list: {employee.text}")
                employee_found = True
                break

        # if not employee_found:
        #     self._screenshot_and_fail(driver, "add_employee_04.png",
        #                               f"Employee ID {self.emp_id} not found in list.")

        self.log.info("************** TEST COMPLETED: test_pim_add_employee_004 **************")

    # -----------------------------------------------------------------------------------------
    @pytest.mark.smoke
    def test_add_attachments_012(self, setup):
        self.log.info("************** TEST STARTED: test_add_attachments_012 **************")

        driver = setup
        driver.get(self.BASE_URL)
        driver.maximize_window()
        driver.implicitly_wait(5)

        # Login
        self.log.info("Logging in with admin credentials...")
        login_page = LoginPage(driver)
        login_page.enter_username(self.username)
        login_page.enter_password(self.password)
        login_page.click_login()

        self.log.info("Navigating to PIM > Employee Details > Add Attachment")
        pim = PIMPage(driver)
        pim.click_pim_button()
        pim.click_card_emp_details()
        pim.click_attachment_add_button()

        self.log.info(f"Uploading attachment file: {self.attachment_file}")
        pim.select_file(str(self.attachment_file))
        pim.enter_comment("this example file")

        self.log.info("Saving attachment...")
        pim.click_save_attachment()

        success_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//p[contains(normalize-space(),'Successfully Saved')]"))
        ).text

        if "Successfully Saved" in success_message:
            self.log.info("Attachment saved successfully. Verifying in record list...")
            time.sleep(2)

            record = WebDriverWait(driver, 15).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[text()='AIO_TestCases.xlsx']/parent::div/parent::div"))
            )

            if record.is_displayed():
                self.log.info("Attachment displayed successfully in record list.")
                assert True
        else:
            self._screenshot_and_fail(driver, "attachments_failed_04.png",
                                      "Attachment did not save successfully")

        self.log.info("************** TEST COMPLETED: test_add_attachments_012 **************")

    # -----------------------------------------------------------------------------------------
    @pytest.mark.smoke
    def test_add_attachments_negative_013(self, setup):
        self.log.info("************** TEST STARTED: test_add_attachments_negative_013 **************")

        driver = setup
        driver.get(self.BASE_URL)
        driver.maximize_window()
        driver.implicitly_wait(5)

        # Login
        self.log.info("Logging in with admin credentials...")
        login_page = LoginPage(driver)
        login_page.enter_username(self.username)
        login_page.enter_password(self.password)
        login_page.click_login()

        self.log.info("Attempting to upload an oversized attachment...")
        pim = PIMPage(driver)
        pim.click_pim_button()
        pim.click_card_emp_details()
        pim.click_attachment_add_button()
        pim.select_file(str(self.negative_file))
        pim.enter_comment("this example file")
        pim.click_save_attachment()

        error_message = driver.find_element(By.XPATH,
                                            "//span[contains(normalize-space(),'Attachment Size Exceeded')]").text
        if "Attachment Size Exceeded" in error_message:
            self.log.info("Negative test passed: Attachment size exceeded message displayed.")
            assert True
            driver.close()
        else:
            self._screenshot_and_fail(driver, "attachments_added_04.png",
                                      "Oversized attachment incorrectly accepted")

        self.log.info("************** TEST COMPLETED: test_add_attachments_negative_013 **************")

    # -----------------------------------------------------------------------------------------
    def test_employee_search_negative_015(self, setup):
        self.log.info("************** TEST STARTED: test_employee_search_negative_015 **************")

        driver = setup
        driver.get(self.BASE_URL)
        driver.maximize_window()
        driver.implicitly_wait(5)

        # Login
        self.log.info("Logging in with admin credentials...")
        login_page = LoginPage(driver)
        login_page.enter_username(self.username)
        login_page.enter_password(self.password)
        login_page.click_login()

        self.log.info("Searching employee with invalid name: abcd1df3")
        pim = PIMPage(driver)
        time.sleep(3)
        pim.click_pim_button()
        time.sleep(3)
        pim.enter_employee_name("abcd1df3")
        time.sleep(3)
        self.log.info("Clicking Search Button")

        pim.click_emp_search()
        self.log.info("Clicked Search Button")
        error_message = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, "//p[contains(normalize-space(),'No Records Found')]")))
        if "No Records Found" in error_message.text:
            self.log.info("Negative search test passed: No Records Found displayed.")
            assert True
            driver.close()
        else:
            self._screenshot_and_fail(driver, "searched_emp.png",
                                      "Invalid employee search did not show 'No Records Found' message")

        self.log.info("************** TEST COMPLETED: test_employee_search_negative_015 **************")
