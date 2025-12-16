from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
    dropdown_emp_information ="//i[@class='oxd-icon bi-caret-down-fill']"
    input_emp_id_xpath = "//label[text()='Employee Id']/parent::div/following-sibling::div/input"
    def __init__(self, driver, wait_timeout: int = 20):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_timeout)

    # ---------- Helpers ----------
    def _wait_visible(self, xpath):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def _click_when_clickable(self, xpath):
        elem = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return elem.click()

    def _wait_presence(self, xpath):
        return self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    def _clear_and_send_keys(self, element, text):
        """Try clear(); if fails use CTRL+A + DELETE; then send text."""
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(text)

    # ---------- Page actions ----------
    def click_pim_button(self):
        self._wait_visible(self.pim_button_xpath).click()

    def click_employee_add_button(self):
        self._click_when_clickable(self.employee_add_button_xpath)

    def enter_firstname(self, firstname):
        el = self.wait.until(EC.visibility_of_element_located((By.NAME, self.firstname_input_name)))
        self._clear_and_send_keys(el, firstname)

    def enter_middlename(self, middlename):
        el = self.wait.until(EC.visibility_of_element_located((By.NAME, self.middlename_input_name)))
        self._clear_and_send_keys(el, middlename)

    def enter_lastname(self, lastname):
        el = self.wait.until(EC.visibility_of_element_located((By.NAME, self.lastname_input_name)))
        self._clear_and_send_keys(el, lastname)

    def enter_employee_id(self, employee_id):
        try:
            el = self._wait_visible(self.employee_id_input_xpath)
            self._clear_and_send_keys(el, employee_id)
        except:
            self._wait_visible(self.dropdown_emp_information).click()
            el = self._wait_visible(self.employee_id_input_xpath)
            self._clear_and_send_keys(el, employee_id)

    def click_save_button(self):
        self._click_when_clickable(self.save_button_xpath)

    # ---------- Attachment actions ----------
    def click_employee_list(self):
        self._wait_visible(self.employee_list_xpath).click()

    def click_card_emp_details(self):
        # This is a brittle locator (text '1232222') but preserved as requested.
        self._click_when_clickable(self.card_emp_details_xpath)

    def click_attachment_add_button(self):
        self._wait_presence(self.button_attachment_add_xpath).click()

    def select_file(self, path):
        file = self._wait_presence(self.input_upload_file)
        file.send_keys(path)

    def enter_comment(self, comment):
        ta = self._wait_visible(self.textarea_xpath)
        # click to focus then send keys safely
        try:
            ta.click()
        except Exception:
            pass
        self._clear_and_send_keys(ta, comment)

    def click_save_attachment(self):
        self._wait_visible(self.button_Save_attachment_xpath).click()

    # ---------- Employee search ----------
    def enter_employee_name(self, employee_name):
        try:
            self._wait_presence(self.input_employee_name_xpath).send_keys(employee_name)
        except:
            self._wait_visible(self.dropdown_emp_information).click()
            self._wait_presence(self.input_employee_name_xpath).send_keys(employee_name)





    def click_emp_search(self):
        try:
            self._wait_visible(self.button_search_xpath).click()
        except:
            self._wait_visible(self.dropdown_emp_information).click()
            self._wait_visible(self.button_search_xpath).click()

    # def enter_employee_id(self,emp_id):
    #     self._wait_visible(self.input_emp_id_xpath).send_keys(emp_id)


