from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Dashboard:

    profile_button_Xpath = "//span[@class='oxd-userdropdown-tab']"
    logout_Xpath = "//a[contains(text(), 'Logout')]"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def click_profile_btn(self):
        # Wait until clickable, then click
        elem = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.profile_button_Xpath)))
        elem.click()

    def click_logout(self):
        # Wait until clickable, then click
        elem = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.logout_Xpath)))
        elem.click()
