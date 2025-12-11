from selenium.webdriver.common.by import By


class Dashboard:

    profile_button_Xpath = "//span[@class='oxd-userdropdown-tab']"
    logout_Xpath ="//a[contains(text(), 'Logout')]"



    def __init__(self, driver):
        self.driver = driver

    def click_profile_btn(self):
        self.driver.find_element(By.XPATH,self.profile_button_Xpath).click()

    def click_logout(self):
        self.driver.find_element(By.XPATH,self.logout_Xpath).click()


