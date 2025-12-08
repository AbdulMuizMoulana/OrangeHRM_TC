import pytest
from selenium.webdriver.common.by import By

from pages.LoginPage import LoginPage
from pages.PIMContactDetailsPage import PIMContactDetailsPage
from pages.PIMPage import PIMPage
from utilities.ReadProperties import ReadConfig
from utilities.RandomString import random_string_generator


class TestPimContactDetailsPage:
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()
    BASE_URL = ReadConfig.get_base_url()

    @pytest.mark.smoke
    def test_pim_contact_details_006(self, setup):
        driver = setup
        driver.get(self.BASE_URL)
        driver.maximize_window()
        driver.implicitly_wait(5)

        test_login_page = LoginPage(driver)
        test_login_page.enter_username(self.username)
        test_login_page.enter_password(self.password)
        test_login_page.click_login()

        test_pim_page = PIMPage(driver)
        test_pim_page.click_pim_button()
        test_pim_page.click_employee_add_button()
        test_pim_page.enter_firstname("John")
        test_pim_page.enter_middlename("nitin")
        test_pim_page.enter_lastname("Doe")
        test_pim_page.enter_employee_id("abc123")
        test_pim_page.click_save_button()

        test_pip_contact_details = PIMContactDetailsPage(driver)
        test_pip_contact_details.click_contact_details()
        test_pip_contact_details.enter_street1("abcd 233")
        test_pip_contact_details.enter_city("udupi")
        test_pip_contact_details.enter_state("karnataka")
        # test_pip_contact_details.select_country("Afghanistan")
        test_pip_contact_details.enter_zip_code("560068")
        test_pip_contact_details.enter_mobile_phone_number("8951648603")
        mail = random_string_generator()+"@test.com"
        test_pip_contact_details.enter_work_email(mail)
        test_pip_contact_details.click_save_button()

        success_message = driver.find_element(By.XPATH, "//p[contains(normalize-space(),'Successfully Updated')]")
        if "Successfully Updated" in success_message.text:
            print("Successfully Updated")
            assert True
            driver.close()
        else:
            driver.save_screenshot(".\\screenshots\\ContactDetails.png")
            driver.close()
            assert False
