import os
from datetime import datetime
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="chrome or firefox")


@pytest.fixture()
def browser(request):
    browser = request.config.getoption("browser")
    return browser

@pytest.fixture()
def setup(browser):
    # Detect headless mode (GitHub Actions sets HEADLESS=true)
    headless = os.getenv("HEADLESS", "false").lower() in ("true", "1", "yes")
    print("HEADLESS MODE =", headless)

    if browser.lower() == "chrome":
        options = webdriver.ChromeOptions()

        # KEEP YOUR EXISTING SETTINGS (not changed)
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

        # ✅ Add HEADLESS support for GitHub Actions
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

            # GitHub's Chrome binary path
            chrome_bin = os.getenv("CHROME_BIN")
            if chrome_bin:
                options.binary_location = chrome_bin

        # Use webdriver-manager so ChromeDriver always matches
        driver = webdriver.Chrome(service=webdriver.ChromeService(ChromeDriverManager().install()),
                                  options=options)

    elif browser.lower() == "firefox":
        options = webdriver.FirefoxOptions()

        if headless:
            options.add_argument("--headless")

        driver = webdriver.Firefox(service=webdriver.FirefoxService(GeckoDriverManager().install()),
                                   options=options)

    elif browser.lower() == "safari":
        driver = webdriver.Safari()

    elif browser.lower() == "edge":
        driver = webdriver.Edge()

    else:
        raise ValueError("browser must be either chrome or firefox")

    yield driver
    driver.quit()
