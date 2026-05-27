"""
test_work_order_only.py
=======================
Work Order test suite — 10 parameterised test cases covering
required fields, optional fields, boundary dates, boundary quantities,
boundary rates, and edge-case remark length.

Test Cases:
  TC-WO-01  Required fields only (no optional fields)
  TC-WO-02  All fields including remark and expected receipt date
  TC-WO-03  Boundary date: order date = today
  TC-WO-04  Boundary date: order date = 1 day ahead
  TC-WO-05  Boundary date: order date = 1 year ahead
  TC-WO-06  Boundary quantity: outsource_qty = 1 (minimum)
  TC-WO-07  Boundary quantity: outsource_qty = 9999 (large)
  TC-WO-08  Boundary rate: rate = 1 (minimum)
  TC-WO-09  Boundary rate: rate = 99999 (high)
  TC-WO-10  Edge case: very long remark text (~500 chars)
"""

import pytest
import allure
import time
from datetime import date, timedelta
from pages.login_page import LoginPage
from pages.work_order_page import WorkOrderPage


def _d(offset_days=0):
    """Return an ISO date string (YYYY-MM-DD) offset from today."""
    return str(date.today() + timedelta(days=offset_days))


LONG_REMARK = (
    "Edge case long remark for work order boundary testing. "
    "This remark contains more than 200 characters to test the field's maximum "
    "capacity and ensure the form handles lengthy input gracefully without "
    "truncation or validation errors. Additional text to reach the limit here."
)

WO_CASES = [
    pytest.param(
        {"date": _d(1), "expected_receipt_date": "", "remark": "",
         "outsource_qty": "10", "rate": "100"},
        id="TC-WO-01-minimal-required-only"
    ),
    pytest.param(
        {"date": _d(3), "expected_receipt_date": _d(20),
         "remark": "Standard production batch run Q2",
         "outsource_qty": "50", "rate": "250"},
        id="TC-WO-02-normal-all-fields"
    ),
    pytest.param(
        {"date": _d(0), "expected_receipt_date": _d(10),
         "remark": "Boundary: order date = today",
         "outsource_qty": "20", "rate": "150"},
        id="TC-WO-03-boundary-date-today"
    ),
    pytest.param(
        {"date": _d(1), "expected_receipt_date": _d(7),
         "remark": "Boundary: 1 day future date",
         "outsource_qty": "15", "rate": "120"},
        id="TC-WO-04-boundary-date-1day-ahead"
    ),
    pytest.param(
        {"date": _d(365), "expected_receipt_date": _d(380),
         "remark": "Boundary: far future date 1 year ahead",
         "outsource_qty": "5", "rate": "500"},
        id="TC-WO-05-boundary-date-1year-ahead"
    ),
    pytest.param(
        {"date": _d(2), "expected_receipt_date": _d(5),
         "remark": "Boundary: minimum quantity = 1",
         "outsource_qty": "1", "rate": "200"},
        id="TC-WO-06-boundary-qty-minimum-1"
    ),
    pytest.param(
        {"date": _d(4), "expected_receipt_date": _d(30),
         "remark": "Boundary: large quantity 500",
         "outsource_qty": "500", "rate": "10"},
        id="TC-WO-07-boundary-qty-large-500"
    ),
    pytest.param(
        {"date": _d(5), "expected_receipt_date": _d(15),
         "remark": "Boundary: minimum rate = 1",
         "outsource_qty": "100", "rate": "1"},
        id="TC-WO-08-boundary-rate-minimum-1"
    ),
    pytest.param(
        {"date": _d(6), "expected_receipt_date": _d(20),
         "remark": "Boundary: very high rate 99999",
         "outsource_qty": "2", "rate": "99999"},
        id="TC-WO-09-boundary-rate-high-99999"
    ),
    pytest.param(
        {"date": _d(7), "expected_receipt_date": _d(25),
         "remark": LONG_REMARK,
         "outsource_qty": "30", "rate": "300"},
        id="TC-WO-10-edge-long-remark"
    ),
]


@allure.epic("TM-PMS Automation Suite")
@allure.feature("Work Order")
class TestWorkOrderOnly:

    @pytest.mark.run(order=1)
    @allure.story("Authentication")
    @allure.title("TC-WO-00 - Login before Work Order tests")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login(self, driver):
        """Login prerequisite — must pass before any Work Order test executes."""
        login = LoginPage(driver)
        with allure.step("Open application URL"):
            login.navigate()
        with allure.step("Login with valid credentials"):
            login.login("Prakasht@gmail.com", "1234")
        with allure.step("Verify redirect to dashboard"):
            time.sleep(3)
            url = driver.current_url
            print("Logged in. URL: %s" % url)
            assert "login" not in url.lower(), (
                "Login failed — still on login page. URL: %s" % url
            )

    @pytest.mark.run(order=2)
    @pytest.mark.parametrize("wo_data", WO_CASES)
    @allure.story("Work Orders")
    @allure.title("Create Work Order")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_work_order(self, driver, wo_data):
        """
        Create a Work Order with the supplied test data and verify
        that the form redirects to the Work Orders list on success.
        """
        wo_page = WorkOrderPage(driver)

        with allure.step("Navigate to Work Orders"):
            wo_page.navigate()

        with allure.step("Open creation form"):
            wo_page.click_add_new_work_order()

        with allure.step("Fill and submit Work Order form"):
            wo_page.create_work_order(wo_data)

        with allure.step("Verify redirect to Work Orders list"):
            url = driver.current_url
            print("Post-submit URL: %s" % url)
            assert "/create-work-order" not in url, (
                "Work Order creation failed — still on form. URL: %s" % url
            )
