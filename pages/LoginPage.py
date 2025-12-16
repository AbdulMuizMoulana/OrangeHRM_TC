from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    input_username_name = "username"
    input_password_name = "password"
    button_login_xpath = "//button"
    logo_orangehrm_xpath = "//div[@class='orangehrm-login-branding']/img"
    logo_login_xpath = "//div[@class='orangehrm-login-logo']/img"
    forgot_password_xpath = "//p[contains(normalize-space(),'Forgot')]"
    button_reset_password_xpath = "//button[contains(normalize-space(),'Reset Password')]"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # -------- Helper Methods --------
    def _clear_and_type(self, element, text):
        """Safely clear input fields and send keys."""
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(text)

    def _wait_and_click(self, locator):
        """Wait until element is clickable then click."""
        elem = self.wait.until(EC.element_to_be_clickable(locator))
        elem.click()

    def _wait_visible(self, locator):
        """Wait until element visible then return."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    # -------- Login Actions --------
    def enter_username(self, name):
        username_el = self._wait_visible((By.NAME, self.input_username_name))
        self._clear_and_type(username_el, name)

    def enter_password(self, password):
        password_el = self._wait_visible((By.NAME, self.input_password_name))
        self._clear_and_type(password_el, password)

    def click_login(self):
        self._wait_and_click((By.XPATH, self.button_login_xpath))

    # -------- UI Element Checks --------
    def is_displayed_login_elements(self, by, xpath):
        try:
            elem = self.wait.until(EC.visibility_of_element_located((by, xpath)))
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

    # -------- Forgot Password --------
    def click_forgot_password(self):
        self._wait_and_click((By.XPATH, self.forgot_password_xpath))

    def click_reset_password(self):
        self._wait_and_click((By.XPATH, self.button_reset_password_xpath))
