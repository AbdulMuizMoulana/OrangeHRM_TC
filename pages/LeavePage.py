from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LeavePage:
    button_leave_xpath = "//li/a/span[contains(normalize-space(),'Leave')]/parent::a"
    button_apply_xpath = "//nav[@class='oxd-topbar-body-nav']//a[contains(normalize-space(),'Apply')]"
    leave_type_dropdown_xpath = "//div/label[text()='Leave Type']/parent::div/following-sibling::div"
    leave_type_option_xpath = "//div/label[text()='Leave Type']/parent::div/following-sibling::div//span[text()='US - Personal']"
    from_date_xpath = "//div[@class='oxd-input-group__label-wrapper']/label[text()='From Date']/parent::div/following-sibling::div//input"
    to_date_xpath = "//div[@class='oxd-input-group__label-wrapper']/label[text()='To Date']/parent::div/following-sibling::div//input"
    duration_xpath = "//div[@class='oxd-input-group__label-wrapper']/label[text()='Duration']/parent::div/following-sibling::div"
    duration_option_xpath = "//span[text()='Half Day - Morning']"
    comment_textarea_xpath = "//textarea"
    apply_button_xpath = "//button[text()=' Apply ']"

    # Assign leave locators
    button_assign_leave_xpath = "//a[text()='Assign Leave']"
    input_emp_name_xpath = "//input[@placeholder='Type for hints...']"
    leave_type_annual_xpath = "//div/label[text()='Leave Type']/parent::div/following-sibling::div//span[text()='Annuall']"
    input_from_date_xpath = "//div/label[text()='From Date']/parent::div/following-sibling::div//input"
    input_to_date_xpath = "//div/label[text()='To Date']/parent::div/following-sibling::div//input"
    button_assign_xpath = "//button[@type='submit']"
    emp_name_option_xpath ="//span[text()='Abdul Muyeez Moulana']"

    def __init__(self, driver):
        self.driver = driver

    def click_leave(self):
        self.driver.find_element(By.XPATH, self.button_leave_xpath).click()

    def click_apply(self):
        self.driver.find_element(By.XPATH, self.button_apply_xpath).click()

    def select_leave_type(self):
        self.driver.find_element(By.XPATH, self.leave_type_dropdown_xpath).click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.leave_type_option_xpath))).click()
        # self.driver.find_element(By.XPATH, self.leave_type_option_xpath).click()


    def select_duration(self):
        duration = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.duration_xpath)))
        duration.click()
        self.driver.find_element(By.XPATH, self.duration_option_xpath).click()

    def enter_comment(self, comment):
        self.driver.find_element(By.XPATH, self.comment_textarea_xpath).send_keys(comment)

    def click_apply_submit_button(self):
        self.driver.find_element(By.XPATH, self.apply_button_xpath).click()

    # Assign leaves methods
    def click_assign_leave_button(self):
        assign_leave =WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH, self.button_assign_leave_xpath)))
        assign_leave.click()

    def enter_emp_name(self, emp_name):
        self.driver.find_element(By.XPATH, self.input_emp_name_xpath).click()
        self.driver.find_element(By.XPATH, self.input_emp_name_xpath).send_keys(emp_name)
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.XPATH, self.emp_name_option_xpath))).click()

    def enter_from_date(self, from_date):
        self.driver.find_element(By.XPATH, self.from_date_xpath).send_keys(from_date)

    def enter_to_date(self, to_date):
        todate = self.driver.find_element(By.XPATH, self.to_date_xpath)
        todate.send_keys(Keys.CONTROL, 'a')
        todate.send_keys(Keys.DELETE)
        todate.send_keys(to_date)

    def select_assign_leave_type(self):
        self.driver.find_element(By.XPATH, self.leave_type_dropdown_xpath).click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, self.leave_type_annual_xpath))).click()

    def click_assign_submit(self):
        self.driver.find_element(By.XPATH, self.button_assign_xpath).click()
