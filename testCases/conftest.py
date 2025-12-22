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


def pytest_html_report_title(report):
    report.title = "OrangeHRM Automation Test Report"

def pytest_metadata(metadata):
    metadata["Tester"] = "Abdul Muyeez"
    metadata["Project"] = "OrangeHRM Automation"
    metadata["Framework"] = "Pytest + Selenium"
    metadata["Browser"] = "Chrome (Headless in CI)"
    metadata["Execution"] = "GitHub Actions"


def pytest_configure(config):
    # Auto-generate report path if not provided
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
        <style>
            body {{
                background-color: #121212 !important;
                color: #E0E0E0 !important;
            }}

            h1 {{
                padding : 5px 0px;
                border-radius : 12px;
                background: linear-gradient(to right, #ff7a18, #ff9900);
                text-align: center;
                color: #FFFFFF !important;
            }}

            h2, h3 {{
                color: #F5F5F5 !important;
            }}

            table {{
                color: #E0E0E0 !important;
            }}

            th {{
                color: #FFFFFF !important;
            }}

            td {{
                background-color: #121212 !important;
                color: #E0E0E0 !important;
            }}
            
            p {{
            color: #FFFFFF !important;
            }}
            
            canvas {{
            padding: 15px;
            border-radius: 12px;
            background-color: #E0E0E0 !important;
            }}
        </style>

        <h2>Test Result Distribution</h2>

        <canvas id="resultChart" width="360" height="360"></canvas>

        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script>
            const passed = {PASSED};
            const failed = {FAILED};
            const skipped = {SKIPPED};
            const total = passed + failed + skipped;

            new Chart(document.getElementById('resultChart'), {{
                type: 'pie',
                data: {{
                    labels: ['Passed', 'Failed', 'Skipped'],
                    datasets: [{{
                        data: [passed, failed, skipped],
                        backgroundColor: ['#2ecc71', '#FF0000', '#f1c40f'],
                        borderColor: '#121212',
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    responsive: false,
                    plugins: {{
                        tooltip: {{
                            callbacks: {{
                                label: function(context) {{
                                    const value = context.raw;
                                    const percent = ((value / total) * 100).toFixed(1);
                                    return `${{context.label}}: ${{value}} (${{percent}}%)`;
                                }}
                            }}
                        }},
                        legend: {{
                            labels: {{
                                color: '#000000',
                                font: {{ size: 14 }}
                            }}
                        }}
                    }}
                }}
            }});
        </script>
        """
    )

    prefix.insert(0, """
        <div style="
            background: #1e1e1e;
            color: #ffffff;
            text-align: center;
            padding: 18px;
            border-radius: 12px;
            margin-bottom: 20px;
            font-size: 32px;
            font-weight: bold;
        ">
        </div>
    """)

    # prefix.insert(0, """
    #     <div style="
    #         background:#1e1e1e;
    #         padding:15px;
    #         border-radius:10px;
    #         margin-bottom:20px;
    #     ">
    #         <h1 style="color:#FFFFFF; margin:0;">
    #             OrangeHRM Automation Test Report
    #         </h1>
    #         <p style="color:#E0E0E0; margin:5px 0 0 0;">
    #             Tester: <b>Abdul Muyeez</b> |
    #             Framework: Pytest + Selenium |
    #             Execution: CI (GitHub Actions)
    #         </p>
    #     </div>
    # """)
