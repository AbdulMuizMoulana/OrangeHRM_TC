import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MyInfoPage:
    # --- XPaths (unchanged) ---
    button_myinfo_xpath = "//span[text()='My Info']"
    input_firstName_xpath = "//input[@name='firstName']"
    input_lastName_xpath = "//input[@name='lastName']"
    input_emp_id_xpath = "//label[text()='Employee Id']/parent::div/following-sibling::div/input"
    radio_male_xpath_ = "//label[normalize-space()='Male']"
    button_save_xpath = "//p[text()=' * Required']/following-sibling::button"

    def __init__(self, driver, wait_timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_timeout)

    # ------- Helper utilities (internal) -------
    def _wait_visible(self, xpath):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def _click_when_clickable(self, xpath):
        elem = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        elem.click()
        return elem

    def _clear_and_send_keys(self, element, text):
        """Try element.clear(); if that fails use CTRL+A + DELETE, then send keys."""
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(text)

    # ------- Page actions -------
    def click_myinfo(self):
        self._click_when_clickable(self.button_myinfo_xpath)
        time.sleep(5)

    def update_firstname(self, firstname):
        f_name = self._wait_visible(self.input_firstName_xpath)
        self._clear_and_send_keys(f_name, firstname)

    def update_lastname(self, lastname):
        l_name = self._wait_visible(self.input_lastName_xpath)
        self._clear_and_send_keys(l_name, lastname)

    def update_emp_id(self, emp_id):
        e_id = self._wait_visible(self.input_emp_id_xpath)
        self._clear_and_send_keys(e_id, emp_id)

    def update_gender(self):
        # wait for radio label to be clickable then click
        self._click_when_clickable(self.radio_male_xpath_)

    def click_save_details(self):
        self._click_when_clickable(self.button_save_xpath)
