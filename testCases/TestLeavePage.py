import time

import pytest
from selenium.webdriver.common.by import By


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

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_apply_leave_010(self, setup):
        driver = setup
        driver.get(self.BASE_URL)
        driver.implicitly_wait(5)
        driver.maximize_window()

        test_login =LoginPage(driver)
        test_login.enter_username(self.ess_username)
        test_login.enter_password(self.ess_password)
        test_login.click_login()


        test_leave_page = LeavePage(driver)
        test_leave_page.click_leave()
        test_leave_page.click_apply()
        test_leave_page.select_leave_type()
        test_leave_page.enter_from_date("2025-20-12")
        time.sleep(3)
        test_leave_page.enter_to_date("2025-20-12")
        time.sleep(3)
        test_leave_page.select_duration()
        time.sleep(3)
        test_leave_page.enter_comment("i needed leave")
        time.sleep(3)
        test_leave_page.click_apply_submit_button()

        success_message = driver.find_element(By.XPATH,"//p[text()='Successfully Saved']")
        if "Successfully Saved" in success_message.text:
            print("Successfully Saved")
            assert True
            driver.close()
        else:
            print("Failed to Saved")
            driver.save_screenshot(".\\screenshots\\applyleave.png")
            driver.close()
            assert False

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_assign_leave_011(self, setup):
        driver = setup
        driver.get(self.BASE_URL)
        driver.maximize_window()
        driver.implicitly_wait(5)

        test_login =LoginPage(driver)
        test_login.enter_username(self.username)
        test_login.enter_password(self.password)
        test_login.click_login()

        test_assign_leave = LeavePage(driver)
        test_assign_leave.click_leave()
        test_assign_leave.click_assign_leave_button()
        test_assign_leave.enter_emp_name(self.emp_name)
        test_assign_leave.enter_from_date("2025-19-12")
        time.sleep(2)
        test_assign_leave.enter_to_date("2025-19-12")
        time.sleep(2)
        test_assign_leave.select_assign_leave_type()
        time.sleep(2)
        test_assign_leave.select_duration()
        time.sleep(2)
        test_assign_leave.enter_comment("TEST_assign leave i needed leave")
        time.sleep(3)
        test_assign_leave.click_assign_submit()

        success_message= driver.find_element(By.XPATH,"//p[text()='Successfully Saved']")
        if "Successfully Saved" in success_message.text:
            print("Successfully Saved")
            assert True
            driver.close()
        else:
            print("Failed to Saved")
            driver.save_screenshot(".\\screenshots\\applyleave.png")
            driver.close()
            assert False



