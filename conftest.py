import os
import pytest
import allure
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    """Add --headless CLI flag to switch between headed and headless Chrome."""
    parser.addoption(
        "--headless",
        action="store",
        default="true",
        help="Run Chrome in headless mode: true (default) or false"
    )


@pytest.fixture(scope="session")
def headless_option(request):
    return request.config.getoption("--headless").lower() == "true"


@pytest.fixture(scope="session")
def driver(headless_option):
    """Session-scoped Chrome WebDriver fixture with teardown."""
    print("\nInitializing Chrome WebDriver...")
    chrome_options = Options()

    if headless_option:
        print("Running in HEADLESS mode...")
        chrome_options.add_argument("--headless=new")
    else:
        print("Running in HEADED (visible) mode...")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=chrome_options)
    driver.delete_all_cookies()

    yield driver

    print("\nClosing Chrome WebDriver...")
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture a screenshot and page source on test failure.
    Attaches both to the Allure report and the pytest-html report.
    """
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call" and report.failed:
        if "driver" not in item.funcargs:
            return

        driver_instance = item.funcargs["driver"]
        os.makedirs("reports/screenshots", exist_ok=True)
        screenshot_path = "reports/screenshots/%s_%d.png" % (item.name, int(time.time()))

        try:
            driver_instance.save_screenshot(screenshot_path)
            print("\n[FAILURE] Screenshot: %s" % screenshot_path)

            source_path = screenshot_path.replace(".png", "_source.html")
            with open(source_path, "w", encoding="utf-8") as f:
                f.write(driver_instance.page_source)
            print("[FAILURE] Page source: %s" % source_path)
            print("[FAILURE] URL at failure: %s" % driver_instance.current_url)

            with open(screenshot_path, "rb") as img:
                allure.attach(
                    img.read(),
                    name="Screenshot_%s" % item.name,
                    attachment_type=allure.attachment_type.PNG
                )

            relative = screenshot_path.replace("reports/", "")
            html = (
                "<div>"
                "  <p style=\"color:red;font-weight:bold;\">Test Failed — Screenshot:</p>"
                "  <img src=\"%s\" alt=\"Failure Screenshot\" "
                "       style=\"width:600px;border:2px solid red;cursor:pointer;\" "
                "       onclick=\"window.open(this.src)\"/>"
                "</div>" % relative
            )
            try:
                from pytest_html import extras
                extra.append(extras.html(html))
                report.extra = extra
            except Exception as e:
                print("[FAILURE] Could not attach to HTML report: %s" % e)

        except Exception as e:
            print("[FAILURE] Could not capture screenshot: %s" % e)
