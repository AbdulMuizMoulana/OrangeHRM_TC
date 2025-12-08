import pytest
from selenium.webdriver.common.by import By

from pages.LoginPage import LoginPage
from pages.MyInfoPage import MyInfoPage
from utilities.ReadProperties import ReadConfig


class TestUpdateMyInfo:
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()
    BASE_URL = ReadConfig.get_base_url()

    new_f_name = "sabari"
    new_l_name = "Tarkuri"

    @pytest.mark.smoke
    def test_update_my_info_014(self, setup):
        driver = setup
        driver.get(self.BASE_URL)
        driver.maximize_window()
        driver.implicitly_wait(5)

        test_login_page = LoginPage(driver)
        test_login_page.enter_username(self.username)
        test_login_page.enter_password(self.password)
        test_login_page.click_login()

        test_update_info = MyInfoPage(driver)
        test_update_info.click_myinfo()
        test_update_info.update_firstname(self.new_f_name)
        test_update_info.update_lastname(self.new_l_name)
        test_update_info.update_emp_id("421")
        test_update_info.update_gender()
        test_update_info.click_save_details()

        success_message = driver.find_element(By.XPATH, "//p[text()='Successfully Updated']")

        if "Successfully Updated" in success_message.text:
            print("Successfully Updated")

            driver.refresh()
            update_name =driver.find_element(By.XPATH, "//div[@class='oxd-topbar-header-userarea']//span//p").text

            if self.new_f_name in update_name:
                print(f"{self.new_f_name} + {self.new_l_name}")
            else:
                print("not found")

            assert True
            driver.close()

        else:
            print("Failed to Update")
            driver.close()
            assert False
