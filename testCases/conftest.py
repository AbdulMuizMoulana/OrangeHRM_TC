import os
from datetime import datetime
import pytest
from selenium import webdriver


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="chrome or firefox")


@pytest.fixture()
def browser(request):
    browser = request.config.getoption("browser")
    return browser


@pytest.fixture()
def setup(browser):
    if browser.lower() == "chrome":
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "password_manager_enabled": False,
            "intl.accept_languages": "en-US,en"
        })
        options.add_argument("--lang=en-US")
        options.add_argument("--incognito")
        options.add_argument("--disable-blink-features=CredentialManagement")
        options.add_argument("--disable-features=PasswordManagerOnboarding,AutofillServerCommunication")

        driver = webdriver.Chrome(options=options)
    elif browser.lower() == "firefox":
        driver = webdriver.Firefox()
    elif browser.lower() == "safari":
        driver = webdriver.Safari()
    elif browser.lower() == "edge":
        driver = webdriver.Edge()
    else:
        raise ValueError("browser must be either chrome or firefox")
    return driver


def pytest_configure(config):
    config._metadata = {
        "Tester": "Abdul Muyeez",
        "Project": "Login Automation",
        "Browser": "Chrome"
    }


# @pytest.mark.optionalhook
# def pytest_metadata(metadata):
#     metadata.pop('Plugins', None)
#     metadata.pop('Packages', None)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    config.option.htmlpath = os.path.abspath(os.curdir) + "\\Reports\\" + datetime.now().strftime(
        "%d-%m-%y- %H-%M-%S") + ".html"
