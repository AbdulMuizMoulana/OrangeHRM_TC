from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PIMContactDetailsPage:
    contact_details_xpath = "//a[contains(text(),'Contact Details')]"
    street_1_input_xpath = "//label[normalize-space()='Street 1']/parent::div/following-sibling::div//input"
    Street_2_input_xpath = "//label[normalize-space()='Street 2']/parent::div/following-sibling::div//input"
    city_input_xpath = "//label[normalize-space()='City']/parent::div/following-sibling::div//input"
    state_input_xpath = "//label[normalize-space()='State/Province']/parent::div/following-sibling::div//input"
    zip_code_input_xpath = "//label[normalize-space()='Zip/Postal Code']/parent::div/following-sibling::div//input"

    country_dropdown_xpath = "//div[@class='oxd-select-wrapper']"
    afghan_country_xpath = "//div[@class='oxd-select-wrapper']/div/div[contains(normalize-space(),'Afghanistan')]"
    # telephone
    home_input_xpath = "//div/label[contains(normalize-space(),'Home')]/parent::div/following-sibling::div/input"
    mobile_input_xpath = "//div/label[contains(normalize-space(),'Mobile')]/parent::div/following-sibling::div/input"
    work_input_xpath = "//div/label[contains(normalize-space(),'Work')]/parent::div/following-sibling::div/input"

    # Email
    work_email_input_xpath = "//div/label[contains(normalize-space(),'Work Email')]/parent::div/following-sibling::div/input"
    other_email_input_xpath = "//div/label[contains(normalize-space(),'Other Email')]/parent::div/following-sibling::div/input"
    save_contact_details_xpath = "//button[contains(normalize-space(), 'Save')]"

    def __init__(self, driver):
        self.driver = driver

    def click_contact_details(self):
        WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.XPATH, self.contact_details_xpath))).click()

    def enter_street1(self, street_1):
        self.driver.find_element(By.XPATH, self.street_1_input_xpath).send_keys(street_1)

    def enter_street2(self, street_2):
        self.driver.find_element(By.XPATH, self.Street_2_input_xpath).send_keys(street_2).send_keys(street_2)

    def enter_city(self, city):
        self.driver.find_element(By.XPATH, self.city_input_xpath).send_keys(city)

    def enter_state(self, state):
        self.driver.find_element(By.XPATH, self.state_input_xpath).send_keys(state)

    def enter_zip_code(self, zip_code):
        self.driver.find_element(By.XPATH, self.zip_code_input_xpath).send_keys(zip_code)

    def click_country_dropdown(self):
        self.driver.find_element(By.XPATH, self.country_dropdown_xpath).click()

    def select_country(self, country):
        self.click_country_dropdown()
        option_xpath = f"//div[@class='oxd-select-wrapper']/div/div[contains(normalize-space(),'{country}']"
        self.driver.find_element(By.XPATH, option_xpath).click()

#     telephone
    def enter_home_phone_number(self, home_ph_number):
        self.driver.find_element(By.XPATH, self.home_input_xpath).send_keys(home_ph_number)

    def enter_work_phone_number(self, work_ph_number):
        self.driver.find_element(By.XPATH, self.work_input_xpath).send_keys(work_ph_number)

    def enter_mobile_phone_number(self, mobile_ph_number):
        self.driver.find_element(By.XPATH, self.mobile_input_xpath).send_keys(mobile_ph_number)

    def enter_work_email(self, work_email):
        self.driver.find_element(By.XPATH, self.work_email_input_xpath).send_keys(work_email)

    def enter_other_email(self, other_email):
        self.driver.find_element(By.XPATH, self.other_email_input_xpath).send_keys(other_email)

    def click_save_button(self):
        self.driver.find_element(By.XPATH, self.save_contact_details_xpath).click()


