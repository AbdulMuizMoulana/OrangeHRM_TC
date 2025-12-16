from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class PIMContactDetailsPage:
    contact_details_xpath = "//a[normalize-space()='Contact Details']"
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

    def __init__(self, driver, wait_timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_timeout)

    # ---- helpers ----
    def _wait_visible(self, xpath):
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

    def _click_when_clickable(self, xpath):
        elem = self.wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return elem.click()


    def _clear_and_send_keys(self, element, text):
        """Try .clear(), fallback to CTRL+A + DELETE, then send text."""
        element.send_keys(Keys.CONTROL, "a")
        element.send_keys(Keys.DELETE)
        element.send_keys(text)

    # ---- actions ----
    def click_contact_details(self):
        self._wait_visible(self.contact_details_xpath).click()

    def enter_street1(self, street_1):
        el = self._wait_visible(self.street_1_input_xpath)
        self._clear_and_send_keys(el, street_1)

    def enter_street2(self, street_2):
        el = self._wait_visible(self.Street_2_input_xpath)
        self._clear_and_send_keys(el, street_2)

    def enter_city(self, city):
        el = self._wait_visible(self.city_input_xpath)
        self._clear_and_send_keys(el, city)

    def enter_state(self, state):
        el = self._wait_visible(self.state_input_xpath)
        self._clear_and_send_keys(el, state)

    def enter_zip_code(self, zip_code):
        el = self._wait_visible(self.zip_code_input_xpath)
        self._clear_and_send_keys(el, zip_code)

    def click_country_dropdown(self):
        self._click_when_clickable(self.country_dropdown_xpath)

    def select_country(self, country):
        """
        Select a country by visible text (country parameter).
        Note: the dynamic option XPath uses normalize-space() to match provided country text.
        """
        self.click_country_dropdown()
        option_xpath = f"//div[@class='oxd-select-wrapper']/div/div[contains(normalize-space(),'{country}')]"
        self._click_when_clickable(option_xpath)

    # telephone
    def enter_home_phone_number(self, home_ph_number):
        el = self._wait_visible(self.home_input_xpath)
        self._clear_and_send_keys(el, home_ph_number)

    def enter_work_phone_number(self, work_ph_number):
        el = self._wait_visible(self.work_input_xpath)
        self._clear_and_send_keys(el, work_ph_number)

    def enter_mobile_phone_number(self, mobile_ph_number):
        el = self._wait_visible(self.mobile_input_xpath)
        self._clear_and_send_keys(el, mobile_ph_number)

    def enter_work_email(self, work_email):
        el = self._wait_visible(self.work_email_input_xpath)
        self._clear_and_send_keys(el, work_email)

    def enter_other_email(self, other_email):
        el = self._wait_visible(self.other_email_input_xpath)
        self._clear_and_send_keys(el, other_email)

    def click_save_button(self):
        self._click_when_clickable(self.save_contact_details_xpath)
