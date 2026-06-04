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
# `wo_data` cases are provided dynamically by `conftest.build_wo_cases()`
# using the `generate_test_cases.load_tc_data()` loader. See `conftest.py`.


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
