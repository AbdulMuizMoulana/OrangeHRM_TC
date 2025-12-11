import os
from datetime import datetime
import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

# Services for explicit log_path and better control
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService


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

    # Try to print available chrome/chromedriver versions (best-effort)
    try:
        import subprocess
        print("CHROME_BIN:", os.getenv("CHROME_BIN"))
        try:
            subprocess.run(["chromium-browser", "--version"], check=True)
        except Exception:
            try:
                subprocess.run(["google-chrome", "--version"], check=True)
            except Exception:
                pass
        try:
            subprocess.run(["chromedriver", "--version"], check=True)
        except Exception:
            pass
    except Exception:
        pass

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

        # HEADLESS support for GitHub Actions - use compatible flags
        if headless:
            # Use the plain headless flag for best compatibility in CI
            options.add_argument("--headless")
            # If you prefer the new headless mode and your Chrome/driver are new enough,
            # you can try: options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-software-rasterizer")

            # GitHub's Chrome binary path (set from workflow if needed)
            chrome_bin = os.getenv("CHROME_BIN")
            if chrome_bin:
                options.binary_location = chrome_bin

        # Use webdriver-manager so ChromeDriver always matches; write driver log for debugging
        chromedriver_path = ChromeDriverManager().install()
        service = ChromeService(chromedriver_path, log_path="chromedriver.log")

        driver = webdriver.Chrome(service=service, options=options)

    elif browser.lower() == "firefox":
        options = webdriver.FirefoxOptions()

        if headless:
            options.add_argument("--headless")

        gecko_path = GeckoDriverManager().install()
        firefox_service = FirefoxService(gecko_path, log_path="geckodriver.log")

        driver = webdriver.Firefox(service=firefox_service, options=options)

    elif browser.lower() == "safari":
        driver = webdriver.Safari()

    elif browser.lower() == "edge":
        driver = webdriver.Edge()

    else:
        raise ValueError("browser must be either chrome or firefox")

    yield driver

    try:
        driver.quit()
    except Exception:
        pass
