import pytest

from utilities.ReadProperties import ReadConfig
from pages.LoginPage import LoginPage
from pages.Dashboard import Dashboard


class TestDashboardPage:
    username = ReadConfig.get_username()
    password = ReadConfig.get_password()
    BASE_URL = ReadConfig.get_base_url()

    @pytest.mark.smoke
    def test_dashboard_end_session_003(self, setup):
        driver = setup
        driver.get(self.BASE_URL)
        driver.maximize_window()
        driver.implicitly_wait(5)

        test_login_page = LoginPage(driver)
        test_login_page.enter_username(self.username)
        test_login_page.enter_password(self.password)
        test_login_page.click_login()

        test_dashboard_page = Dashboard(driver)
        test_dashboard_page.click_profile_btn()
        test_dashboard_page.click_logout()

        current_url = driver.current_url
        if current_url == self.BASE_URL:
            assert True
            driver.close()
        else:
            driver.save_screenshot(".\\screenshots\\DashboardTest.png")
            driver.close()
            assert False
