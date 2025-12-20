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



# ---------------- PIE CHART COUNTERS ----------------
PASSED = 0
FAILED = 0
SKIPPED = 0
# ---------------------------------------------------


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
    # Always set metadata
    config._metadata = {
        "Tester": "Abdul Muyeez",
        "Project": "Login Automation",
        "Browser": "Chrome"
    }

    # If PyCharm DID NOT pass --html, auto-generate a report
    if not getattr(config.option, "htmlpath", None):
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


def pytest_runtest_logreport(report):
    global PASSED, FAILED, SKIPPED

    if report.when == "call":
        if report.passed:
            PASSED += 1
        elif report.failed:
            FAILED += 1
        elif report.skipped:
            SKIPPED += 1


def pytest_html_results_summary(prefix, summary, postfix):
    prefix.append(
        f"""
        <h2>Test Result Distribution</h2>
        <canvas id="resultChart" width="350" height="350"></canvas>

        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
            new Chart(document.getElementById('resultChart'), {{
                type: 'pie',
                data: {{
                    labels: ['Passed', 'Failed', 'Skipped'],
                    datasets: [{{
                        data: [{PASSED}, {FAILED}, {SKIPPED}],
                        backgroundColor: ['#28a745', '#dc3545', '#ffc107']
                    }}]
                }},
                options: {{ responsive: false }}
            }});
        </script>
        """
    )



#
#
# def pytest_html_results_summary(prefix, summary, postfix):
#     # Convert None → 0  (VERY IMPORTANT)
#     passed = getattr(summary, "passed", 0) or 0
#     failed = getattr(summary, "failed", 0) or 0
#     skipped = getattr(summary, "skipped", 0) or 0
#
#     prefix.extend([
#         html.div(
#             html.h3("Test Summary Pie Chart"),
#             html.div(id="piechart", style="width:300px;height:300px;"),
#         ),
#         html.script(
#             f"""
#             window.onload = function() {{
#                 let passed = {passed};
#                 let failed = {failed};
#                 let skipped = {skipped};
#
#                 let total = passed + failed + skipped;
#                 if (total === 0) return;
#
#                 let canvas = document.createElement("canvas");
#                 canvas.width = 300;
#                 canvas.height = 300;
#                 document.getElementById("piechart").appendChild(canvas);
#
#                 let ctx = canvas.getContext("2d");
#                 let data = [
#                     {{ label: "Passed", value: passed, color: "#4CAF50" }},
#                     {{ label: "Failed", value: failed, color: "#F44336" }},
#                     {{ label: "Skipped", value: skipped, color: "#FFC107" }}
#                 ];
#
#                 let start = 0;
#                 data.forEach(item => {{
#                     if (item.value === 0) return;
#                     let slice = (item.value / total) * 2 * Math.PI;
#                     ctx.beginPath();
#                     ctx.moveTo(150,150);
#                     ctx.arc(150,150,150, start, start + slice);
#                     ctx.closePath();
#                     ctx.fillStyle = item.color;
#                     ctx.fill();
#                     start += slice;
#                 }});
#             }};
#             """
#         )
#     ])
