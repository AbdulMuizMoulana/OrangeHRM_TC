import os
from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as GeckoService
from selenium.webdriver.edge.service import Service as EdgeService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from pytest_html import extras


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on: chrome, firefox, edge, safari"
    )


@pytest.fixture()
def browser(request):
    return request.config.getoption("browser")


@pytest.fixture()
def setup(browser):
    headless = os.getenv("HEADLESS", "false").lower() in ("true", "1", "yes")
    browser_name = (browser or "chrome").lower()

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--lang=en-US")
        options.add_argument("--incognito")

        if headless:
            options.add_argument("--lang=en-US")
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--start-maximized")
            options.add_argument("--force-device-scale-factor=1")
            options.add_argument("--high-dpi-support=1")
            options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # IMPORTANT FIX
        if headless:
            driver.set_window_size(1920, 1080)


    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("-headless")
            options.add_argument("--window-size=1920,1080")
        service = GeckoService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

    elif browser_name == "edge":
        options = webdriver.EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)

    elif browser_name == "safari":
        if headless:
            raise RuntimeError("Safari does not support headless mode.")
        driver = webdriver.Safari()

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    try:
        driver.maximize_window()
    except:
        pass

    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def _default_report_path():
    reports_dir = Path.cwd() / "Reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    filename = datetime.now().strftime("TestReport_%d-%m-%Y_%H-%M-%S.html")
    return str(reports_dir / filename)


def pytest_configure(config):
    if hasattr(config.option, "htmlpath"):
        config.option.htmlpath = _default_report_path()




from pytest_html import extras

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("setup", None)
        if driver:
            try:
                # Take screenshot in base64
                png_b64 = driver.get_screenshot_as_base64()

                # IMPORTANT: remove whitespace + line breaks
                png_b64 = png_b64.replace("\n", "").replace("\r", "").strip()

                # Attach screenshot as proper PNG
                extra = extras.png(png_b64, "Screenshot on failure")

                if hasattr(report, "extra"):
                    report.extra.append(extra)
                else:
                    report.extra = [extra]

            except Exception as e:
                print(f"Screenshot capture failed: {e}")


# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     # FIX for pytest-html-reporter crash: only run if plugin exists
#     try:
#         from pytest_html import extras
#     except ImportError:
#         extras = None
#
#     outcome = yield
#     report = outcome.get_result()
#
#     if extras and report.when == "call" and report.failed:
#         driver = item.funcargs.get("setup")
#         if driver:
#             screenshot = driver.get_screenshot_as_base64()
#             report.extra = getattr(report, "extra", [])
#             report.extra.append(
#                 extras.image(screenshot, mime_type="image/png")
#             )


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
