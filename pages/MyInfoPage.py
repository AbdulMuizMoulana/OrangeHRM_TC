from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class MyInfoPage:
    button_myinfo_xpath = "//span[text()='My Info']"
    input_firstName_xpath = "//input[@name='firstName']"
    input_lastName_xpath = "//input[@name='lastName']"
    input_emp_id_xpath = "//label[text()='Employee Id']/parent::div/following-sibling::div/input"
    radio_male_xpath_ = "//label[normalize-space()='Male']"
    button_save_xpath = "//p[text()=' * Required']/following-sibling::button"

    def __init__(self, driver):
        self.driver = driver

    def click_myinfo(self):
        self.driver.find_element(By.XPATH, self.button_myinfo_xpath).click()

    def update_firstname(self, firstname):
        f_name = self.driver.find_element(By.XPATH, self.input_firstName_xpath)
        f_name.send_keys(Keys.CONTROL, 'a')
        f_name.send_keys(Keys.DELETE)
        f_name.send_keys(firstname)

    def update_lastname(self, lastname):
        l_name = self.driver.find_element(By.XPATH, self.input_lastName_xpath)
        l_name.send_keys(Keys.CONTROL, 'a')
        l_name.send_keys(Keys.DELETE)
        l_name.send_keys(lastname)

    def update_emp_id(self, emp_id):
        e_id = self.driver.find_element(By.XPATH, self.input_emp_id_xpath)
        e_id.click()
        e_id.send_keys(Keys.CONTROL, 'a')  # Select all
        e_id.send_keys(Keys.DELETE)  # Clear
        e_id.send_keys(emp_id)

    def update_gender(self):
        self.driver.find_element(By.XPATH, self.radio_male_xpath_).click()

    def click_save_details(self):
        self.driver.find_element(By.XPATH, self.button_save_xpath).click()
