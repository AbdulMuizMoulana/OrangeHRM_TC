from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    input_username_name = "username"
    input_password_name = "password"
    button_login_xpath = "//button"
    logo_orangehrm_xpath = "//div[@class='orangehrm-login-branding']/img"
    logo_login_xpath = "//div[@class='orangehrm-login-logo']/img"
    forgot_password_xpath = "//p[contains(normalize-space(),'Forgot your password?')]"
    button_reset_password_xpath = "//button[contains(normalize-space(),'Reset Password')]"


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def enter_username(self, name):
        username_text_field = self.driver.find_element(By.NAME, self.input_username_name)
        username_text_field.clear()
        username_text_field.send_keys(name)

    def enter_password(self, password):
        password_text_field = self.driver.find_element(By.NAME, self.input_password_name)
        password_text_field.clear()
        password_text_field.send_keys(password)

    def click_login(self):
        self.driver.find_element(By.XPATH, self.button_login_xpath).click()

    # Login page UI Elements

    def is_displayed_login_elements(self,by,xpath):
        try:
            elem = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((by, xpath)))
            return elem.is_displayed()
        except:
            return False

    def is_displayed_login_branding(self):
        return self.is_displayed_login_elements(By.XPATH, self.logo_orangehrm_xpath)

    def is_displayed_login_logo(self):
        return self.is_displayed_login_elements(By.XPATH, self.logo_login_xpath)

    def is_displayed_username_text_field(self):
        return self.is_displayed_login_elements(By.NAME, self.input_username_name)

    def is_displayed_password_text_field(self):
        return self.is_displayed_login_elements(By.NAME, self.input_password_name)

    def is_displayed_button_login(self):
        return self.is_displayed_login_elements(By.XPATH, self.button_login_xpath)

# forgot password

    def click_forgot_password(self):
        self.driver.find_element(By.XPATH,self.forgot_password_xpath).click()

    def click_reset_password(self):
        self.driver.find_element(By.XPATH,self.button_reset_password_xpath).click()

