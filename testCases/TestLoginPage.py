import pytest
from selenium.webdriver.common.by import By

from pages.LoginPage import LoginPage
from utilities.ReadProperties import ReadConfig
from utilities.CustomLogger import LogMaker

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestHomePage:
    BASE_URL = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()
    log = LogMaker.log_gen()

    @pytest.mark.smoke
    @pytest.mark.regression
    def test_login_001(self, setup):
        driver = setup
        self.log.info("************** Launching the web application ***************")
        driver.get(self.BASE_URL)
        driver.implicitly_wait(1000)
        driver.maximize_window()

        test_login_page = LoginPage(driver)
        self.log.info("************** starting logging in **************")
        test_login_page.enter_username(self.username)
        test_login_page.enter_password(self.password)
        test_login_page.click_login()
        self.log.info("************** verifying the landing page **************")
        dashboard = driver.find_element(By.XPATH, "//h6").text
        if "dashboard" in dashboard.lower():
            self.log.info(" ************** Successfully logged in to expected page **************")
            driver.close()
            assert True
        else:
            self.log.debug("************** Failed to login to expected page **************")
            driver.save_screenshot(".\\screenshots\\login.png")
            driver.close()
            assert False
    @pytest.mark.smoke
    def test_login_negative_002(self, setup):
        driver = setup
        driver.get(self.BASE_URL)
        driver.maximize_window()
        driver.implicitly_wait(10)

        test_login_page = LoginPage(driver)
        test_login_page.enter_username("Rockey")
        test_login_page.enter_password("hungama@123")
        test_login_page.click_login()

        expected_error_message = "Invalid credentials"
        error = driver.find_element(By.XPATH, "//p[contains(normalize-space(), 'Invalid credentials')]").text
        if error in expected_error_message:
            assert True
            driver.close()
        else:
            driver.save_screenshot(".\\screenshots\\NegativeLogin.png")
            driver.close()
            assert False

    @pytest.mark.smoke
    def test_login_negative_007(self, setup):
        driver = setup
        driver.get(self.BASE_URL)
        driver.maximize_window()
        driver.implicitly_wait(10)

        login_page = LoginPage(driver)
        # login_page.enter_username()
        # login_page.enter_password()
        login_page.click_login()
        expected_username_error_message = driver.find_element(By.XPATH, "//div/input[@name='username']/parent::div/following-sibling::span").text
        expected_password_error_message = driver.find_element(By.XPATH, "//div/input[@name='password']/parent::div/following-sibling::span").text

        if "Required" in expected_username_error_message and "Required" in expected_password_error_message:
            print(f"negative Test is passed,It contains :{expected_username_error_message}")
            assert True
            driver.close()
        else:
            driver.save_screenshot(".\\screenshots\\negativeLogin.png")
            driver.close()
            assert False

    @pytest.mark.smoke
    def test_login_ui_elements_presence_008(self, setup):
        driver = setup
        driver.get(self.BASE_URL)
        driver.maximize_window()
        driver.implicitly_wait(10)

        test_login_page = LoginPage(driver)
        assert test_login_page.is_displayed_login_branding(),"Login Branding is not displayed"
        assert test_login_page.is_displayed_login_logo(),"Login Logo is not displayed"
        assert test_login_page.is_displayed_username_text_field(),"Login Text Field is not displayed"
        assert test_login_page.is_displayed_button_login(),"Login Button is not displayed"

    @pytest.mark.smoke
    def test_login_forgot_password_009(self, setup):
        driver = setup
        driver.get(self.BASE_URL)
        driver.maximize_window()
        driver.implicitly_wait(10)

        forget_login_details = LoginPage(driver)
        forget_login_details.click_forgot_password()
        forget_login_details.enter_username(self.username)
        forget_login_details.click_reset_password()

        success_message = driver.find_element(By.XPATH, "//h6").text
        if "Reset Password link sent successfully" in success_message:
            print(success_message)
            assert True
            driver.close()
        else:
            driver.save_screenshot(".\\screenshots\\forgot_password.png")
            driver.close()
            assert False


