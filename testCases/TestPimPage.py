import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.LoginPage import LoginPage
from pages.PIMPage import PIMPage
from utilities.ReadProperties import ReadConfig


class TestPimPage:
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()
    BASE_URL = ReadConfig.get_base_url()
    emp_id ="AUTO001"

    ess_username = ReadConfig.get_ess_username()
    ess_password = ReadConfig.get_ess_password()

    attachment_file ="C:\\Users\\LENOVO\\PycharmProjects\\OrangeHRM\\AIO_TestCases.xlsx"
    negative_file = "C:\\Users\\LENOVO\\PycharmProjects\\OrangeHRM\\Screen Recording 2025-11-07 120303.mp4"
    # attachment_file = "..//AIO_TestCases.xlsx"
    # negative_file = "..//Screen Recording 2025-11-07 120303.mp4"

    @pytest.mark.smoke
    def test_pim_add_employee_004(self, setup):
        driver =setup
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
        test_pim_add_employee.enter_firstname("lucy")
        test_pim_add_employee.enter_middlename("juicy")
        test_pim_add_employee.enter_lastname("Spicy")
        test_pim_add_employee.enter_employee_id(self.emp_id)
        test_pim_add_employee.click_save_button()

        test_pim_add_employee.click_employee_list()
        list_employees = driver.find_elements(By.XPATH, "//div[@class='oxd-table-card --mobile']")
        for employee in list_employees:
            if self.emp_id in employee.text:
                assert True
                driver.close()
            else:
                driver.save_screenshot(".\\screenshots\\employee_list.png")
                assert False

    @pytest.mark.smoke
    def test_add_attachments_012(self,setup):
        driver =setup
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
        test_add_attachments.select_file(self.attachment_file)
        test_add_attachments.enter_comment("this example file")
        test_add_attachments.click_save_attachment()

        success_message = driver.find_element(By.XPATH,"//p[contains(normalize-space(),'Successfully Saved')]").text
        if "Successfully Saved" in success_message:
            print("Successfully Saved")
            record = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,"//div[text()='AIO_TestCases.xlsx']/parent::div/parent::div")))
            if record.is_displayed():
                print("successfully displayed record in list")
                assert True
                driver.close()
        else:
            print("Failed to Saved")
            driver.save_screenshot(".\\screenshots\\add_attachment_success_message.png")
            driver.close()

    @pytest.mark.smoke
    def test_add_attachments_negative_013(self,setup):
        driver =setup
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
        test_add_attachments.select_file(self.negative_file)
        test_add_attachments.enter_comment("this example file")
        test_add_attachments.click_save_attachment()

        error_message = driver.find_element(By.XPATH,"//span[contains(normalize-space(),'Attachment Size Exceeded')]").text
        if "Attachment Size Exceeded" in error_message:
            print("displaying error message as Attachment \"Size Exceeded\"")
            assert True
            driver.close()
        else:
            print("Failed not displayin error message")
            driver.save_screenshot(".\\screenshots\\add_attachment_error_message.png")
            driver.close()

    def test_employee_search_negative_015(self,setup):
        driver =setup
        driver.get(self.BASE_URL)
        driver.maximize_window()
        driver.implicitly_wait(5)

        login_page = LoginPage(driver)
        login_page.enter_username(self.username)
        login_page.enter_password(self.password)
        login_page.click_login()

        test_employee_search = PIMPage(driver)
        test_employee_search.click_pim_button()
        test_employee_search.enter_employee_name("abcd123")
        test_employee_search.click_emp_search()

        error_message = driver.find_element(By.XPATH,"//p[contains(normalize-space(),'No Records Found')]").text
        if "No Records Found" in error_message:
            print("displaying error message as No Records Found")
            assert True
            driver.close()
        else:
            print("Failed not displayin error message")
            driver.save_screenshot(".\\screenshots\\employee_search_error_message.png")
            driver.close()


