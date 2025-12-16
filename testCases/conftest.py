import os
from datetime import datetime
from pathlib import Path

import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as GeckoService
from selenium.webdriver.edge.service import Service as EdgeService

# webdriver-manager imports
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on: chrome (default), firefox, edge, safari"
    )


@pytest.fixture()
def browser(request) -> str:
    return request.config.getoption("browser")


@pytest.fixture()
def setup(browser):
    """
    Returns a webdriver instance based on --browser option.
    Supports HEADLESS mode via environment variable HEADLESS=true|1|yes
    and respects CHROME_BIN environment variable if provided (useful on CI).
    """
    headless = os.getenv("HEADLESS", "false").lower() in ("true", "1", "yes")
    browser_name = (browser or "chrome").lower()

    if browser_name == "chrome":
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

        if headless:
            # new headless flag for modern Chrome; fallback to "--headless" if you need
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

        # If CI provides a Chrome binary path (e.g. /usr/bin/google-chrome-stable)
        chrome_bin = os.getenv("CHROME_BIN")
        if chrome_bin:
            options.binary_location = chrome_bin

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        service = GeckoService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

    elif browser_name == "edge":
        options = webdriver.EdgeOptions()
        if headless:
            # Edge/Chromium usually accepts same headless flags as Chrome
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--no-sandbox")
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)

    elif browser_name == "safari":
        # SafariDriver comes preinstalled on macOS (no webdriver-manager)
        if headless:
            raise RuntimeError("Safari does not support headless mode in this fixture.")
        driver = webdriver.Safari()

    else:
        raise ValueError("Unsupported browser: %s. Choose chrome, firefox, edge or safari." % browser_name)

    # common setup: maximize + implicit wait (tune as needed)
    try:
        driver.maximize_window()
    except Exception:
        # some headless environments don't support maximize_window
        pass

    driver.implicitly_wait(5)

    yield driver

    try:
        driver.quit()
    except Exception:
        pass



def _default_report_path() -> str:
    reports_dir = Path.cwd() / "Reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    filename = datetime.now().strftime("TestReport_%d-%m-%Y_%H-%M-%S.html")
    return str(reports_dir / filename)


def pytest_configure(config):
    # Force custom report filename
    if hasattr(config.option, "htmlpath"):
        config.option.htmlpath = _default_report_path()


def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([
        "Tester: Abdul Muyeez",
        "Project: Login Automation",
        "Browser: Chrome"
    ])


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("setup")  # YOUR WebDriver fixture
        if driver:
            screenshot = driver.get_screenshot_as_base64()
            report.extra = getattr(report, "extra", [])
            report.extra.append(
                pytest_html.extras.image(screenshot, mime_type='image/png')
            )




























# def _default_report_path() -> str:
#     # Reports folder inside project root
#     reports_dir = Path.cwd() / "Reports"
#     reports_dir.mkdir(parents=True, exist_ok=True)
#     filename = datetime.now().strftime("%d-%m-%y_%H-%M-%S") + ".html"
#     return str(reports_dir / filename)
#
#
# def pytest_configure(config):
#     # Add custom metadata
#     config._metadata = {
#         "Tester": "Abdul Muyeez",
#         "Project": "Login Automation",
#         "Browser": "Chrome"
#     }
# # Set HTML report path if html plugin present and not already provided
#     if hasattr(config.option, "htmlpath") and not config.option.htmlpath:
#         config.option.htmlpath = _default_report_path()
