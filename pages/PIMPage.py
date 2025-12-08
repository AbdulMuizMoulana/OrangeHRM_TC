from selenium.webdriver.common.by import By


class PIMPage:
    pim_button_xpath = "//span[contains(normalize-space(),'PIM')]"
    employee_add_button_xpath = "//button[contains(normalize-space(),'Add')]"
    firstname_input_name = "firstName"
    middlename_input_name = "middleName"
    lastname_input_name = "lastName"
    employee_id_input_xpath = "(//div/input[@class='oxd-input oxd-input--active'])[2]"
    save_button_xpath = "//button[contains(normalize-space(),'Save')]"
    employee_list_xpath = "//li[contains(normalize-space(),'Employee List')]"

    # add attachment in employee list
    button_emloyee_list_xpath = "//a[contains(normalize-space(),'Employee List')]"
    card_emp_details_xpath = "//div[text()='1232222']/parent::div/parent::div"
    button_attachment_add_xpath = "//button[text()=' Add ']"
    input_upload_file = "//input[@type='file']"
    textarea_xpath = "//textarea"
    button_Save_attachment_xpath = "//div[@class='orangehrm-attachment']//button[@type='submit'][normalize-space()='Save']"

    # employee_search
    input_employee_name_xpath = "//label[text()='Employee Name']/parent::div/following-sibling::div//input"
    button_search_xpath = "//button[contains(normalize-space(),'Search')]"


    def __init__(self, driver):
        self.driver = driver

    def click_pim_button(self):
        self.driver.find_element(By.XPATH, self.pim_button_xpath).click()

    def click_employee_add_button(self):
        self.driver.find_element(By.XPATH, self.employee_add_button_xpath).click()

    def enter_firstname(self, firstname):
        self.driver.find_element(By.NAME, self.firstname_input_name).send_keys(firstname)

    def enter_middlename(self, middlename):
        self.driver.find_element(By.NAME, self.middlename_input_name).send_keys(middlename)

    def enter_lastname(self, lastname):
        self.driver.find_element(By.NAME, self.lastname_input_name).send_keys(lastname)

    def enter_employee_id(self, employee_id):
        emp_id = self.driver.find_element(By.XPATH, self.employee_id_input_xpath)
        emp_id.send_keys(employee_id)

    def click_save_button(self):
        self.driver.find_element(By.XPATH, self.save_button_xpath).click()

    # add attachment methods
    def click_employee_list(self):
        self.driver.find_element(By.XPATH, self.employee_list_xpath).click()

    def click_card_emp_details(self):
        self.driver.find_element(By.XPATH, self.card_emp_details_xpath).click()

    def click_attachment_add_button(self):
        self.driver.find_element(By.XPATH, self.button_attachment_add_xpath).click()

    def select_file(self, path):
        self.driver.find_element(By.XPATH, self.input_upload_file).send_keys(path)

    def enter_comment(self, comment):
        self.driver.find_element(By.XPATH, self.textarea_xpath).click()

    def click_save_attachment(self):
        self.driver.find_element(By.XPATH, self.button_Save_attachment_xpath).click()

# employee search in employee lis methods

    def enter_employee_name(self, employee_name):
        self.driver.find_element(By.XPATH,self.input_employee_name_xpath).send_keys(employee_name)

    def click_emp_search(self):
        self.driver.find_element(By.XPATH, self.button_search_xpath).click()
